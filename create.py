import geopandas as gpd
import numpy as np
import json
import uuid
import argparse

# Create the argument parser
parser = argparse.ArgumentParser(description='Create CityJSON file from points and a 3D model (OBJ)', prog='template_cj')

# Add the arguments
parser.add_argument('--points', type=str, help='Path to shapefile containing points', required=True)
parser.add_argument('--model', type=str, help='Path to 3D model in OBJ format', required=True)
parser.add_argument('--save', type=str, help='Path to save CityJSON file', default='output.json')

parser.add_argument('--crs', type=int, help='EPSG code of the coordinate reference system', default=None)
parser.add_argument('--height', type=float, help='Name of the height attribute', default=None)
parser.add_argument('--rotation', type=float, nargs=3, help='Rotation angles (in degrees) around x, y, and z axes', default=[0.0, 0.0, 0.0])
parser.add_argument('--translation', type=float, nargs=3, help='Translation vector', default=[0.0, 0.0, 0.0])
parser.add_argument('--scale', type=float, nargs=3, help='Scale factor for the coordinates', default=[1.0, 1.0, 1.0])
parser.add_argument('--version', type=str, help='Version of the CityJSON file', default='1.1')

# Define function to read ASCII OBJ file
def read_obj(file):
    vertices = []
    faces = []

    with open(file, 'r') as file:
        for line in file:
            if line.startswith('v '):
                vertex = [float(i) for i in line.strip().split()[1:]]
                vertices.append(vertex)
            elif line.startswith('f '):
                face = [int(i.split('/')[0]) - 1 for i in line.strip().split()[1:]]
                faces.append(face)

    return vertices, faces

def create_cityjson():
    # Parse arguments
    args = parser.parse_args()

    crs = args.crs
    height = args.height
    rotation = args.rotation
    translation = args.translation
    scale = args.scale
    version = args.version

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
        "version": version,
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

    # Calculate the transformation matrix
    rotation = np.radians(rotation)
    rotation_matrix = np.array([
        [1, 0, 0],
        [0, np.cos(rotation[0]), -np.sin(rotation[0])],
        [0, np.sin(rotation[0]), np.cos(rotation[0])]
    ])
    translation = np.array(translation)
    scale = np.array(scale)
    transformation_matrix = np.eye(4)
    transformation_matrix[:3, :3] = rotation_matrix
    transformation_matrix[:3, 3] = translation
    transformation_matrix[:3, :3] *= scale

    # Create CityObject for each instance, first generate UUIDs, then add CityObject as a dictionary where geometry is as follows:
    for index, point in enumerate(points_gdf.iterrows()):
        fid = str(uuid.uuid4())
        # Get attributes of the point except geometry
        attributes = point[1].drop(['geometry', 'x', 'y', 'z']).to_dict()
        cityjson['CityObjects'][fid] = {
            "type": "GenericCityObject",
            "attributes": attributes,
            "geometry": [
                {
                    "type": "GeometryInstance",
                    "template": 0,
                    "boundaries": [index],
                    "transformationMatrix": transformation_matrix.tolist()
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
