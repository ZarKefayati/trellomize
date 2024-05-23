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
            self.setUsername(input("The username is already available. Enter another one:"), file)
        elif  len(username) < 4 or len(username) > 10:
            self.setUsername(input("Characters must be between 4 and 10. Enter another one:"), file)
        else:
            self.username = username


def sign_in ():
    username = input('Enter username: ')
    password = input('Enter password: ')
    if os.path.exists(file):
        file = open("Users.txt")
        if username in file.read():
            print('yes')
        else:
            print('Username is not exsits. create an account first.')
            create_acount()

def create_acount ():
    User1 = User("", "", "", "Active")
    User1.Email = input('Enter your Email: ')
    if not os.path.exists("Users.txt"):
        file = open("Users.json", 'w')
        lst = []
        json.dump(lst,file)
        file.close()
    file = open("Users.json")
    User1.setUsername(input('Enter a username: ') , json.load(file))
    User1.password = input('Enter your password: ')

    with open("Users.json", 'r') as file:
        data = json.load(file)
    new_name = User1.username
    data.append(new_name)
    with open("Users.json", 'w') as file:
        json.dump(data, file, indent=0)

    file = open(User1.username + ".json" , 'w')
    item = {"Email" : User1.Email , "username" : User1.username , "password" : User1.password , "active" : User1.active}
    json.dump(item, file, indent=4)
    file.close()

create_acount()

