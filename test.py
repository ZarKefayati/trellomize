from rich import print
from rich.table import Table
from rich.console import Console
import os



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
tasks = {
    '11' : {
        'Status' : 'BACKLOG',
        'Title' : 'start'
    },

    '22' : {
        'Status' : 'BACKLOG',
        'Title' : 'start2'
    },

    '33' : {
        'Status' : 'DONE',
        'Title' : 'start3'
    },

    '44' : {
        'Status' : 'TODO',
        'Title' : 'start'
    }
}

id_i = {}


for i , ID in zip(range(len(tasks)), tasks.keys()):
    tasks_by_status[tasks[ID]['Status']].append(str(i+1) + '.' + tasks[ID]['Title'])
    id_i[str(i+1)] = ID

lst = []
for status in tasks_by_status.values():
    column = '\n'.join(status)
    lst.append(column)
table.add_row(*lst)
console = Console()
console.print(table)

i = input('Choose number to show details(or -1 to exit): ')
if i == '-1':
    pass
    # Account_page(username)
    # return
elif i.isdigit():
    task = tasks[id_i[i]]
    table2 = Table(title=task['Title'])
    Values = []
    for j in tasks[id_i[i]].keys():
        table2.add_column(j, style="green")
        Values.append(task[j])
    table2.add_row(*Values)
    print(table2)
