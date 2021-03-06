# DeepLandforms-YOLOv5
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4430015.svg)](https://doi.org/10.5281/zenodo.4430015)


This repository has been developed to provide a simplified YOLOv5 Object Detection workflow using georefernced images, from training to GIS mapping of results.
YOLOv5 is developed by [ultralytics](https://github.com/ultralytics/yolov5)  and has been modified to adapt to georeferenced images and GIS.
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4418161.svg)](https://doi.org/10.5281/zenodo.4418161)

Abstract has been accepted and published at Lunar Planetary Scince Conference 2021 

https://www.hou.usra.edu/meetings/lpsc2021/pdf/1316.pdf

This study is within the Europlanet 2024 RI, and it has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 871149. Mars images were obtained from NASA PDS.

## Notebooks
Two interactive notebooks:
- Training PyTorch YOLOv5 models (developed by [ultralytics](https://github.com/ultralytics/yolov5))
- Inference on georeferenced images and create create a shapefile with results.

## Python scripts
- General utilities to support both notebooks
- Script to convert detections to shapefile using georeferenced images or images + world files

## Dataset structure
Dataset must have a configuration file in YAML format with the following structure.
If you are using Roboflow prepared dataset skip this part, else prepare the dataset folder as follow:

Organize the dataset folder as following:

* *datasetfolder/train/images*
* *datasetfolder/valid/images*

then create a dataset.yaml file containing:

* train: *path to datasetfolder/train/images*
* valid: *path to datasetfolder/valid/images*
* nc: *number of classes*
* names: ['label1','label2','...']

## Usage
**TRAINING**

### Simple
Prepare the dataset then run the training notebook as it is, it will ask for:
- source folder
- model (small, medium, large, extra)
### Advanced
Edit the training parameters dictionary according to your needs

**INFERENCE**

### Simple 
Just run the inference notebook as it is, it will ask for:
- weights folder
- source folder
- destination folder



