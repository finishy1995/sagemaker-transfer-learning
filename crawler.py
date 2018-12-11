import urllib2
import urllib
import re
import sys
import boto3

count = 0
label = "flower"
bucket = "davwan-dataset"
s3 = boto3.resource('s3')
flower_labels = ['Flower']
car_labels = ['Van', 'Caravan', 'Truck', 'Car', 'Pickup Truck']
bird_labels = ['Bird']
plane_labels = ['Airplane', 'Aircraft']

def img_crawler(url):
	global count

	img_exp = r"<img[\s\S]*?>"
	img_src_exp = r"src=\"[\s\S]*?\""

	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	page_contents = response.read()
	img_metadata = re.findall(img_exp, page_contents, re.I)
	img_arr = []

	for index in xrange(len(img_metadata)):
		img_src = re.search(img_src_exp, img_metadata[index], re.I).group(0)
		if img_src != "" and not "/static/img/" in img_src:
			img_arr.append(img_src[5:-1])

	for index in xrange(len(img_arr)):
		img = img_download(img_arr[index], index)
		img_upload(img)
		img_clean(img)

	count += len(img_arr)

def img_download(url, index):
	img = "%s/%s.jpg"%(label, str(count + index))
	urllib.urlretrieve(url, "./" + img)

	return img

def img_upload(img):
	s3.meta.client.upload_file("./" + img, bucket, img)

def img_clean(img):
	rek = boto3.client('rekognition', region_name='us-east-1')
	s3 = boto3.client('s3', region_name='us-east-1')

	response = rek.detect_labels(
    	Image={
        	'S3Object': {
            	'Bucket': bucket,
            	'Name': img
        	}
    	}
	)

	img_labels = response.get('Labels', [])
	print "Image Key: ", img
	if label == "flower":
		labels = flower_labels
		ex_labels = car_labels + bird_labels + plane_labels
	elif label == "car":
		labels = car_labels
		ex_labels = flower_labels + bird_labels + plane_labels
	elif label == "bird":
		labels = bird_labels
		ex_labels = car_labels + flower_labels + plane_labels
	elif label == "plane":
		labels = plane_labels
		ex_labels = car_labels + bird_labels + flower_labels
	flag = 0

	for img_label in img_labels:
		if img_label.get('Name', '') in labels and flag == 0:
			flag = 1
		if img_label.get('Name', '') in ex_labels:
			flag = 2
	print flag

	if flag != 1:
		s3.delete_object(
			Bucket=bucket,
    		Key=img,
		)

def main():
	global label

	for index in xrange(1, 101):
		img_crawler("https://pixabay.com/en/photos/%s/?image_type=photo&pagi=%s"%(label, str(index)))
	label = 'car'
	for index in xrange(1, 101):
		img_crawler("https://pixabay.com/en/photos/%s/?image_type=photo&pagi=%s"%(label, str(index)))
	label = 'bird'
	for index in xrange(1, 101):
		img_crawler("https://pixabay.com/en/photos/%s/?image_type=photo&pagi=%s"%(label, str(index)))
	label = 'plane'
	for index in xrange(1, 51):
		img_crawler("https://pixabay.com/en/photos/%s/?image_type=photo&pagi=%s"%(label, str(index)))

if __name__ == '__main__':
    main()
