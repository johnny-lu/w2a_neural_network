import json

def open_file(filename):
        with open(filename, 'r') as data_file:
            data = json.load(data_file)
        return data

small_dict = open_file('lhdepart_lharrive.json')
big_dict = open_file('omconsign_signed.json')

for key in small_dict:
    small_dict[key]
    big_dict[key]
    print(small_dict[key]/big_dict[key])
   
