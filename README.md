<img src="https://user-images.githubusercontent.com/72500344/210864557-4078754f-86c1-4e7c-b291-73223bdf4e4d.png" alt="logo" width="200"/>

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
                   [--crs CRS] [--height HEIGHT] [--rotation ROTATION ROTATION ROTATION]
                   [--translation TRANSLATION TRANSLATION TRANSLATION] [--scale SCALE SCALE SCALE]        
                   [--version VERSION]

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
  --rotation ROTATION ROTATION ROTATION
                        Rotation angles (in degrees) around x, y, and z axes
  --translation TRANSLATION TRANSLATION TRANSLATION
                        Translation vector
  --scale SCALE SCALE SCALE
                        Scale factor for the coordinates
  --version VERSION     Version of the CityJSON file
```

## Example

To create a CityJSON file using `templates_cj`, you can use the following command:

```bash
template_cj --points points.shp --model model.obj --save output.json
```

This command will create a CityJSON file named `output.json` using the points from `points.shp`, the 3D model from `model.obj`, with default configuration.

```bash
template_cj --points points.shp --model model.obj --save output.json --type CityFurniture --crs 4326 --height elevation --rotation 0 90 0 --translation 0 0 0 --scale 1 1 1 --version 1.0
```

This command will create a CityJSON file named `output.json` using the points from `points.shp`, the 3D model from `model.obj`, as `CityFurniture` object, with EPSG code `4326`, height attribute named `elevation`, rotation angles of `0` degrees around the x-axis, `90` degrees around the y-axis, `0` degrees around the z-axis, no translation, no scaling, and with version `1.1`.

![image](https://github.com/Yarroudh/templates_cj/assets/72500344/9497c126-6281-497c-b466-ee27f60667e8)

## Author

This software was developped by [Anass Yarroudh](https://www.linkedin.com/in/anass-yarroudh/), a Research Engineer at the [Geomatics Unit of the University of Liege](http://geomatics.ulg.ac.be/fr/home.php).
For more detailed information please contact us via <ayarroudh@uliege.be>, we are pleased to send you the necessary information.

-----

Copyright © 2023, [Geomatics Unit of ULiège](http://geomatics.ulg.ac.be/fr/home.php). Released under [MIT License](https://github.com/Yarroudh/templates_cj/blob/main/LICENSE).
