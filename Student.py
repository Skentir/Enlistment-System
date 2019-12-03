# Kirsten Sison

class User:
    def __init__(self, first, last, id):
        self.username = id
        self.first = first
        self.last = last

class Student(User):
    def __init__(self, first, last, id, college, course):
        super().__init__(self, first, last, id)
        courses = set()
        self.id = id
        self.college = college
        self.course = course

    def fullname(self):
        return '{} {}'.format(self.first, self.last)

class Admin(User):
    def __init__(self, first, last, id, password):
        super().__init__(self, first, last, id)
        self.password = password

class Course:
    def __init__(self, name, code, units):
        self.name = name
        self.code = code
        self.units = units

def findUser(code):
    for p in users:
        if (p.username == code):
            return True
    return False

def createAcct(code, type):
    fname = input("Enter first name\t: ")
    lname = input("Enter last name\t: ")
    if type == 1:
        college = input("Enter college\t: ")
        course = input("Enter course\t: ")
        temp = Student(fname,lname,code,college,course)
        users.add(temp)
    else:
        password = input("Enter a pass key\t: ")
        temp = Admin(fname,lname,code,password)
        users.add(temp)


def Menu(student):
    print("[1] Add a course\n[2] Drop a course\n[3] View cart\n")

# s1 = Student('Kirsten', 'Smith', '11898754','CCS')
# print(Student.fullname(s1))
users = set()
def MainMenu():
    print(">>>>\tWelcome to AnimoSys!\t<<<<\n")
    while True:
        try:
            userType = int(input("[1] Student or [2] Admin?\t: "))

            if userType == 1 or userType == 2:
                print("Please login with your credentials.")
                break;
            else:
                print("Number not a choice.")
        except ValueError:
                print("This is not a valid number.")

    # Student module
    if userType == 1:
        try:
            id = int(input("Enter ID number\t: "))
            exists = findUser(id)
            # Check if Student exists
            if exists:
                launch_menu()
            else:
                print("Oops! You're not registered yet.\nLet's create an account!\n")
                createAcct(id, userType)
        except ValueError:
            print("This is not a valid number.")
    else:
        try:
            id = int(input("Enter employee ID\t: "))
            exists = findUser(id)
            # Check if Admin exists
            if exists:
                launch_menu(id)
            else:
                print("Oops! You're not registered yet.\nLet's create an account!\n")
                createAcct(id, userType)
        except ValueError:
            print("This is not a valid number.")
MainMenu()
