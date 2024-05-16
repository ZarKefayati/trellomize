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

User1 = User("", "", "", "Active")
User1.Email = input('Enter your Email: ')
file = open("Users.txt" , 'a+')

User1.setUsername(input('Enter a username: ') , file)
User1.password = input('Enter your password: ')
file.write('\n' + User1.username)
file.close()

file = open(User1.username+".txt" , 'w')
file.write(User1.Email + '\n' + User1.username + '\n' +  User1.password + '\n' + User1.active + '\n')
file.close()