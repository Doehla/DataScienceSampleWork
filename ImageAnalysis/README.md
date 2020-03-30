# Image Categorization Project
## Objective
Successfully develop a model that can categorize a given photo into a number of categories.
Image provided will be in one of the possible categories, but not multiple are not expected.

## Data
### Acquisition
For this project, data is pulled from
[here](https://www.kaggle.com/puneet6060/intel-image-classification/data#)
for use.
Data from this source is broken up into several folders with labeled folders for the category the image falls in.

### Wrangle
The data is extracted from these images and placed into an array of dimensions (150, 150, 3) for 150 x 150 image size and 3 channels for red, green, and blue.

This is done in DataWrangle.py and a file is exported to data/packaged/training_data.csv

### Clean
The data cleaning process is handled at the same time we are wrangling the data.
Functions exist that ensure we have the expected uniform shape.

This is done in DataWrangle.py and a file is exported to data/packaged/training_data.csv
