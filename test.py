from cryptography.fernet import Fernet

with open("mykey.key", 'rb') as mykey: #receive key 
    key = mykey.read()
    f = Fernet(key)
print (f.decrypt(b'gAAAAABmWc0-GSGRy2d_JZWvyMHAk-64bGOeN3Jkkkb_Pba3Vly13uIr-GKlR4dQzSsfVLBvIHu04CGgnRSYGFpPfTmYADoelA=='))