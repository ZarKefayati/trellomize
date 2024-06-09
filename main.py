import os
import json
from cryptography.fernet import Fernet
from rich import print
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
from rich.table import Table
import datetime as dt
import uuid
import logging
import re
import unittest
import shutil

console = Console()

#create Users.json & data folder
if not os.path.isdir('data'):
    os.makedirs('data')
#logging
error_logger = logging.getLogger('error_logger')
error_logger.setLevel(logging.ERROR)
error_file_handler = logging.FileHandler('data/errors.log')
error_formatter = logging.Formatter('%(asctime)s - %(message)s')
error_file_handler.setFormatter(error_formatter)
error_logger.addHandler(error_file_handler)

info_logger = logging.getLogger('info_logger')
info_logger.setLevel(logging.INFO)
info_file_handler = logging.FileHandler('data/user_actions.log')
info_formatter = logging.Formatter('%(asctime)s - %(message)s')
info_file_handler.setFormatter(info_formatter)
info_logger.addHandler(info_file_handler)


class User:
    def __init__(self, Email, username, password, active):
        self.Email = Email
        self.username = username
        self.password = password
        self.active = active
    def setUsername(self, username , file):
        if username in file: #Repetitive username
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
    def __init__(self ,name="" ,description="", priority="LOW" ,status="BACKLOG", hour = 24, day = 0, members = [], history = [], comments = [] ): 
        self.ID = uuid.uuid4()
        self.name=name
        self.description=description
        self.start_date = dt.datetime.now().replace(microsecond=0)
        self.last_date=self.start_date + dt.datetime(hour=24 , day=0)
        self.degr=["CRITICAL" , "HIGH" , "MEDIUM" , "LOW"]
        if priority in self.degr:
            self.priority = priority
        else:
            print("the priority is not able")
        self.statuses = ["BACKLOG" , "TODO" , "DOING" , "DONE" , "ARCHIVED"]
        if status in self.statuses:
            self.status = status 
        else:
            print("the status is not able")

        self.history = history
        self.comments = comments
        self.members = members
    def add_history(self, user, changes):
        self.history.append({'user':user,'changes':changes, 'timestamp':str(dt.datetime.now())})

    def add_comment(self, username, comment):
        self.comments.append({'username':username,'comment':comment,'start_date':str(dt.datetime.now())})
    
    def __repr__(self):
        return (f"Task(id={self.ID}, title={self.name}, start_date={self.start_date}"+
                f"end_date={self.last_date}, "+
                f"history={self.history}, comments={self.comments}")

class project:
    def __init__(self, Leader, ID, Title, Users = [], tasks_dict= {}): 
        self.Leader = Leader
        self.ID = ID
        self.Title = Title
        self.tasks_dict = tasks_dict
        self.Users = Users 
    
    def setID(self, ID , file):
        if ID in file: #Repetitive username
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
                self.Users.append(username) #save
            else: #Repetitive Username
                username = input ("User is already here. \nEnter another one or 1 to exit:")
                if username == '1': 
                    Account_page(username)
                    return
                else:
                    self.add_member(username, file)
                    return

        else: #Unavailable Username
            username = input ("Username is not exists. Enter username or 1 to exit:")
            if username == '1': 
                Account_page(username)
                return
            else:
                self.add_member(username, file)
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



    def delete_task(self, task_id):
        del_task = self.tasks_dict.pop(task_id)
        print(f" task '{task_name}' deleted.")

    def Assignees(self):
        for t, m in self.tasks_dict.items():
            print(f"this task : {m} is given to : {t}") #can use new file

#Tools
def decrypt_user_info(username):
    try: #file is empty or not exists
        with open("data/mykey.key", 'rb') as mykey: #receive key 
            key = mykey.read()
            f = Fernet(key)
        with open('users/' + username + '.json', 'rb') as encrypted_file: #receive user information 
            encrypted = encrypted_file.read()
            decrypted = f.decrypt(encrypted) #decryption
            information = eval(decrypted.decode()) #byte to str to dict
            return information
    except Exception as e:
        error_logger.error(f"error : {e} ")
        print(Text('Sorry! something went wrong. \nUser not found!', 'red'))
        menu()

def encrypt_user_info(username, info):
    with open("data/mykey.key", 'rb') as mykey: #receive key 
        key = mykey.read()
        f = Fernet(key)
    with open('users/' + username + '.json', 'wb') as file:
        encrypted = f.encrypt((str(info)).encode())
        file.write(encrypted)

def decrypt_admin_pass(username, password):
    try: #file is empty or not exists
        with open("data/mykey.key", 'rb') as mykey: #receive key 
            key = mykey.read()
            f = Fernet(key)
        with open('data/Admin.json', 'r') as encrypted_file: #receive user information 
            encrypted = json.load(encrypted_file)
            Truepass=f.decrypt((encrypted[username]['password']).encode()).decode()
            return Truepass == password
    except Exception as e:
        error_logger.error(f"error : {e} ")
        print(Text('Sorry! something went wrong. \nAdmin not found!', 'red'))
        menu()

def info_to_obj_task(task_item): #info = dict / task
    task = Tasks()
    task1.ID = task_item["ID"]
    task1.name = task_item["Title"] 
    task1.description = task_item["Description"]
    task1.start_date,  = task_item["Start Date"]
    task1.last_date = task_item["End Date"] 
    task1.priority = task_item["priority"] 
    task1.status = task_item["Status"] 
    task1.members = task_item["Members"] 
    task1.comments = task_item["Comments"] 
    task1.histor = task_item["History"]
    return task1

def info_to_obj_proj(info): #info = dict / proj
    project1 = project(info['Leader'], info['ID'], info['Title'], info['Members'], info['Tasks'])
    return project1

def is_valid_email(email):
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email)

#sign in
def sign_in (username, password):
    #decryption
    if os.path.exists('users/' + username + ".json"):
        information = decrypt_user_info(username)
        if information['password'] == password: #check password
            if information["active"] == 'Active':
                info_logger.info(f"user {username} signed in.")
                Account_page(username)
                return
            else:
                print('Your account is inactived by admin.')
                menu()
        else:
            k = input(Text('Password is incorrect.\nEnter your password or 1 to exit: ', 'red'))    
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

def sign_in_admin (username, password):
    #decryption
    if os.path.exists("data/Admin.json") and os.path.getsize("data/Admin.json") > 0:
        with open ("data/Admin.json", 'r') as file:
            information = json.load(file)
        if username in information.keys(): #check username
            if decrypt_admin_pass(username, password): #check password
                Account_page_admin(username)
            else:
                k = input(Text('Password is incorrect.\nEnter your password or 1 to exit: ', 'red'))    
                if k == '1': 
                    menu()
                    return
                else:
                    sign_in_admin(username, k)
                return
        else:
            k = input(Text('Username is incorrect.\nEnter username or 1 to exit: ', 'red'))    
            if k == '1': 
                menu()
                return
            else:
                sign_in_admin(k, password)
            return
    else:
        k = input("Something went wrong! sign up again.")
        return

#create
def create_acount ():
    User1 = User("", "", "", "Active")

    #get Email
    Email = input('Enter your Email: ')
    if is_valid_email(Email):
        User1.Email= Email
    else:
        print("Incorrect Email\n")
        create_acount()
    #create Users.json & data folder
    if not os.path.isdir('data'):
        os.makedirs('data')
    if not os.path.exists("data/Users.json"):
        with open("data/Users.json", 'w') as file:
            lst = []
            json.dump(lst, file, indent = 0)


    #get username
    username = input('Enter a username: ')
    with open("data/Users.json", 'r') as file:    
        data = json.load(file)
        User1.setUsername(username, data)
        data.append(User1.username)
    with open("data/Users.json", 'w') as file:
        json.dump(data, file, indent=0)


    #get password
    User1.password = input('Enter your password: ')


    #adding information in another file
    item = {"Email" : User1.Email ,
     "username" : User1.username ,
     "password" : User1.password ,
     "active" : User1.active,
     "projects_Leader" : [],
     "projects_Member" : []
    }
    if not os.path.isdir('users'):
         os.makedirs('users')
    if not os.path.exists('mykey.key'): #create key & save
        key = Fernet.generate_key()
        with open('mykey.key', 'wb') as mykey:
            mykey.write(key)
    encrypt_user_info(User1.username, item)
    info_logger.info(f"user {username} created account.")
    menu()
       
def create_project (username):
    #Create Project object
    project1 = project(username, '', '', [])
    #create "data/ID.json"
    if not os.path.exists("data/ID.json"):
        with open("data/ID.json", 'w') as file:
            lst = []
            json.dump(lst,file, indent=0)
    #get ID
    ID = input('Enter a project ID: ') #Unik ID & Save
    with open("data/ID.json", 'r') as file:    
        data = json.load(file)
        project1.setID(ID, data)
        data.append(project1.ID)
    with open("data/ID.json", 'w') as file: 
        json.dump(data, file, indent=0)

    project1.Title = input('Enter a title: ') #Title
    user = username
    while user != '1':
        with open('data/Users.json', 'r') as file: #Add Users
            project1.add_member(user, file.read())
        #Add project to Users (encrypt)
        if os.path.exists('users/' + user + '.json'):
            information = decrypt_user_info(user)
        else:
            print('user not found!')
            return
        if user != username: 
            information['projects_Member'].append(project1.ID)
        else:
            information['projects_Leader'].append(project1.ID)
        encrypt_user_info(user, information)
        user = input(Text('Invite users to this project.\nEnter username or 1 to end: ', 'magenta')) #Add Users
    
    # Save Project
    information = {
        'ID' : project1.ID,
        'Leader' : project1.Leader,
        'Title' : project1.Title,
        'Members' :  project1.Users,
        'Tasks' : project1.tasks_dict
        }
    #create projects folder
    if not os.path.isdir('projects'):
        os.makedirs('projects')
    with open('projects/' + project1.ID + '.json', 'w') as file:
        json.dump(information, file, indent=4) 
    info_logger.info(f"user {username} created project {project1.ID}.")
    edit_projet_leader(project1,username)
    Account_page(username)

def create_Task (project, username):
    ID = project.ID
    task1 = Tasks()
    edit_task_member(task1, project, username)
    task_item = {
        "ID" : str(task1.ID),
        "Title" : task1.name,
        "Description" : task1.description,
        "Start Date" : str(task1.start_date),  
        "End Date" : str(task1.last_date),
        "priority" : task1.priority,
        "Status" : task1.status,
        "Members" : task1.members,
        "Comments" : task1.comments,
        "History" : task1.history
    }
    project.tasks_dict[str(task1.ID)] = task_item
    with open ('projects/' + ID + '.json', 'r') as file:
        information = eval(file.read())
    information["Tasks"][str(task1.ID)] = task_item
    with open ('projects/' + ID + '.json', 'w') as file:
        json.dump (information, file, indent=4)
    info_logger.info(f"user {username} created task {task1.name} in project {project1.ID}.")

#edit project
def edit_projet_leader(project, username): 
    # Save changes
    information = {
        'ID' : project.ID,
        'Leader' : project.Leader,
        'Title' : project.Title,
        'Members' :  project.Users,
        'Tasks' : project.tasks_dict
        }
    #create projects folder
    with open('projects/' + project.ID + '.json', 'w') as file:
        json.dump(information, file, indent=4)

    print(Panel(Text(f"{project.ID} - {project.Title}\n" , 'bold magenta') 
    + Text("1.show members \n2.show tasks & edit & remove \n3.change info \n4.add/remove member \n5.Delete project \n6.exit", 'yellow')))
    k = input()
    if k == '1':
        print(project.Users)
        edit_projet_leader(project, username)
        return
    elif k == '2':
        n = input('1.New Task\n2.show tasks\n3.remove task\n')
        if n == '1':
            create_Task(project, username)
        elif n == '2':
            show_tasks(project.ID)
        elif n == '3':
            tasks = project['Tasks'] #dict of tasks
            id_i = {}
            lst = []
            for i , ID in zip(range(len(tasks)), tasks.keys()):
                lst.append(str(i+1) + '.' + tasks[ID]['Title'])
                id_i[str(i+1)] = ID
            i = input(Task("Enter a number to remove" , 'magenta'))
            project.delete_task(id_i[i])
        else:
            print(Text('invalid number' , 'red'))
        edit_projet_leader(project, username)
        return
       
    elif k == '3':
        print(Text(f'ID : {project.ID} \nTitle : {project.Title}' , 'green'))
        print('1.change ID\n2.change Title\n')
        n = input()
        if n == '1':
            newID = input(Text('Enter new ID: ', 'bold magenta'))
            with open("data/ID.json ", 'r') as file:
                if newID in file.read():
                    print('repetitive ID')
                    edit_projet_leader(project, username)
                    return
            with open('projects/' + project.ID + '.json' , 'r') as file:
                data = json.load(file)
            with open('projects/' + newID + '.json' , 'w')as file:
                data[project.ID] = newID
                json.dump(data , file , indent = 4)
            project.ID = newID
        elif n == '2':
            newTitle = input(Text('Enter new Title', 'magenta'))
            project.Title = newTitle
        else:
            print(Text('invalid number!' , 'red'))
            return
        edit_projet_leader(project, username)
        return
    elif k == '4':
        print(project.Users)
        n = input('1.add member\n2.remove member\n')
        if n == '1':
            user = input('Enter username: ')
            if os.path.exists('users/' + user + '.json'): #check
                information = decrypt_user_info(user)
            else:
                print('user not found!')
                return

            with open('data/Users.json', 'r') as file: #Add User to project
                project1.add_member(user, file.read())

            #Add project to User
            if user != username: 
                information['projects_Member'].append(project1.ID)
            else:
                information['projects_Leader'].append(project1.ID)
            encrypt_user_info(user, information)

        elif n == '2':
            user = input('Enter username: ')
            project.Users.remove(user)
        else:
            print("invalid number")

        edit_projet_leader(project, username)
        return

    elif k == '5':
        with open('projects/' + project.ID + '.json' , 'r') as file: #remove project from users data
            data = json.load(file)
        members = data["Members"]
        leader = data["Leader"]
        data = decrypt_user_info(member)
        data["projects-Leader"].pop(project.ID)
        for member in members:
            data = decrypt_user_info(member)
            data["projects-Member"].pop(project.ID)
        
        os.remove('projects/' + project.ID + '.json') #remove project file
        Account_page(username)
        return

    elif k == '6':
        Account_page(username)
        return

def edit_project(project, username):
    print(Panel(Text(f"{project.ID} - {project.Title}\n" , 'bold magenta') + Text("1.show members \n2.show tasks \n3.exit", 'yellow')))
    k = input()
    if k == '1':
        print(project.Users)
        edit_project(project, username)
        return
    elif k == '2':
        show_tasks(project.ID)
        edit_projet(project, username)
        return
    elif k == '3':
        Account_page(username)
        return

#edit task
def edit_task_member (task1, project, username):
    ID = project.ID
    #save project
    task_item = {
        "ID" : str(task1.ID),
        "Title" : task1.name,
        "Description" : task1.description,
        "Start Date" : str(task1.start_date),  
        "End Date" : str(task1.last_date),
        "priority" : task1.priority,
        "Status" : task1.status,
        "Members" : task1.members,
        "Comments" : task1.comments,
        "History" : task1.history
    }
    project.tasks_dict[str(task1.ID)] = task_item
    print(Text('you can change the details.' , 'blue'), 
    Panel('1.title'+ '\n' '2.description' + '\n' '3.start & end time' + '\n'
    '4.change priority (CRITICAL, HIGH, MEDIUM, LOW(default)' + '\n'
    '5.change status (BACKLOG(default), TODO, DOING, DONE, ARCHIVED)'+ '\n'
    '6.give to members' + '\n' '7.add comment' + '\n' + '8.Show details'
     + '\n' + '9.exit'))
    k = input()
    if k == '1':
        print (task1.name)
        task1.name = input('Enter a title: ') #Title
        task1.add_history(username,f'Title changed to {task1.name}.')
        edit_task_member (task1, project, username)
        return

    elif k == '2':
        print (task1.description)
        task1.description = input('description of task (optional): ')
        task1.add_history(username,f'description changed to {task1.description}.')
        edit_task_member (task1, project, username)
        return

    elif k == '3':
        #start
        try: #does not match format
            input_year = input(f'Enter your Date to start: (e.g. {task1.start_date})')
            syear = dt.datetime.strptime(input_year, "%Y-%m-%d %H:%M:%S")
            task1.start_date = syear
            task1.add_history(username,f'start time changed to {task1.start_date}.')

        except Exception as e:
            error_logger.error(f"error : {e} ")
            print (f"time data {input_year} does not match format '%Y-%m-%d %H:%M:%S' \nor invalid date.")
        finally:
            print (task1.start_date)
        #end
        try: #does not match format
            input_year = input(f'Enter your Date to end: (e.g. { task1.last_date })')
            syear = dt.datetime.strptime(input_year, "%Y-%m-%d %H:%M:%S")
            task1.last_date = syear
            task1.add_history(username,f'end of time changed to {task1.last_date}.')

        except Exception as e:
            error_logger.error(f"error : {e} ")
            print (f"time data {input_year} does not match format '%Y-%m-%d %H:%M:%S' \nor invalid date.")
        finally:
            print (f'new date: {task1.last_date}')
        edit_task_member (task1, project, username)
        return

    elif k == '4':
        print(task1.priority)
        n = input('1.CRITICAL\n2.HIGH\n3.MEDIUM\n4.LOW(default)\n')
        if n.isdigit() and 0 < int(n) < 5:
            task1.priority = task1.degr[int(n)-1]
            task1.add_history(username,f'priority changed to {task1.priority}.')
        else:
            print('invalid number')
        edit_task_member (task1, project, username)
        return

    elif k == '5':
        print(task1.status)
        n = input('1.BACKLOG(default) \n2.TODO \n3.DOING \n4.DONE \n5.ARCHIVED\n')
        if n.isdigit() and 0 < int(n) < 6:
            task1.status = task1.statuses[int(n)-1]
            task1.add_history(username,f'priority changed to {task1.priority}.')
        else:
            print('invalid number')
        edit_task_member (task1, project, username)
        return

    elif k == '6':
        
        with open ('projects/' + ID + '.json') as file:
            information = eval(file.read())
        print(f"project members: {information['Members']}")
        print(f'task members: {task1.members}')
        if username == information['Leader']:
            name = input('Enter member: ')
            if name in information['Members']:
                if name not in task1.members:
                    task1.members.append(name)
                    task1.add_history(username,f'{name} added to project.')

                else:
                    print(f'{name} is already here.')
            else:
                print('user is not member of project.')
        else:
            print("you ara not leader in the project.",
             "you can't add members.")
        edit_task_member (task1, project, username)
        return

    elif k == '7':
        print(task1.add_comment)
        comment = input('Enter your comment: ')
        task1.add_comment(username, comment)
        task1.add_history(username,f'new comment: {comment}.')
        edit_task_member (task1, project, username)
        return
    
    elif k == '8':
        task_item = {
            "ID" : str(task1.ID),
            "Title" : task1.name,
            "Description" : task1.description,
            "Start Date" : str(task1.start_date),  
            "End Date" : str(task1.last_date),
            "priority" : task1.priority,
            "Status" : task1.status,
            "Members" : task1.members,
            "Comments" : task1.comments,
            "History" : task1.history
        }
        print(task_item)
        edit_task_member (task1, project, username)
        return
    elif k == '9':
        return
    else:
        print("I didn't understand! What should I do?")
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


#show
def show_projects(username, c): #c = leader (1) or member (2)
    information = decrypt_user_info(username)
    if c == '2':
        id_lst = information['projects_Leader']
    elif c == '3':
        id_lst = information['projects_Member']
    else:
        print("I didn't understand!")
        return
    table = Table(title="All Projects")
    table.add_column("row", justify="right", style="green")
    table.add_column("ID", justify="right", style="cyan")
    table.add_column("Title", justify="right", style="yellow")
    id_i = {}
    try: # error in open file
        for i , ID in enumerate(id_lst):
            with open('projects/' + ID + '.json', 'r') as file:
                info = json.load(file)
            table.add_row(str(i+1), ID, info["Title"])
            id_i[str(i+1)] = ID
        print(table)
        i = input(Text('Choose number to show details(or -1 to exit): ', 'red'))
        if i.isdigit() and 0 < int(i) < (len(id_i) + 1) :
            with open ('projects/' + id_i[i] + '.json') as file:
                info = eval(file.read())
            project = info_to_obj_proj(info)
            if username == project.Leader:
                edit_projet_leader(project, username)
            else:
                edit_project(project, username)
            show_projects(username, c)
        else:
            Account_page(username)
    except Exception as e:
        error_logger.error(f"error : {e} ")
        print('Sorry! Project not found.')
        Account_page(username)

def show_tasks(ID):
    table = Table(title="All Tasks")

    table.add_column("BACKLOG", justify="right", style="cyan")
    table.add_column("TODO", style="magenta")
    table.add_column("DOING", justify="right", style="yellow")
    table.add_column("DONE", justify="right", style="red")
    table.add_column("ARCHIVED", justify="right", style="green")

    tasks_by_status = {
        "BACKLOG" : [],
        "TODO" : [],
        "DOING" : [],
        "DONE" : [],
        "ARCHIVED" : []
    }
    with open ('projects/' + ID + '.json', 'r') as file:
        project = eval(file.read())
    tasks = project['Tasks'] #dict of tasks
    id_i = {}
    for i , ID in zip(range(len(tasks)), tasks.keys()):
        tasks_by_status[tasks[ID]['Status']].append(str(i+1) + '.' + tasks[ID]['Title'])
        id_i[str(i+1)] = ID

    lst = [] #columns
    for status in tasks_by_status.values():
        column = '\n'.join(status) #Write the names of the projects below
        lst.append(column)
    table.add_row(*lst)
    console = Console()
    console.print(table)

    i = input('Choose number to show details(or -1 to exit): ')
    if i == '-1':
        return
    elif i.isdigit() & 0 < int(i) < len(id_i) + 1 :
        task = tasks[id_i[i]]
        table2 = Table(title=task['Title'])
        Values = []
        for j in tasks[id_i[i]].keys():
            if j != "Members" and j != "Comments" and j !="History":
                table2.add_column(j, style="green")
                Values.append(task[j])
        table2.add_row(*Values)
        print(table2) 
        print (f"Members: {task["Members"]}" ,
        f"Comments: {task["Comments"]}" ,
        f"History: {task["History"]}")
    else:
        print('incorrect number!')
        menu()


#pages
def menu():
    # os.system('cls')
    from rich.text import Text
    from rich.console import Console
    console = Console()
    panel = Panel(Text('1. create account\n2. sign in \n3. sign in as admin', 'green',justify="left")) 
    k = console.input(panel)
    if k == '1':
        create_acount()
        return
    elif k == '2':
        from rich.console import Console
        from rich.text import Text
        console = Console()
        username = console.input(Text("Enter username: ","bold green"))
        password = console.input(Text("Enter password: ","bold green"))
        sign_in(username, password)
        return
    elif k == '3':
        username = console.input(Text("Enter username: ","bold green"))
        password = console.input(Text("Enter password: ","bold green"))
        sign_in_admin(username, password)
    else:
        print("I didn't understand! (Enter 1 or 2 or 3!)\n")
        menu()

def Account_page(username):
    panel = Panel(Text(f'WELCOME {username}! \n1. create project\n2. leader projects\n3. user projects\n4. sign out',"bold yellow", justify="left"))
    print(panel)
    k = input()
    if k == '1':
        create_project(username)
        return
    elif k == '2' or k == '3':
        show_projects(username, k)
        return
    elif k == '4':
        menu()
        return

def Account_page_admin(username):
    print(Panel(Text(f'Welcome {username}!\n1.Inactive users \n2.Delete all data' , 'bold magenta')))
    k = input()
    if k == '1':
        username = input(Text('Enter a usernamt to inactive: ' , 'green'))
        information = decrypt_user_info(username)
        information['active'] = "Inactive"
        encrypt_user_info(username, information)
        print(Text(f'User {username} Inactived.' , 'bold red'))
    elif k == '2':
        n = input(Text("All data will be delete; Are you sure? (1.yes)"))
        if n == '1':
            if os.path.exists("data/Users.json"):
                os.remove("data/Users.json")
            if os.path.exists("data/Admin.json"):
                os.remove("data/Admin.json")
            if os.path.exists("data/ID.json"):
                os.remove("data/ID.json")

            if os.path.isdir("users"):
                shutil.rmtree('users')
                shutil.rmtree('users', ignore_errors=True)
            if os.path.isdir("projects"):
                shutil.rmtree('projects')
                shutil.rmtree('projects', ignore_errors=True)
            if os.path.isdir("data"):
                shutil.rmtree('data')
                shutil.rmtree('data', ignore_errors=True)

menu()

