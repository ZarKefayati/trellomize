import os
import json



class User:
    def __init__(self, Email, username, password, active):
        self.Email = Email
        self.username = username
        self.password = password
        self.active = active
    def setUsername(self, username , file):
        if username in file:
            username = input("The username is already available. \nEnter another one \n(1. exit)")
            if username == '1':
                menu()
                return

        elif  len(username) < 4 or len(username) > 10:
            self.setUsername(input("Characters must be between 4 and 10. Enter another one:"), file)
        else:
            self.username = username



def sign_in ():
    username = input('Enter username: ')
    password = input('Enter password: ')
    if os.path.exists("Users.json"):
        with open("Users.json") as file:
            data = json.load(file)
        if username in data:
            #decryption
            from cryptography.fernet import Fernet
            with open("mykey.key", 'rb') as mykey:
                key = mykey.read()
            f = Fernet(key)
            with open(username + '.json', 'rb') as encrypted_file:
                encrypted = encrypted_file.read()
            decrypted = f.decrypt(encrypted)
            information = eval(decrypted.decode())
            if information['password'] == password: #check password
                print ('yes')

        else:
            print('Username is not exsits. create an account first.')
            create_acount()
    else:
        print('Username is not exsits. create an account first.')
        create_acount()


def create_acount ():
    User1 = User("", "", "", "Active")

    #get Email
    User1.Email = input('Enter your Email: ')

    #create Users.json
    if not os.path.exists("Users.json"):
        with open("Users.json", 'w') as file:
            lst = []
            json.dump(lst,file, indent=0)

    #get username
    username = input('Enter a username: ')
    with open("Users.json", 'r') as file:    
        data = json.load(file)
        User1.setUsername(username, data)
        data.append(User1.username)
    with open("Users.json", 'w') as file:
        json.dump(data, file, indent=0)

    #get password
    User1.password = input('Enter your password: ')


    #adding information in another file
    file = open(User1.username + ".json" , 'w')
    item = {"Email" : User1.Email , "username" : User1.username , "password" : User1.password , "active" : User1.active}
    json.dump(item, file, indent=4)
    file.close()

    #encryption
    from cryptography.fernet import Fernet
    if not os.path.exists('mykey.key'): #create key & save
        key = Fernet.generate_key()
        with open('mykey.key', 'wb') as mykey:
            mykey.write(key)
    else:
        with open('mykey.key', 'rb') as mykey:
            key = mykey.read()

    f = Fernet(key)
    with open(User1.username + ".json", 'rb') as original_file:
        original = original_file.read()
    encrypted = f.encrypt(original) 
    with open(User1.username + ".json", 'wb') as encrypted_file:
        encrypted_file.write(encrypted)


def menu():
    k = input('1. create account\n2. sign in\n')
    if k == '1':
        create_acount()
    elif k == '2':
        sign_in()

menu()