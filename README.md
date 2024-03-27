<img src="https://github.com/Yarroudh/templates_cj/assets/72500344/1b523bfa-b0d4-46d6-9400-69bc1c81fe90" alt="logo" width="200"/>

# CityJSON Geometry Templates Mapper

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Geomatics Unit of ULiege - Development](https://img.shields.io/badge/Geomatics_Unit_of_ULiege-Development-2ea44f)](http://geomatics.ulg.ac.be/)

CLI application to create CityJSON files from points and a 3D model (OBJ).

## Installation

You can install `templates_cj` by cloning this repository and then running:

```bash
pip install .
```

This will install the package locally from the current directory.

## Usage

```bash
usage: template_cj [-h] --points POINTS --model MODEL [--save SAVE]
                   [--type {GenericCityObject,CityFurniture,OtherConstruction,Bridge,Building,PlantCover,SolitaryVegetationObject,TransportSquare,WaterBody}]
                   [--crs CRS] [--height HEIGHT] [--global_rotation GLOBAL_ROTATION GLOBAL_ROTATION GLOBAL_ROTATION]
                   [--global_translation GLOBAL_TRANSLATION GLOBAL_TRANSLATION GLOBAL_TRANSLATION]
                   [--global_scale GLOBAL_SCALE GLOBAL_SCALE GLOBAL_SCALE] [--local_rotation_x LOCAL_ROTATION_X]
                   [--local_rotation_y LOCAL_ROTATION_Y] [--local_rotation_z LOCAL_ROTATION_Z]
                   [--local_translation_x LOCAL_TRANSLATION_X] [--local_translation_y LOCAL_TRANSLATION_Y]
                   [--local_translation_z LOCAL_TRANSLATION_Z] [--local_scale LOCAL_SCALE]

Create CityJSON file from points and a 3D model (OBJ)

optional arguments:
  -h, --help            show this help message and exit
  --points POINTS       Path to shapefile containing points
  --model MODEL         Path to 3D model in OBJ format
  --save SAVE           Path to save CityJSON file
  --type {GenericCityObject,CityFurniture,OtherConstruction,Bridge,Building,PlantCover,SolitaryVegetationObject,TransportSquare,WaterBody}
                        Type of the CityObject
  --crs CRS             EPSG code of the coordinate reference system
  --height HEIGHT       Name of the height attribute
  --global_rotation GLOBAL_ROTATION GLOBAL_ROTATION GLOBAL_ROTATION
                        Rotation angles (in degrees) around x, y, and z axes
  --global_translation GLOBAL_TRANSLATION GLOBAL_TRANSLATION GLOBAL_TRANSLATION
                        Translation vector
  --global_scale GLOBAL_SCALE GLOBAL_SCALE GLOBAL_SCALE
                        Scale factor for the coordinates
  --local_rotation_x LOCAL_ROTATION_X
                        Name of the local rotation attribute around x-axis
  --local_rotation_y LOCAL_ROTATION_Y
                        Name of the local rotation attribute around y-axis
  --local_rotation_z LOCAL_ROTATION_Z
                        Name of the local rotation attribute around z-axis
  --local_translation_x LOCAL_TRANSLATION_X
                        Name of the local translation attribute along x-axis
  --local_translation_y LOCAL_TRANSLATION_Y
                        Name of the local translation attribute along y-axis
  --local_translation_z LOCAL_TRANSLATION_Z
                        Name of the local translation attribute along z-axis
  --local_scale LOCAL_SCALE
                        Name of the local scale attribute
```

## Example

To create a CityJSON file using `templates_cj`, you can use the following command:

```bash
template_cj --points points.shp --model model.obj --save output.json
```

This is the basic command that will create a CityJSON file named `output.json` using the points from `points.shp`, the 3D model from `model.obj`, with default configuration.

```bash
template_cj --points points.shp --model model.obj --save output.json --type CityFurniture --crs 4326 --height elevation --rotation 0 90 0 --translation 0 0 0 --scale 1 1 1 --version 1.0
```

This command will create a CityJSON file named `output.json` using the points from `points.shp`, the 3D model from `model.obj`, as `CityFurniture` object, with EPSG code `4326`, height attribute named `elevation`, rotation angles of `0` degrees around the x-axis, `90` degrees around the y-axis, `0` degrees around the z-axis, no translation, no scaling, and with version `1.1`.

You can also specify a local rotation and translation if you have this data stored in your shapefile.

![image](https://github.com/Yarroudh/templates_cj/assets/72500344/9497c126-6281-497c-b466-ee27f60667e8)

## Author

This software was developped by [Anass Yarroudh](https://www.linkedin.com/in/anass-yarroudh/), Research Engineer at [University of Liege](http://uliege.be/).
For more detailed information please contact us via <ayarroudh@uliege.be>, we are pleased to send you the necessary information.

-----

Copyright © 2023, [GeoScITY Lab - ULiège](http://www.geoscity.uliege.be/). Released under [MIT License](https://github.com/Yarroudh/templates_cj/blob/main/LICENSE).
