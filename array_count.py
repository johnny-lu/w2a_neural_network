import json

with open ('test_result_array.json') as data_file:
	data = json.load(data_file)
print(len(data))
