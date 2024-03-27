import geopandas as gpd
import numpy as np
import json
import uuid
import argparse

# Define arguments
parser = argparse.ArgumentParser(description='Create CityJSON file from points and a 3D model (OBJ)')
parser.add_argument('--points', type=str, help='Path to shapefile containing points')
parser.add_argument('--model', type=str, help='Path to 3D model in OBJ format')
parser.add_argument('--save', type=str, help='Path to save CityJSON file', default='output.json')

# Parse arguments
args = parser.parse_args()

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

# Read shapefile containing points
points_shapefile = *args.points
points_gdf = gpd.read_file(points_shapefile)

# Add z-coordinate to points
points_gdf['x'] = points_gdf['geometry'].x
points_gdf['y'] = points_gdf['geometry'].y
points_gdf['z'] = 0

# Create a CityJSON object
cityjson = {
    "type": "CityJSON",
    "version": "1.1",
    "transform": {
        "scale": [1.0, 1.0, 1.0],
        "translate": [0.0, 0.0, 0.0]
    },
    "metadata": {
        "referenceSystem": f"http://www.opengis.net/def/crs/EPSG/0/{points_gdf.crs.to_epsg()}",
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
                # Rotation 90° around x-axis
                "transformationMatrix": [
                    1.0, 0.0, 0.0, 0.0,
                    0.0, 1.0, 0.0, 0.0,
                    0.0, 0.0, 1.0, 0.0,
                    0.0, 0.0, 0.0, 1.0
                ]
            }
        ]
    }


with open(args.save, 'w') as file:
    json.dump(cityjson, file, indent=4)