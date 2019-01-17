#!/bin/bash

# This shell script will help you use the DEMO dataset to test Amazon SageMaker Ground Truth.


# Unzip All Image Data
wget https://s3.amazonaws.com/davwan-dataset/data.zip
unzip ./data.zip
echo

# Install MXNet, awscli
pip install mxnet
pip install awscli
echo

# Create a new S3 bucket
bucket=sagemaker-data-labeling-$(date "+%Y%m%d%H")-$RANDOM
echo $bucket >> buckets.ls

# Setup metadata, Ground Truth input data
python setup.py $bucket
echo "Data set setup successfully."

# Upload Images and input data (Ground Truth required json list) to Amazon S3
aws s3api create-bucket --bucket $bucket
aws s3 cp ./ s3://$bucket/ --recursive --exclude "*" --include "bird/*" --include "car/*" --include "flower/*" --include "plane/*" --include "data.json"
echo

# Input data file.
echo You can now open Amazon SageMaker console to test Ground Truth, your input data location:
echo s3://$bucket/data.json
