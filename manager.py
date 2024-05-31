import argparse
import json
import os
from cryptography.fernet import Fernet

def encrypt_user_info(info): #info is dict
    with open("mykey.key", 'rb') as mykey: #receive key 
        key = mykey.read()
        f = Fernet(key)
    with open('Admin.json', 'w') as file:
        for i in info.keys():
            info[i]['password'] = (f.encrypt(info[i]['password'].encode())).decode()
        json.dump(info, file, indent=4)
        

parser = argparse.ArgumentParser() 

parser.add_argument('newPerson') 
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()
new_admin = args.__dict__

if not os.path.exists("Admin.json") or  os.path.getsize("Admin.json") == 0:
    with open("Admin.json", 'w') as file:
        dict1 = {}
        json.dump(dict1, file, indent=4)

with open('Admin.json', 'r') as file:
    data = json.load(file)
    if (new_admin['username']) in data: #repetitive admin
        print('You are already admin.')
    else:
        data[new_admin['username']] = (new_admin)

encrypt_user_info(data)