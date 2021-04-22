import yaml

with open(r'config.yaml') as file:
	print(file)
	dict = yaml.load(file, Loader=yaml.FullLoader)
	print(dict)

	print(yaml.dump(dict))
