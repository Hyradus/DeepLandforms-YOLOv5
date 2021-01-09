# DeepLandforms-YOLOv5

This repository has been developed to provide a simplified YOLOv5 Object Detection workflow using georefernced images, from training to GIS mapping of results.
YOLOv5 is developed by [ultralytics](https://github.com/ultralytics/yolov5) and has been modified to adapt to georeferenced images and GIS.

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



