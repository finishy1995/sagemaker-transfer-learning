import sys
import json
import random
import subprocess
import os
import mxnet as mx

def write_lst(file_name, content):
	lst = []

	for index in range(len(content)):
		lst.append(str(index) + '\t' + content[index][0]+ '\t' + content[index][1] + '\n')

	with open(file_name + '.lst', 'w') as file:
		file.writelines(lst)

def read_lst(file_name):
	content = []

	with open(file_name + '.lst', 'r') as file:
		lst = file.readlines()

	for line in lst:
		line = line[:-1]
		pod = line.split('\t')

		if len(pod) == 3:
			content.append([pod[1], pod[2]])
		else:
			print("Error in line %s"%(line))

	return content

def read_metadata():
	with open('metadata.json', 'r') as file:
		content = file.read()

	return json.loads(content)

def create_lst_rec(file_name, flower_size, car_size, bird_size, plane_size, train_ratio):
	metadata = read_metadata()

	flag = True
	if flower_size > metadata['flower']['size']:
		flag = False
	elif car_size > metadata['car']['size']:
		flag = False
	elif bird_size > metadata['bird']['size']:
		flag = False
	elif plane_size > metadata['plane']['size']:
		flag = False
	if not flag:
		print("Argv input error.")
		return

	flower_range = range(metadata['flower']['size'])
	car_range = range(metadata['flower']['size'], metadata['flower']['size'] + metadata['car']['size'])
	bird_range = range(metadata['flower']['size'] + metadata['car']['size'], metadata['flower']['size'] + metadata['car']['size'] + metadata['bird']['size'])
	plane_range = range(metadata['flower']['size'] + metadata['car']['size'] + metadata['bird']['size'], metadata['flower']['size'] + metadata['car']['size'] + metadata['bird']['size'] + metadata['plane']['size'])
    
	flower_train_size = round(flower_size * train_ratio)
	car_train_size = round(car_size * train_ratio)
	bird_train_size = round(bird_size * train_ratio)
	plane_train_size = round(plane_size * train_ratio)
    
	flower_train_sample = [i for i in sorted(random.sample(flower_range, flower_train_size))]
	car_train_sample = [i for i in sorted(random.sample(car_range, car_train_size))]
	bird_train_sample = [i for i in sorted(random.sample(bird_range, bird_train_size))]
	plane_train_sample = [i for i in sorted(random.sample(plane_range, plane_train_size))]
	lst_train_sample = flower_train_sample + car_train_sample + bird_train_sample + plane_train_sample
    
	flower_range = [i for i in flower_range if i not in flower_train_sample]
	car_range = [i for i in car_range if i not in car_train_sample]
	bird_range = [i for i in bird_range if i not in bird_train_sample]
	plane_range = [i for i in plane_range if i not in plane_train_sample]
    
	flower_val_sample = [i for i in sorted(random.sample(flower_range, flower_size - flower_train_size))]
	car_val_sample = [i for i in sorted(random.sample(car_range, car_size - car_train_size))]
	bird_val_sample = [i for i in sorted(random.sample(bird_range, bird_size - bird_train_size))]
	plane_val_sample = [i for i in sorted(random.sample(plane_range, plane_size - plane_train_size))]
	lst_val_sample = flower_val_sample + car_val_sample + bird_val_sample + plane_val_sample
    
	meta_lst = read_lst('meta')
	train_content = []
	for index in lst_train_sample:
		train_content.append(meta_lst[index])
	random.shuffle(train_content)
	val_content = []
	for index in lst_val_sample:
		val_content.append(meta_lst[index])
	random.shuffle(val_content)
    
	write_lst(file_name + '_train', train_content)
	write_lst(file_name + '_val', val_content)

	im2rec_path = os.path.join(mx.__path__[0], 'tools/im2rec.py')
	if not os.path.exists(im2rec_path):
		im2rec_path = os.path.join(os.path.dirname(os.path.dirname(mx.__path__[0])), 'tools/im2rec.py')
     
	subprocess.check_call(["python", im2rec_path,
        os.path.abspath(file_name + '_train.lst'), os.path.abspath('./'), '--resize=224'])
	subprocess.check_call(["python", im2rec_path,
        os.path.abspath(file_name + '_val.lst'), os.path.abspath('./'), '--resize=224'])

def main():
	if len(sys.argv) == 4:
		create_lst_rec(sys.argv[1], int(sys.argv[2]), int(sys.argv[2]), int(sys.argv[2]), int(sys.argv[2]), float(sys.argv[3]))
	elif len(sys.argv) == 7:
		create_lst_rec(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), float(sys.argv[6]))
	else:
		print("Argv input error.")

if __name__ == '__main__':
  main()
