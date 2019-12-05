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
        self.credited_courses = set()

    def __str__(self):
        return self.first+'\t'+self.last+'\t\t'+str(self.id)+'\tStudent\t'+self.college+'\t'+self.course

    def enlist(self, course):
        if course.currsize < course.size:
            if course.get_diff(self.credited_courses):
                self.cart.add(course)
                course.add_student(self)
            else:
                print("You must take the prerequisites first")
        else:
            print("Course is already full")

    def drop(self, code):
        for c in self.cart:
            if c.code == code:
                self.cart.remove(c)
                c.remove_student(self)
                break
    def credit(self, code):
        self.credited_courses.add(code)

class Admin(User):
    def __init__(self, first, last, id, password):
        super().__init__(first, last, id)
        self.password = password
    def __str__(self):
        return self.first+'\t'+self.last+'\t\t'+str(self.id)+'\tAdmin'

    def add_course(self, name, code, units, size):
        temp = Course(name, code, units, size)
        courses.add(temp)

    def remove_course(self, code):
        for c in courses:
            if c.code == code:
                courses.remove(c)
                break

class Course:
    def __init__(self, name, code, units, size):
        self.name = name
        self.code = code
        self.units = units
        self.size = size
        self.currsize = 0
        self.classlist = set()
        self.prereqs = set()

    def __str__(self):
        return "{}\t{}\t\t{}\t{}/{}\t\t{}".format(self.code,self.name,self.units,self.currsize,self.size,','.join(self.prereqs))
    # Adds student to the class
    def add_student(self, student):
        self.classlist.add(student)
        self.currsize += 1
    # Removes student to the class
    def remove_student(self, student):
        self.classlist.remove(student)
        self.currsize -= 1
    # Adds a prerequisite
    def add_prereq(self, code):
        self.prereqs.add(code)
    # Adds a prerequisite
    def remove_prereq(self, code):
        self.prereqs.remove(code)
    def get_diff(self, credited_courses):
        diff = self.prereqs.difference(credited_courses)
        if len(diff) > 0:
            return False
        else:
            return True
# Prints out all courses available
def view_courses():
    print(">>>>\tCourse Directory\t<<<<")
    print("Code\tCourse Name\tUnits\tCapacity\tPrerequisites")
    if (len(courses) == 0):
        print("\t\tEMPTY\t\t")
    else:
        for c in courses:
            print (c)

#Returns a course given the code
def get_course(code):
    for c in courses:
        if c.code == code:
            return c

# Retrieve a user from the users set
def get_user(id):
    for p in users:
        if p.id == id:
            return p
# Allows student to view all courses and add it
def add_menu(user):
    view_courses()
    # Admin users add to course offerings
    if isinstance(user, Admin):
        name = input("Enter course name\t: ")
        code = input("Enter course code\t: ")
        units = int(input("Enter course units\t: "))
        size = int(input("Enter course capacity\t: "))
        user.add_course(name,code,units,size)
    # Student users add to cart
    else:
        view_cart(user)
        code = input("Please type the course code to add\t: ")
        course = get_course(code)
        user.enlist(course)

# Allows student to view all courses in cart
def view_cart(student):
    print(">>>>\tShopping Cart\t<<<<")
    sum = 0
    if (len(courses) == 0):
        print("\t\tEMPTY\t\t")
    else:
        for c in student.cart:
            print(c)
            sum += c.units
        print("Total Units\t: ", sum)
# Allows student to view enlisted courses and remove them
def drop_menu(user):
    # Admin users add to course offerings
    if isinstance(user, Admin):
        view_courses()
        code = input("Please enter course code to be removed\t: ")
        user.remove_course(code)
    # Student users add to cart
    else:
        view_cart(user)
        code = input("Please enter course code to be removed\t: ")
        user.drop(code)
# Adds a prereq code of a coures
def add_course_prereq(admin):
    view_courses()
    code = input("Please enter course code to add a prereq\t: ")
    course = get_course(code)
    prereq_code = input("Please enter the prereq course code\t: ")
    if prereq_code != code:
        course.add_prereq(prereq_code)
# Removes prereq code of a course
def remove_course_prereq(admin):
    view_courses()
    code = input("Please enter course code to add a prereq\t: ")
    course = get_course(code)
    if (len(course.prereqs) != 0):
        prereq_code = input("Please enter the prereq course code\t: ")
        if prereq_code != code:
            course.remove_prereq(prereq_code)
    else:
        print("Nothing to remove")
# Allows student to add course code to be credited (for prereq)
def credit_course(student):
    view_courses()
    code = input("Please enter course code to credit\t: ")
    student.credit(code)
# Registration page
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

# Show all users registered
def view_users():
    print(">>>>\tUser Directory\t<<<<")
    print("First\tLast\t\tID\tRole\tCollege\tCourse")
    if len(users) == 0:
        print("\t\tEMPTY\t\t")
    else:
        for p in users:
            print(p.__str__())
# Allows navigation to add, drop, and view menu
def student_menu(id):
    student = get_user(id)
    while True:
        try:
            print(">>>>\tStudent Dashboard\t<<<<")
            choice = int(input("[1] Add a course\n[2] Drop a course\n[3] View cart\n" +
            "[4] Credit a course\n[5] Logout\n"))

            if choice >= 1 and choice <= 5:
                break;
            else:
                print("Not an option")
        except ValueError:
                print("This is not a valid number.")

    if choice == 1:
        add_menu(student)
        student_menu(id)
    elif choice == 2:
        drop_menu(student)
        student_menu(id)
    elif choice == 3:
        view_cart(student)
        student_menu(id)
    elif choice == 4:
        credit_course(student)
        student_menu(id)
    else:
        MainMenu()

# Allows navigation to add, drop, and view menu
def admin_menu(id):
    admin = get_user(id)
    while True:
        try:
            print(">>>>\tAdmin Settings\t<<<<")
            choice = int(input("[1] Add a course\n[2] Remove a course\n[3] View Courses\n[4] View Users\n"
                    + "[5] Add course prerequisite\n[6] Remove course prerequisite\n[7] Logout\n"))
            if choice >= 1 and choice <= 7:
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
    elif choice == 5:
        add_course_prereq(admin)
        admin_menu(id)
    elif choice == 6:
        remove_course_prereq(admin)
        admin_menu(id)
    else:
        MainMenu()
# Checks if admin password is correct
def checkPassword(admin, password):
    if admin.password == password:
        return True
    else:
        return False

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
            # Only allow student users to access student Dashboard
            if isinstance(get_user(id), Student):
                student_menu(id)
            elif isinstance(get_user(id), Admin):
                print("Sorry! You are not a student user. Please log in again.")
                MainMenu()
            else:
                print("Oops! You're not registered yet.\nLet's create an account!")
                createAcct(id, userType)
                MainMenu()
        except ValueError:
            print("This is not a valid number.")
    else:
        try:
            id = int(input("Enter employee ID\t: "))
            # Only allow admin users to access Admin Settings
            if isinstance(get_user(id), Admin): #
                password = input("Enter passkey\t: ")
                if checkPassword(get_user(id),password):
                    admin_menu(id)
                else:
                    print("Wrong passkey.")
                    MainMenu()
            elif isinstance(get_user(id), Student):
                print("Sorry! You are not an admin user. Please log in again.")
                MainMenu()
            else:
                print("Oops! You're not registered yet.\nLet's create an account!\n")
                createAcct(id, userType)
                MainMenu()
        except ValueError:
            print("This is not a valid number.")
MainMenu()
