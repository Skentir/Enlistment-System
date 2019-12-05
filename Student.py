# Kirsten Sison
import sys

users = set() # set of users registered
courses = set() # set of courses available

class User:
    def __init__(self, first, last, id):
        self.id = id
        self.first = first
        self.last = last

class Student(User):
    def __init__(self, first, last, id, college, course):
        super().__init__(first, last, id)
        self.cart = set()
        self.college = college
        self.course = course

    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    def enlist(self, course):
        cart.add(course)

class Admin(User):
    def __init__(self, first, last, id, password):
        super().__init__(first, last, id)
        self.password = password

    def add_course(self, name, code, units):
        temp = Course(name, code, units)
        courses.add(temp)

    def remove_course(self, code):
        for c in courses:
            if c.code == code:
                courses.remove(c)


class Course:
    def __init__(self, name, code, units):
        self.name = name
        self.code = code
        self.units = units
    def info(self):
        return '{} {} {}'.format(self.code,"\t\t", self.name,"\t\t", self.units)

# Prints out all courses available
def view_courses():
    print(">>>>\tCourse Directory\t<<<<")
    print("Code\t\tCourse Name\t\tUnits")
    for c in courses:
        Course.info(c)

#Returns a course given the code
def get_course(code):
    for c in courses:
        if c.code == code:
            return c
# Allows student to view all courses and add it
def add_menu(user):
    view_courses()
    # Admin users add to course offerings
    if isinstance(user, Admin):
        name = input("Enter course name\t: ")
        code = input("Enter course code\t: ")
        units = input("Enter course units\t: ")
        user.add_course(name,code,units)
    # Student users add to cart
    else:
        view_cart()
        code = input("Please type the course code to add\t: ")
        course = get_course(code)
        user.enlist(course)

def view_cart(student):
    print(">>>>\tShopping Cart\t<<<<")
    sum
    for c in student.courses:
        Course.info(c)
        sum += c.units
    print("Total Units\t: ", sum)
# Allows student to view enlisted courses and remove them
# TODO: Delete course from Student's course set
def drop_menu(student):
    view_cart(student)
# Checks if the user is already registered
def findUser(id):
    for p in users:
        if (p.id == id):
            return True
    return False

def createAcct(id, type):
    fname = input("Enter first name\t: ")
    lname = input("Enter last name\t: ")
    if type == 1:
        college = input("Enter college\t: ")
        course = input("Enter course\t: ")
        temp = Student(fname,lname,id,college,course)
        users.add(temp)
    else:
        password = input("Enter a pass key\t: ")
        temp = Admin(fname,lname,id,password)
        users.add(temp)
# Retrieve a user from the users set
def get_user(id):
    for p in users:
        if p.id == id:
            return p
def view_users():
    print(">>>>\tUser Directory\t<<<<")
    print("First\t\tLast\t\tID\t\tRole")
    for p in users:
        if isinstance(p, Admin):
            print(p.first,"\t\t", p.last,"\t\t", p.id,"\t\tAdmin")
        else:
            print(p.first,"\t\t", p.last,"\t\t", p.id,"\t\tStudent\n")
# Allows navigation to add, drop, and view menu
def student_menu(id):
    student = get_user(id)
    while True:
        try:
            print(">>>>\tStudent Dashboard\t<<<<")
            choice = int(input("[1] Add a course\n[2] Drop a course\n[3] View cart\n[4] Logout\n"))

            if choice >= 1 and choice <= 4:
                break;
            else:
                print("Not an option")
        except ValueError:
                print("This is not a valid number.")

    if choice == 1:
        add_menu(student)
    elif choice == 2:
        drop_menu(student)
    elif choice == 3:
        view_cart(student)
    else:
        MainMenu()

# Allows navigation to add, drop, and view menu
def admin_menu(id):
    admin = get_user(id)
    while True:
        try:
            print(">>>>\tAdmin Settings\t<<<<")
            choice = int(input("[1] Add a course\n[2] Remove a course\n[3] View Courses\n[4] View Users\n[5] Logout\n"))
            if choice >= 1 and choice <= 5:
                break;
            else:
                print("Not an option")
        except ValueError:
                print("This is not a valid number.")


    if choice == 1:
        add_menu(admin)
        admin_menu(id)
    elif choice == 2:
        drop_menu(admin)
        admin_menu(id)
    elif choice == 3:
        view_courses()
        admin_menu(id)
    elif choice == 4:
        view_users()
        admin_menu(id)
    else:
        MainMenu()


def MainMenu():
    print("\n>>>>\tWelcome to AnimoSys!\t<<<<\n")

    while True:
        try:
            login = int(input("[1] Log In or [2] Exit?\t: "))

            if login == 1:
                break;
            elif login == 2:
                sys.exit()
            else:
                print("Number not a choice.")
        except ValueError:
                print("This is not a valid number.")

    while True:
        try:
            userType = int(input("[1] Student or [2] Admin?: "))

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
                student_menu(id)
            else:
                print("Oops! You're not registered yet.\nLet's create an account!")
                createAcct(id, userType)
                MainMenu()
        except ValueError:
            print("This is not a valid number.")
    else:
        try:
            id = int(input("Enter employee ID\t: "))
            exists = findUser(id)
            # Check if Admin exists
            if exists:
                admin_menu(id)
            else:
                print("Oops! You're not registered yet.\nLet's create an account!\n")
                createAcct(id, userType)
                MainMenu()
        except ValueError:
            print("This is not a valid number.")
MainMenu()
