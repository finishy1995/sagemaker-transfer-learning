#!/bin/bash

# This shell script will help you train the model by transfer learning using custom dataset.


# Unzip All Image Data
wget https://s3.amazonaws.com/davwan-dataset/data.zip
unzip ./data.zip
echo

# Install MXNet, awscli
pip install mxnet
pip install awscli
echo

# Setup metadata, meta lst file
python setup.py
echo "Data set setup successfully."

# Create custom dataset using mxnet
python lst_handler.py train 1000 1000 1000 300
python lst_handler.py val 100 100 100 30
