import os
import json
from cryptography.fernet import Fernet
from rich import print
from rich.panel import Panel
from rich.text import Text
from rich.console import Console

class User:
    def __init__(self, Email, username, password, active):
        self.Email = Email
        self.username = username
        self.password = password
        self.active = active
    def setUsername(self, username , file):
        if username in file: #Duplicate username
            username = input ("Username already exists. Enter username or 1 to exit:")
            if username == '1': 
                menu()
                return
            else:
                self.setUsername(username, file)
                return

        elif  len(username) < 4 or len(username) > 10: #incorrect username
            self.setUsername(input("Characters must be between 4 and 10. \nEnter another one:"), file)
        else: #correct username & save
            self.username = username

class field:
    pass

class project:
    def __init__(self, Leader, ID, Title, Fields, Users): 
        self.Leader = Leader
        self.ID = ID
        self.Title = Title
        self.Fields = Fields
        self.Users = Users

def sign_in (username, password):
    #decryption
    if os.path.exists('users/' + username + ".json"):
        with open("mykey.key", 'rb') as mykey: #receive key 
            key = mykey.read()
        f = Fernet(key)
        with open('users/' + username + '.json', 'rb') as encrypted_file: #receive user information 
            encrypted = encrypted_file.read()
        decrypted = f.decrypt(encrypted) #decryption
        information = eval(decrypted.decode()) #byte to str
        if information['password'] == password: #check password
            if information["active"] == 'Active':
                print(Text('yes', 'bold green')) 
            else:
                print('no')
        else:
            k = input('Password is incorrect.\nEnter your password or 1 to exit:')      
            if k == '1': 
                menu()
                return
            else:
                sign_in(username, k)
                return
    else:
        k = input("Username is not exsits. \nEnter username or 1 to exit:")
        if k == '1': 
            menu()
            return
        else:
            sign_in(k, password)
            return

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
    file = open('users/' + User1.username + ".json" , 'w')
    item = {"Email" : User1.Email , "username" : User1.username , "password" : User1.password , "active" : User1.active}
    json.dump(item, file, indent=4)
    file.close()

    #encryption
    if not os.path.exists('mykey.key'): #create key & save
        key = Fernet.generate_key()
        with open('mykey.key', 'wb') as mykey:
            mykey.write(key)
    else:
        with open('mykey.key', 'rb') as mykey:
            key = mykey.read()

    f = Fernet(key)
    with open('users/' + User1.username + ".json", 'rb') as original_file:
        original = original_file.read()
    encrypted = f.encrypt(original) 
    with open('users/' + User1.username + ".json", 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

def menu():
    from rich import print
    from rich.panel import Panel
    from rich.text import Text
    from rich.console import Console
    console = Console()
    panel = Panel(Text('1. create account\n2. sign in', justify="left")) 
    k = console.input(panel)
    if k == '1':
        create_acount()
    elif k == '2':
        from rich.console import Console
        from rich.text import Text
        console = Console()
        username = console.input(Text("Enter username: ","bold green"))
        password = console.input(Text("Enter password: ","bold green"))
        sign_in(username, password)

def Account_page(username):
    pass

menu()