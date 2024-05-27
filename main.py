import os
import json
from cryptography.fernet import Fernet
from rich import print
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
import datetime as dt


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

class Tasks:
    def __init__(self ,name="" ,description="", priority="" ,status=""):
        self.uniq_id = uuid.uuid4()
        self.name=name
        self.description=description
        self.start_date = dt.datetime.now()
        self.last_date = dt.combine(dt.today(), self.start_date + dt.timedelta(hours=24).time())
        
        self.degr=("CRITICAL" , "HIGH" , "MEDIUM" , "LOW")
        if priority in self.degr:
            self.priority = priority
        else:
            print("Your priority is not able")
        self.position = ("BACKLOG" , "TODO" , "DOING" , "DONE" , "ARCHIVED") 
        if status in self.position:
            self.position = status 

        self.history = [] 
        self.comments = []

    def add_history(self, user, change_assiAssignees, change_priority, change_status):
        self.history.append({'user':user,'change_in_assiAssignees':change_assiAssignees, 'change_in_priority':change_priority,'change_in_status':change_status, 'timestamp':dt.now()})

    def add_comment(self, username, comment):
        self.comments.append({'username':username,'comment':comment,'start_date':dt.now()})
    
    def __repr__(self):
        return (f"Task(id={self.uniq_id}, title={self.task_name}, start_date={self.start_date}"+
                f"end_date={self.last_date}, "+
                f"history={self.history}, comments={self.comments}")

class project:
    def __init__(self, Leader, ID, Title, Fields, Users): 
        self.Leader = Leader
        self.ID = ID
        self.Title = Title
        self.Fields = Fields
        self.tasks_dict = {}
        self.Users = set() # assignees
    
    def setID(self, ID , file):
        if ID in file: #Duplicate username
            ID = input ("Username already exists. Enter username or 1 to exit:")
            if ID == '1': 
                Account_page(username)
                return
            else:
                self.setID(ID, file)
                return

        elif  len(ID) < 4 or len(ID) > 10: #incorrect username
            self.setID(input("Characters must be between 4 and 10. \nEnter another one:"), file)
        else: #correct username & save
            self.ID = ID

    def add_user(self, username , file):
        if username in file: #Correct Username 
            if username not in self.Users: 
                self.Users.append(username) #save
            else: #Duplicate Username
                username = input ("User is already here. \nEnter another one or 1 to exit:")
                if username == '1': 
                    Account_page(username)
                    return
                else:
                    self.add_user(username, file)
                    return

        else: #Unavailable Username
            username = input ("Username is not exists. Enter username or 1 to exit:")
            if username == '1': 
                Account_page(username)
                return
            else:
                self.add_user(username, file)
                return

    def add_task(self, task_name, members_names): #members_names is a list
        for member_name in members_names:
            if member_name not in self.Users:
                print(f"'{member_name}' is not in the members of project.")
                return
        self.tasks_dict[task_name] = members_names
        print(f"{task_name} is given to {members_names}.")


    def add_member_to_task(self, task_name, member_name):
        if member_name in self.Users:
            self.tasks_dict[task_name].append(member_name)
            print(f"{task_name} is given to {member_name}.")
        else:
            print(f"'{member_name}' is not in the members of project.")



    def delete_task(self, task_name):
        del_task = self.tasks_dict.pop(task_name)
        print(f" task '{task_name}' deleted.")

    def Assignees(self):
        for t, m in self.tasks_dict.items():
            print(f"this task : {m} is given to : {t}") #can use new file



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
                Account_page(username)
                return
            else:
                print('Your account is inactived by admin.')
                menu()
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
    item = {"Email" : User1.Email , "username" : User1.username , "password" : User1.password , "active" : User1.active, "projects" : []}
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

    f = Fernet(key)  #encryption
    with open('users/' + User1.username + ".json", 'rb') as original_file:
        original = original_file.read()
    encrypted = f.encrypt(original)
    with open('users/' + User1.username + ".json", 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
    menu()

def create_project (username):
    #Create Project
    project1 = project(username, '', '', [], [username])
    #create "ID.json"
    if not os.path.exists("ID.json"):
        with open("ID.json", 'w') as file:
            lst = []
            json.dump(lst,file, indent=0)
    #get ID
    ID = input('Enter a project ID: ') #Unik ID & Save
    with open("ID.json", 'r') as file:    
        data = json.load(file)
        project1.setID(ID, data)
        data.append(project1.ID)
    with open("ID.json", 'w') as file: 
        json.dump(data, file, indent=0)

    project1.Title = input('Enter a title: ') #Title
    user = username
    while user != '1':
        with open('Users.json', 'r') as file: #Add Users
            project1.add_user(user, file.read())
        #Add project to Users (encrypt)
        with open("mykey.key", 'rb') as mykey: #receive key 
            key = mykey.read()
        f = Fernet(key)
        with open('users/' + user + '.json', 'rb') as encrypted_file: #receive user information 
            encrypted = encrypted_file.read()
        decrypted = f.decrypt(encrypted) #decryption
        information = eval(decrypted.decode()) #byte to str to dict
        if user != username:
            information['projects_member'].append(project1.ID)
        else:
            information['projects_leader'].append(project1.ID)
        print(information)
        with open('users/' + user + '.json', 'wb') as file:
            encrypted = f.encrypt((str(information)).encode())
            file.write(encrypted)
        user = input('Invite users to this project.\nEnter username or 1 to end: ') #Add Users
    
    # Save Project
    information = {
        'ID' : project1.ID,
        'title' : project1.Title,
        'members' :  project1.Users
        'fields' : project1.Fields,
        }
    with open('projects/' + project1.ID + '.json', 'w') as file:
        json.dump(information, file, indent=4)   

    Account_page(username)

def create_Task (ID):


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
    panel = Panel(Text(f'WELCOME {username}! \n1. create project\n2. leader projects\n3. user projects',"bold yellow", justify="left"))
    print(panel)
    k = input()
    if k == '1':
        create_project(username)


menu()
