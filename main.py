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
console = Console()

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
                    self.add_member(username, file)
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


#Tools
def decrypt_user_info(username):
    with open("mykey.key", 'rb') as mykey: #receive key 
        key = mykey.read()
        f = Fernet(key)
    with open('users/' + username + '.json', 'rb') as encrypted_file: #receive user information 
        encrypted = encrypted_file.read()
    try: #file is empty
        decrypted = f.decrypt(encrypted) #decryption
        information = eval(decrypted.decode()) #byte to str to dict
        return information
    except:
        print(Text('Sorry! something went wrong. \nyou should sign up again :(', 'red'))
        menu()

def encrypt_user_info(username, info):
    with open("mykey.key", 'rb') as mykey: #receive key 
        key = mykey.read()
        f = Fernet(key)
    with open('users/' + username + '.json', 'wb') as file:
        encrypted = f.encrypt((str(info)).encode())
        file.write(encrypted)

def info_to_obj_task(task_item): #info = json / task
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

def info_to_obj_proj(info): #info = json / proj
    project1.ID = info['ID']
    project1.Leader = ['Leader']
    project1.Title = ['Title']
    project1.Users = ['Members']
    project1.Field = ['Tasks']
    return project1



def sign_in (username, password):
    #decryption
    if os.path.exists('users/' + username + ".json"):
        information = decrypt_user_info(username)
        if information['password'] == password: #check password
            if information["active"] == 'Active':
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

    #create user file
    item = {"Email" : User1.Email , "username" : User1.username , "password" : User1.password , "active" : User1.active}
    if not os.path.exists('mykey.key'): #create key & save
        key = Fernet.generate_key()
        with open('mykey.key', 'wb') as mykey:
            mykey.write(key)
    encrypt_user_info(User1.username, item)
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
        information = decrypt_user_info(user)
        if user != username:
            information['projects_Memder'].append(project1.ID)
        else:
            information['projects_Leader'].append(project1.ID)
        print(information)
        encrypt_user_info(user, information)
        user = input('Invite users to this project.\nEnter username or 1 to end: ') #Add Users
    
    # Save Project
    information = {
        'ID' : project1.ID,
        'Leader' : project1.Leader,
        'Title' : project1.Title,
        'Members' :  project1.Users,
        'Tasks' : project1.tasks_dict
        }
    print(information)
    with open('projects/' + project1.ID + '.json', 'w') as file:
        json.dump(information, file, indent=4)   

    Account_page(username)


def edit_projet():
    pass

def edit_task_member (task1, ID, username):
    print(Text('task is created. you can change the details.' , 'blue'), 
    Panel('1.title'+ '\n' '2.description' + '\n' '3.start & end time' + '\n'
    '4.change priority (CRITICAL, HIGH, MEDIUM, LOW(default)' + '\n'
    '5.change status (BACKLOG(default), TODO, DOING, DONE, ARCHIVED)'+ '\n'
    '6.give to members' + '\n' '7.add comment' + '\n' + '8.Show details'
     + '\n' + '9.exit'))
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
        with open ('projects/' + ID + '.json', 'r') as file:
            information = eval(file.read())
        print(information["Tasks"])
        edit_task_member (task1, ID, username)
        return
    elif k == '9':
        return
    else:
        print("I didn't understand! What should I do?")

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

    edit_task_member(task1, ID, username)

def show_projects(username, c): #c = leader (1) or member (2)
    information = decrypt_user_info(username)
    if c == '2':
        lst = information['projects_Leader']
    elif c == '3':
        lst = information['projects_Member']
    else:
        print("I didn't understand!")
        return
    for i in lst:
        with open('projects/' + i + '.json', 'r') as file:
            print(file.read())


    # print(information["Tasks"])
    # if username in information['Members']:
    #    pass 
    # else:
    #     print('You are not member')

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
        id_i[i] = ID

    lst = [] #columns
    for status in tasks_by_status.values():
        column = '\n'.join(status)
        lst.append(column)
    table.add_row(lst[0],lst[1],lst[2],lst[3],lst[4])
    console = Console()
    console.print(table)

    i = input('Choose number to show details(or -1 to exit): ')
    if i == '-1':
        pass
        Account_page(username)
        return
    elif i.isdigit():
        task = tasks[id_i[i]]
        table2 = Table(title=task['Title'])
        Values = []
        for j in tasks[id_i[i]].keys():
            if j != "Members" or j != "Comments" or j !="History":
                table2.add_column(j, style="green")
                Values.append(task[j])
        table2.add_row(*Values)
        print(table2) 
        print (f"Members: {task["Members"]}" ,
        f"Comments: {task["Comments"]}" ,
        f"History: {task["History"]}")

def menu():
    # os.system('cls')
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
    else:
        print("I didn't understand! (Enter 1 or 2!)\n")
        menu()


def Account_page(username):
    panel = Panel(Text(f'WELCOME {username}! \n1. create project\n2. leader projects\n3. user projects',"bold yellow", justify="left"))
    print(panel)
    k = input()
    if k == '1':
        create_project(username)
    elif k == '2' or k == '3':
        show_projects(username, k)



menu()