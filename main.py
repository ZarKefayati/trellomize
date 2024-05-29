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
    os.system('cls')
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






show_projects('zark2', '2')

create_project (username)
menu()


