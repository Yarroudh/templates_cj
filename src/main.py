import geopandas as gpd
import numpy as np
import json
import uuid
import argparse
from src.utils import euler_to_rotation_matrix, read_obj

# Create the argument parser
parser = argparse.ArgumentParser(description='Create CityJSON file from points and a 3D model (OBJ)', prog='template_cj')

# Add the arguments
parser.add_argument('--points', type=str, help='Path to shapefile containing points', required=True)
parser.add_argument('--model', type=str, help='Path to 3D model in OBJ format', required=True)
parser.add_argument('--save', type=str, help='Path to save CityJSON file', default='output.json')
parser.add_argument('--type', type=str, help='Type of the CityObject', default='GenericCityObject', choices=['GenericCityObject', 'CityFurniture', 'OtherConstruction', 'Bridge', 'Building', 'PlantCover', 'SolitaryVegetationObject', 'TransportSquare', 'WaterBody'])
parser.add_argument('--crs', type=int, help='EPSG code of the coordinate reference system', default=None)
parser.add_argument('--height', type=float, help='Name of the height attribute', default=None)
parser.add_argument('--global_rotation', type=float, nargs=3, help='Rotation angles (in degrees) around x, y, and z axes', default=[0.0, 0.0, 0.0])
parser.add_argument('--global_translation', type=float, nargs=3, help='Translation vector', default=[0.0, 0.0, 0.0])
parser.add_argument('--global_scale', type=float, nargs=3, help='Scale factor for the coordinates', default=[1.0, 1.0, 1.0])
parser.add_argument('--local_rotation_x', type=str, help='Name of the local rotation attribute around x-axis', default=None)
parser.add_argument('--local_rotation_y', type=str, help='Name of the local rotation attribute around y-axis', default=None)
parser.add_argument('--local_rotation_z', type=str, help='Name of the local rotation attribute around z-axis', default=None)
parser.add_argument('--local_translation_x', type=str, help='Name of the local translation attribute along x-axis', default=None)
parser.add_argument('--local_translation_y', type=str, help='Name of the local translation attribute along y-axis', default=None)
parser.add_argument('--local_translation_z', type=str, help='Name of the local translation attribute along z-axis', default=None)
parser.add_argument('--local_scale', type=str, help='Name of the local scale attribute', default=None)

def create_cityjson():
    # Parse arguments
    args = parser.parse_args()

    object_type = args.type
    crs = args.crs
    height = args.height
    global_r = args.global_rotation
    global_t = args.global_translation
    global_s = args.global_scale
    local_r_x = args.local_rotation_x
    local_r_y = args.local_rotation_y
    local_r_z = args.local_rotation_z
    local_t_x = args.local_translation_x
    local_t_y = args.local_translation_y
    local_t_z = args.local_translation_z
    local_s = args.local_scale

    # Read shapefile containing points
    points_shapefile = args.points
    points_gdf = gpd.read_file(points_shapefile)

    # Add z-coordinate to points
    points_gdf['x'] = points_gdf['geometry'].x
    points_gdf['y'] = points_gdf['geometry'].y
    points_gdf['z'] = 0 if height is None else points_gdf[height]

    # Create a CityJSON object
    referenceSystem = f"http://www.opengis.net/def/crs/EPSG/0/{points_gdf.crs.to_epsg()}" if crs is None else f"http://www.opengis.net/def/crs/EPSG/0/{crs}"

    cityjson = {
        "type": "CityJSON",
        "version": "2.0",
        "transform": {
            "scale": [1.0, 1.0, 1.0],
            "translate": [0.0, 0.0, 0.0]
        },
        "metadata": {
            "referenceSystem": referenceSystem,
        },
        "CityObjects": {},
        "vertices": [],
        "geometry-templates": {}
    }

    # Create vertices for the CityJSON object
    cityjson['vertices'] = points_gdf[['x', 'y', 'z']].values.tolist()

    # Add the mesh vertices to the geometry-templates as a list for key "vertices-templates"
    model_file = args.model # Assuming the model is in OBJ format
    mesh = read_obj(model_file)
    vertices_templates = mesh[0]

    boundaries = []
    for face in mesh[1]:
        boundaries.append([face])

    # Define template object
    template = {
        "type": "MultiSurface",
        "lod": "2",
        "boundaries": boundaries
    }

    cityjson['geometry-templates']['templates'] = [template]
    cityjson['geometry-templates']['vertices-templates'] = vertices_templates

    # Calculate the global transformation matrix
    gamma, beta, alpha = global_r
    global_R = euler_to_rotation_matrix(gamma, beta, alpha)
    global_t = np.array(global_t)
    global_s = np.array(global_s)
    global_Transform = np.eye(4)
    global_Transform[:3, :3] = global_R
    global_Transform[:3, 3] = global_t
    global_Transform[:3, :3] *= global_s

    # If -0.0, convert to 0.0
    global_Transform = np.array([[0.0 if i == -0.0 else i for i in row] for row in global_Transform])

    # Create CityObject for each instance, first generate UUIDs, then add CityObject as a dictionary where geometry is as follows:
    for index, point in enumerate(points_gdf.iterrows()):
        fid = str(uuid.uuid4())

        # Calculate the local transformation matrix
        r_x = 0 if local_r_x is None else point[1].loc[local_r_x]
        r_y = 0 if local_r_y is None else point[1].loc[local_r_y]
        r_z = 0 if local_r_z is None else point[1].loc[local_r_z]
        t_x = 0 if local_t_x is None else point[1].loc[local_t_x]
        t_y = 0 if local_t_y is None else point[1].loc[local_t_y]
        t_z = 0 if local_t_z is None else point[1].loc[local_t_z]
        s = 1 if local_s is None else point[1].loc[local_s]

        local_R = euler_to_rotation_matrix(np.radians(r_x), np.radians(r_y), np.radians(r_z))
        local_t = np.array([t_x, t_y, t_z])
        scale_l = np.array([s, s, s])

        local_Transform = np.eye(4)
        local_Transform[:3, :3] = local_R
        local_Transform[:3, 3] = local_t
        local_Transform[:3, :3] *= scale_l

        # If -0.0, convert to 0.0
        local_Transform = np.array([[0.0 if i == -0.0 else i for i in row] for row in local_Transform])

        # Combine global and local transformations
        transformation_matrix = np.dot(global_Transform, local_Transform).flatten().tolist()

        # Get attributes of the point except geometry
        attributes = point[1].drop(['geometry', 'x', 'y', 'z']).to_dict()
        cityjson['CityObjects'][fid] = {
            "type": object_type,
            "attributes": attributes,
            "geometry": [
                {
                    "type": "GeometryInstance",
                    "template": 0,
                    "boundaries": [index],
                    "transformationMatrix": transformation_matrix
                }
            ]
        }


    with open(args.save, 'w') as file:
        json.dump(cityjson, file, indent=4)

    print(f"CityJSON file saved to {args.save}")

def main():
    create_cityjson()

if __name__ == '__main__':
    main()
