import uuid
import datetime as dt
import enum as en

class priority(en.Enum):
    crit = "CRITICAL"
    high = "HIGH"
    medium = "MEDIUM"
    low = "LOW"
        
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
        self.position=("BACKLOG" , "TODO" , "DOING" , "DONE" , "ARCHIVED") 
        if status in self.position:
            self.position = status 

        self.history = [] 
        self.comments = []

    def add_history(self, user, change_assiAssignees, change_priority, change_status):
        self.history.append({'user':user,'change_in_assiAssignees':change_assiAssignees, 'change_in_priority':change_priority,'change_in_status':change_status, 'timestamp':dt.now()})

    def add_comment(self, username, comment):
        self.comments.append({'username':username,'comment':comment,'start_date':dt.now()})
    
    def __repr__(self):
        return (f"Task(id={self.uniq_id}, title={self.task_name}, start_date={self.start_date}", 
                f"end_date={self.last_date}, "
                f"history={self.history}, comments={self.comments}")

task_name=input("name of project: ")
task_description=input("name of discription: ")


t=Tasks()

class Project:
    def __init__(self):
        self.tasks_dict = {}
        self.members_set = set() # assignees  


    def add_member(self, name):
        self.members_set.append(name)

    def adds_task(self, task_name, member_name):
        if member_name in self.members_set:
            self.tasks_dict[task_name] = member_name
            print(f" task of '{task_name}' give to '{member_name}' ")
        else:
            print(f" no any person of '{member_name}'")

    def delet_task(self, task_name, member_name):
        if member_name in self.members_set:
            del_task=self.tasks_dict.pop(task_name)
            print(f" task of '{task_name}' delet of '{member_name}' ")
        else:
            print(f" no any person of '{member_name}'")
        
        
    def Assignees(self):
        for t, m in self.tasks_dict.items():
            print(f"this task : {m} is to : {t}") #can use new file


m = Project()
m.add_member('Zahra')
m.add_member('Ali')
m.adds_task('frontend', 'Ali')
m.adds_task('backend' ,'Zahra')
m.show_tasks()

t = Tasks("com" , "HIGH")
p =Project()
p.add_member("Fat")
p.adds_task(t,"Fat")

