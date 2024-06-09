import argparse
import json
import os
from cryptography.fernet import Fernet

#create Users.json & data folder
if not os.path.isdir('data'):
    os.makedirs('data')

def encrypt_user_info(info): #info is dict
    if not os.path.exists('data/mykey.key'): #create key & save
        key = Fernet.generate_key()
        with open('data/mykey.key', 'wb') as mykey:
            mykey.write(key)
    with open("data/mykey.key", 'rb') as mykey: #receive key 
        key = mykey.read()
        f = Fernet(key)
    with open('data/Admin.json', 'w') as file:
        for i in info.keys():
            info[i]['password'] = (f.encrypt(info[i]['password'].encode())).decode()
        json.dump(info, file, indent=4)
        

parser = argparse.ArgumentParser() 

parser.add_argument('newPerson') 
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()
new_admin = args.__dict__

if not os.path.exists("data/Admin.json") or  os.path.getsize("data/Admin.json") == 0:
    with open("data/Admin.json", 'w') as file:
        dict1 = {}
        json.dump(dict1, file, indent=4)

with open('data/Admin.json', 'r') as file:
    data = json.load(file)
    if (new_admin['username']) in data: #repetitive admin
        print('You are already admin.')
    else:
        data[new_admin['username']] = (new_admin)

encrypt_user_info(data)