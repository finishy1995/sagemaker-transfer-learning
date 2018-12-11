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

def create_lst_rec(file_name, flower_size, car_size, bird_size, plane_size):
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

	flower_sample = [i for i in sorted(random.sample(range(metadata['flower']['size']), flower_size))]
	car_sample = [i for i in sorted(random.sample(range(metadata['flower']['size'], metadata['flower']['size'] + metadata['car']['size']), car_size))]
	bird_sample = [i for i in sorted(random.sample(range(metadata['flower']['size'] + metadata['car']['size'], metadata['flower']['size'] + metadata['car']['size'] + metadata['bird']['size']), bird_size))]
	plane_sample = [i for i in sorted(random.sample(range(metadata['flower']['size'] + metadata['car']['size'] + metadata['bird']['size'], metadata['flower']['size'] + metadata['car']['size'] + metadata['bird']['size'] + metadata['plane']['size']), plane_size))]
	lst_sample = flower_sample + car_sample + bird_sample + plane_sample

	meta_lst = read_lst('meta')
	content = []
	for index in lst_sample:
		content.append(meta_lst[index])
	random.shuffle(content)

	write_lst(file_name, content)

	im2rec_path = os.path.join(mx.__path__[0], 'tools/im2rec.py')
	if not os.path.exists(im2rec_path):
		im2rec_path = os.path.join(os.path.dirname(os.path.dirname(mx.__path__[0])), 'tools/im2rec.py')
     
	subprocess.check_call(["python", im2rec_path,
        os.path.abspath(file_name + '.lst'), os.path.abspath('./')])

def main():
	if len(sys.argv) == 3:
		create_lst_rec(sys.argv[1], int(sys.argv[2]), int(sys.argv[2]), int(sys.argv[2]), int(sys.argv[2]))
	elif len(sys.argv) == 6:
		create_lst_rec(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
	else:
		print("Argv input error.")

if __name__ == '__main__':
  main()
