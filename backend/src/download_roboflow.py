"""
Download Dataset from Roboflow
Paste your Roboflow code snippet here
"""

from roboflow import Roboflow

rf = Roboflow(api_key="Yib9c0GwevglUYIVcjCq")

# Dataset 1: Cigarette & Vape Detection
print("Downloading Dataset 1: Cigarette & Vape Detection...")
project1 = rf.workspace("takoyati").project("cigarette-vape-detection")
version1 = project1.version(14)
dataset1 = version1.download("yolov8")

rf = Roboflow(api_key="Yib9c0GwevglUYIVcjCq")
project = rf.workspace("sgugit-igrke").project("glasses-w4pwl")
version = project.version(4)
dataset = version.download("yolov8")
                

rf = Roboflow(api_key="Yib9c0GwevglUYIVcjCq")
project = rf.workspace("nyp-g6utj").project("earbuds-paaxr")
version = project.version(4)
dataset = version.download("yolov8")
                
rf = Roboflow(api_key="Yib9c0GwevglUYIVcjCq")
project = rf.workspace("battery-detector").project("personal-belongings")
version = project.version(3)
dataset = version.download("yolov8")
                
# After download, the datasets will be in the current directory
# You can then train with:
# python src/train.py --data path/to/data.yaml --epochs 100
