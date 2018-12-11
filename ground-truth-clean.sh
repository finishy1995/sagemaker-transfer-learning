#!/bin/bash

# This shell script will help you clean the files and S3 objects and bucket created by ground-truth-setup.sh.


rm -rf ./bird/ ./car/ ./flower/ ./plane/
rm data.zip

cat 'buckets.ls' | while read line
do
    bucket=$line
    aws s3 rm s3://$bucket --recursive
    aws s3api delete-bucket --bucket $bucket
done

rm buckets.ls data.json metadata.json meta.lst
