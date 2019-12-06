# Title: AnimoSys Enlistment Platform
# Language: Python
# Created by Kirsten Sison
# Finished in Dec 5, 2019 as Term 1 Project for DLSU COMET
import sys

users = set() # set of users registered
courses = set() # set of courses available
# I used set as the data structure for courses and students because of the ff.
# 1. Sets doesn't allow duplicates, saving me from more lines of code for validation had I used a List.
#   Besides, every student/employee ID and course object is unique and cannot have a clone.
# 2. Set operations prove to be useful especially when checking for requirements. In example, I used
#   set difference to easily check whether the prerequisites exist in the credited courses of the student!
#   This can also be utilized further had I implemented a basic Analytics tool for the Admin.
# 3. It's faster compared to a List since Set is implemented with a Hash Table in Python!

class User:
    def __init__(self, first, last, id):
        self.id = id
        self.first = first
        self.last = last

class Student(User):
    def __init__(self, first, last, id, college, course):
        super().__init__(first, last, id)
        self.cart = set()   # shopping cart
        self.college = college
        self.course = course
        self.credited_courses = set()

    def __str__(self):
        return self.first+'\t'+self.last+'\t\t'+str(self.id)+'\tStudent\t'+self.college+'\t'+self.course
    # Add course object to shopping cart
    def enlist(self, course):
        if course.currsize < course.size:
            if course.get_diff(self.credited_courses): # All prerequisites must exist in the credited courses of the student
                self.cart.add(course)
                course.add_student(self)
            else:
                print("You must take the prerequisites first")
        else:
            print("Course is already full")
    # Remove course object from shopping cart
    def drop(self, code):
        for c in self.cart:
            if c.code == code:  # Drop vourse if it's in the student's shopping cart
                self.cart.remove(c)
                c.remove_student(self)
                break
    # Add course code to credited courses
    def credit(self, code):
        self.credited_courses.add(code) # Adds a course code to the credited course set

class Admin(User):
    def __init__(self, first, last, id, password):
        super().__init__(first, last, id)
        self.password = password

    def __str__(self):
        return self.first+'\t'+self.last+'\t\t'+str(self.id)+'\tAdmin'
    # Adds course object to set of course offerings
    def add_course(self, name, code, units, size):
        courses.add(Course(name, code, units, size))
    # Removes a course object from the set of course offerings
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
    # Checks if student has the prerequisites required (done by set difference)
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
        print("Code\tCourse Name\tUnits\tCapacity\tPrerequisites")
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
        users.add(Student(fname,lname,id,college,course))
    else:
        password = input("Enter a pass key\t: ")
        users.add(Admin(fname,lname,id,password))

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
            print("٩꒰｡•‿•｡꒱۶\tStudent Dashboard\t٩꒰｡•‿•｡꒱۶")
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
            print("꒰●꒡ ̫ ꒡●꒱>>\tAdmin Settings\t<<꒰●꒡ ̫ ꒡●꒱")
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
                print("This is not a valid number. (⌯⊙⍛⊙)")

    while True:
        try:
            userType = int(input("[1] Student or [2] Admin?: "))

            if userType == 1 or userType == 2:
                print("Please login with your credentials.")
                break;
            else:
                print("Number not a choice.")
        except ValueError:
                print("This is not a valid number. (⌯⊙⍛⊙)")

    # Student module
    if userType == 1:
        try:
            id = int(input("Enter ID number\t: "))
            # Only allow student users to access student Dashboard
            if isinstance(get_user(id), Student):
                student_menu(id)
            elif isinstance(get_user(id), Admin):
                print("Sorry! You are not a student user. Please log in again. ٩꒰• ε •꒱۶⁼³")
                MainMenu()
            else:
                print("Oops! You're not registered yet.\nLet's create an account!(=^-ω-^=)")
                createAcct(id, userType)
                MainMenu()
        except ValueError:
            print("This is not a valid number. (⌯⊙⍛⊙)")
    else:
        try:
            id = int(input("Enter employee ID\t: "))
            # Only allow admin users to access Admin Settings
            if isinstance(get_user(id), Admin): #
                password = input("Enter passkey\t: ")
                if checkPassword(get_user(id),password):
                    admin_menu(id)
                else:
                    print("Wrong passkey. └༼ •́ ͜ʖ •̀ ༽┘")
                    MainMenu()
            elif isinstance(get_user(id), Student):
                print("Sorry! You are not an admin user. Please log in again. ٩꒰• ε •꒱۶⁼³")
                MainMenu()
            else:
                print("Oops! You're not registered yet.\nLet's create an account!(=^-ω-^=)\n")
                createAcct(id, userType)
                MainMenu()
        except ValueError:
            print("This is not a valid number.(⌯⊙⍛⊙)")
MainMenu()
