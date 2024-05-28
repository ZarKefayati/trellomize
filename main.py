import os
import json
from cryptography.fernet import Fernet
from rich import print
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
import datetime as dt
import uuid


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
    def __init__(self ,name="" ,description="", priority="LOW" ,status="BACKLOG", hour = 24, day = 0, members = []): 
        self.ID = uuid.uuid4()
        self.name=name
        self.description=description
        self.start_date = dt.datetime.now()
        self.last_date = self.start_date + dt.timedelta(hours=hour, days=day)
        self.degr=["CRITICAL" , "HIGH" , "MEDIUM" , "LOW"]
        if priority in self.degr:
            self.priority = priority
        else:
            print("the priority is not able")
        self.position = ["BACKLOG" , "TODO" , "DOING" , "DONE" , "ARCHIVED"]
        if status in self.position:
            self.status = status 
        else:
            print("the status is not able")

        self.history = [] 
        self.comments = []
        self.members = members
    def add_history(self, user, change_assiAssignees, change_priority, change_status):
        self.history.append({'user':user,'change_in_assiAssignees':change_assiAssignees, 'change_in_priority':change_priority,'change_in_status':change_status, 'timestamp':dt.now()})

    def add_comment(self, username, comment):
        self.comments.append({'username':username,'comment':comment,'start_date':dt.datetime.now()})
    
    def __repr__(self):
        return (f"Task(id={self.uniq_id}, title={self.task_name}, start_date={self.start_date}"+
                f"end_date={self.last_date}, "+
                f"history={self.history}, comments={self.comments}")

class project:
    def __init__(self, Leader, ID, Title, Users): 
        self.Leader = Leader
        self.ID = ID
        self.Title = Title
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

    def add_member(self, username , file):
        if username in file: #Correct Username 
            if username not in self.Users: 
                self.Users.add(username) #save
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
    item = {"Email" : User1.Email ,
     "username" : User1.username ,
     "password" : User1.password ,
     "active" : User1.active,
     "projects_Leader" : [],
     "projects_Memder" : []
    }
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
    project1 = project(username, '', '', [username])
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
            project1.add_member(user, file.read())
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
        'Leader' : project1.Leader,
        'Title' : project1.Title,
        'Members' :  project1.Users,
        'Tasks' : project1.Fields
        }
    with open('projects/' + project1.ID + '.json', 'w') as file:
        json.dump(information, file, indent=4)   

    Account_page(username)


def edit_task_member (task1, ID, username):
    print(Text('task is created. you can change the details.' , 'blue'), 
    Panel('1.title'+ '\n' '2.description' + '\n' '3.start & end time' + '\n'
    '4.change priority (CRITICAL, HIGH, MEDIUM, LOW(default)' + '\n'
    '5.change status (BACKLOG(default), TODO, DOING, DONE, ARCHIVED)'+ '\n'
    '6.give to members' + '\n' '7.add comment' + '\n' + '8.Show details'))
    k = input()
    if k == '1':
        task1.name = input('Enter a title: ') #Title
        edit_task_member (task1, ID, username)
        return

    elif k == '2':
        task1.description = input('description of task (optional): ')
        edit_task_member (task1, ID, username)
        return

    elif k == '3':
        #start
        try: #does not match format
            input_year = input('Enter your Date to start: (e.g. 2024.01.01 15:30:00)')
            syear = dt.datetime.strptime(input_year, "%Y.%m.%d %H:%M:%S")
            task1.start_date_date = syear
        except:
            print (f"time data {input_year} does not match format '%Y.%m.%d %H:%M:%S'")
        finally:
            print (task1.start_date)
        #end
        try: #does not match format
            input_year = input('Enter your Date to end: (e.g. 2024.01.01 15:30:00)')
            syear = dt.datetime.strptime(input_year, "%Y.%m.%d %H:%M:%S")
            task1.last_date = syear
        except:
            print (f"time data {input_year} does not match format '%Y.%m.%d %H:%M:%S'")
        finally:
            print (task1.last_date)
        edit_task_member (task1, ID, username)
        return

    elif k == '4':
        n = input('1.CRITICAL\n2.HIGH\n3.MEDIUM\n4.LOW(default)\n')
        if n.isdigit() and 0 < int(n) < 5:
            task1.priority = task1.degr[int(n)-1]
        else:
            print('invalid number')
        edit_task_member (task1, ID, username)
        return

    elif k == '5':
        n = input('1.BACKLOG(default) \n2.TODO \n3.DOING \n4.DONE \n5.ARCHIVED\n')
        if n.isdigit() and 0 < int(n) < 6:
            task1.status = task1.position[int(n)-1]
        else:
            print('invalid number')
        edit_task_member (task1, ID, username)
        return

    elif k == '6':
        with open ('projects/' + ID + '.json') as file:
            information = eval(file.read())
        if username == information['Leader']:
            name = input('Enter member: ')
            if name in information['members']:
                task1.members.append(name)
            else:
                print('user is not member of project.')
        else:
            print("you ara not leader in the project.",
             "you can't add members.")
        edit_task_member (task1, ID, username)
        return

    elif k == '7':
        comment = input('Enter your comment: ')
        task1.add_comment(username, comment)
        edit_task_member (task1, ID, username)
        return
    
    elif k == '8':
        task_details = {
            "ID" : task1.ID,
            "Title" : task1.name,
            "Description" : task1.description,
            "Start Date" : task1.start_date,  
            "End Date" : task1.last_date,
            "priority" : task1.priority,
            "Status" : task1.status,
            "Members" : task1.members,
            "Comments" : task1.comments,
            "History" : task1.history
        }
        print(task_details)
        edit_task_member (task1, ID, username)
        return

def task_editor(task1, ID, username):
    print(Panel('1.add comment' + '\n' + '2.Show details'))
    if k == '1':
        comment = input('Enter your comment: ')
        task1.add_comment(username, comment)
        task_editor(task1, ID, username)
        return
    
    elif k == '2':
        task_details = {
            "ID" : task1.ID,
            "Title" : task1.name,
            "Description" : task1.description,
            "Start Date" : task1.start_date,  
            "End Date" : task1.last_date,
            "priority" : task1.priority,
            "Status" : task1.status,
            "Members" : task1.members,
            "Comments" : task1.comments,
            "History" : task1.history
        }
        print(task_details)
        task_editor(task1, ID, username)
        return
    pass

def create_Task (ID, username):
    task1 = Tasks()
    edit_task(task1, ID, username)
    with open ('projects/' + ID + '.json', 'r') as file:
        information = eval(file.read())
    task_item = {
        "ID" : task1.ID,
        "Title" : task1.name,
        "Description" : task1.description,
        "Start Date" : task1.start_date,  
        "End Date" : task1.last_date,
        "priority" : task1.priority,
        "Status" : task1.status,
        "Members" : task1.members,
        "Comments" : task1.comments,
        "History" : task1.history
    }
    information["Tasks"].append(task_item)

    with open ('projects/' + ID + '.json', 'w') as file:
        json.dump (information, file, indent=4)


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
