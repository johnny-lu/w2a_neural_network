import json

with open ('lhdepart_lharrive.json') as data_file:
	data = json.load(data_file)
print(len(data))
