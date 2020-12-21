# Metadata extraction from German scientific papers 

This repository contains  a method of extraction metadata from  German scientific papers (PDF) using  [Detectron2](https://github.com/facebookresearch/detectron2) implementation and synthetic data of German publications.   

In this project we used an implementation of detectron2 that was trained with 200K images from PublayNet dataset ([model](https://github.com/hpanwar08/detectron2))and we re-finetuned it with 30k of our synthetic data.  

Our model extracts nine metadata classes:Title, Author, Journal, Abstract, Affiliation, Email, Address, DOI, Date.

## Quick Links

- [Data](#data)
- [Training and Evaluation](#training-and-evaluation)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Sample Results](#sample-results-of-our-model)
- [License](#license)
## Data
The Data contains around 44K papers with German and English content. 100 of  German scientific papers  randomly selected from available publications in [SSOAR](https://www.gesis.org/ssoar/home) with various layout and style. we extended our dataset by automatically generating synthetic papers based on the 28 most common layouts we identified during the mannual annotation phase. To this end, we randomly extracted metadata records from [SSOAR](https://www.gesis.org/ssoar/home) , [DBLP](https://dblp.org/xml/release/) ,  and a list of scientific affiliations from [Wikipedia](https://de.wikipedia.org/wiki/Liste).
For each of these layouts, we generated an average of 1600 synthetic papers by randomly inserting metadata from the extracted metadata at their corresponding positions on the first page.

## Training and Evaluation
### Training configuartion:
* we froze the stem and the first backbone layer:  `cfg.MODEL.BACKBONE.FREEZE_AT= 2`
*  learning rate of 0.0025
* Number of iterations: 15000
* 70% training, 15% validation, and 15% test data.
### Final model and config files
| Architecture                                                                                                                                       | Config file                                                 | Training Script            |
|---------------------------------------------------------------------------------------------------------------|-----------------------------------------------|--------------------------|
| [MaskRCNN Resnext101_32x8d FPN 3X](https://drive.google.com/file/d/1Ie1SeTKoqzPH86DN2xPBgEz-3qq6DLoE/view?usp=sharing) | configs/DLA_mask_rcnn_X_101_32x8d_FPN_3x.yaml | ./model_training/Final/detectron2_training_fullData.ipynb |

### Evaluation
 Dataset                                              |  AP     | AP50   | AP75   | AP Small | AP Medium | AP Large | 
|------------------------------------------|--------|---------|---------|------------|---------------|------------|
| Validation set | 90.363 | 95.828 | 95.269 | 74.173 | 81.523 | 95.273|
|Test set            |90.167 | 95.626 | 94.911 | 75.199 | 81.275 | 79.225|


 ## Installation

1. Run ```git@github.com:jagben/Metadata-extraction-from-German-scientific-papers.git``` to clone this repository.
2. [Download the model](https://drive.google.com/file/d/1Ie1SeTKoqzPH86DN2xPBgEz-3qq6DLoE/view?usp=sharing) and copy it to the [models/](models) folder
   (and probably also needed in /app/models/final/ )
3. There are two ways to install the model locally: using Docker or by manually installing the dependencies

### Docker Deployment
```
cd pubmexwebdemo

# run docker build to create the docker image using and specify the name of the image.
# For instance, run
docker build -t my-mexpub-app .

# run the docker image inside a container and specify a port. This will allow you to both use the model locally
# and run the web application on localhost
docker run -it -p 5000:5000 --name mexPubContainer my-mexpub-app:latest

# the web application can now be accessed from a browser using hhtp://localhost:5000

```
Note: by default, the web application makes inferences using the CPU. To run the model on a GPU for faster inference, set the use_cuda parameter to True inside [main.py](pubmexwebapp/main.py).

 | <img src="images/webApp_1.png" width=400> | <img src="images/webApp_2.png" width=400> |
 |---------------------------------------------------------------------------|---------------------------------------------------------------------------|

 ### Manual installation
 ##### Requirements:
 - Linux or macOS
 - Poppler >= 20.09.0 
 - Python ≥ 3.6
 - pip >= 20.2.3

```

# install the necessary dependencies
pip install -r requirements.txt 
pip install torch==1.5 torchvision==0.6 -f https://download.pytorch.org/whl/cu101/torch_stable.html 
pip install detectron2==0.1.3 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu101/torch1.5/index.html
pip install -U 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'
```
Note: Having multiple versions of Python installed in parallel (e.g., Python2 and Python3) can lead to errors related to the pycocotools. It is advisable to use Anaconda and run the installation inside a conda environment to prevent dependency conflicts. 

## Getting Started

### Run a simple demo of the model
Run below command from the main repository for prediction on a single PDF document. The demo will store two files at the specified output path: (i) an image of the PDF's first page including bounding boxes for the predictions, (ii) a .json file containing the inferred metadata.
```
# using the default model configurations and weights and making inferences using the CPU:
python demo/demo.py <path/to/input.pdf> <output/path/>

# you can also specify the path to the model dump, the configuration file and use CUDA instead of the CPU for faster inference as follows (optional):
python demo/demo.py <path/to/input.pdf> <output/path/> --model-dump <path/to/model.pth> --config-file <path/to/config-file.yaml> --use_cuda True

# for help run
python demo/demo.py -h
```

### In Python
```
from pubmex.pubmexinference import *

pubmex = PubMexInference(
	model_dump="../models/model_final.pth",
	config_file="../configs/train_config.yaml",
	use_cuda=False,
)

# Call the model with a given PDF document; returns a visualization object and a dictionary containing the inferred metadata
img_array, metadata = pubmex.predict("path/to/document.pdf")

```

## Sample results of our Model
| <img src="images/21375_1036.jpeg" width=400> | <img src="images/20011_1311.jpeg" width=400> |
|---------------------------------------------------------------------------|---------------------------------------------------------------------------|
| <img src="images/11703_510.jpeg" width=400> | <img src="images/11916_950.jpeg" width=400> |
| <img src="images/12455_890.jpeg" width=400> | <img src="/images/12715_540.jpeg" width=400> |


## License
[MIT](https://choosealicense.com/licenses/mit/)

