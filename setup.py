import os
import json
import sys
from lst_handler import write_lst

def init():
	content = [] # All image data content
	manifest = [] # Amazon SageMaker Ground Truth input data
	metadata = {
		'flower': {
			'type': '0',
			'size': 0
		},
		'car': {
			'type': '1',
			'size': 0
		},
		'bird': {
			'type': '2',
			'size': 0
		},
		'plane': {
			'type': '3',
			'size': 0
		},
	}

	flower_size = 0
	for filename in os.listdir('./flower/'):
		flower_size += 1
		content.append(['0', os.path.abspath('./flower/' + filename)])
		manifest.append('flower/' + filename)
	metadata['flower']['size'] = flower_size
    
	car_size = 0
	for filename in os.listdir('./car/'):
		car_size += 1
		content.append(['1', os.path.abspath('./car/' + filename)])
		manifest.append('car/' + filename)
	metadata['car']['size'] = car_size
    
	bird_size = 0
	for filename in os.listdir('./bird/'):
		bird_size += 1
		content.append(['2', os.path.abspath('./bird/' + filename)])
		manifest.append('bird/' + filename)
	metadata['bird']['size'] = bird_size
    
	plane_size = 0
	for filename in os.listdir('./plane/'):
		plane_size += 1
		content.append(['3', os.path.abspath('./plane/' + filename)])
		manifest.append('plane/' + filename)
	metadata['plane']['size'] = plane_size
    
	write_lst('meta', content)
	
	metadata_json = json.dumps(metadata, sort_keys=True, separators=(',', ': '))
	with open('metadata.json', 'w') as file:
		file.write(metadata_json)
	manifest_json = ''
	data_bucket_name = "tmp"
	if sys.argv[1]:
		data_bucket_name = sys.argv[1]
	for item in manifest:
		key = "s3://" + data_bucket_name + "/" + item
		item_json = {"source-ref": key}
		manifest_json += json.dumps(item_json, sort_keys=True, separators=(',', ': ')) + '\n'
	with open('data.json', 'w') as file:
		file.write(manifest_json)

if __name__ == '__main__':
  init()
