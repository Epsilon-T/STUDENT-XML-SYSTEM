from xml.dom import minidom

target_file = 'student.xml'
docs = minidom.parse(target_file)

def load_xml():
    return minidom.parse(target_file)

def save_xml(document):
    with open(target_file, "w") as f:
        f.write(document.toprettyxml())

def student_interface():
    print("==== STUDENT XML SYSTEM ====")
    print("1 - Add Student")
    print("2 - Display Report")
    print("3 - Update Student")
    print("4 - Delete Student")
    print("5 - Exit")

    user_input = input("Enter Choice: ")
    if user_input == "1":
        return addStudent()
    elif user_input == "2":
        return displayStudents()
    elif user_input == "3":
        return updateStudent()
    elif user_input == "4":
        return deleteStudent()
    elif user_input == "5":
        print("Thank you for using the STUDENT XML SYSTEM")
        return None # This breaks the loop inside the function
    else:
        print("Error: invalid choice")
        return student_interface()

def displayStudents():
    students = docs.getElementsByTagName("student")
    load_xml()   # this just updates the current function to latest file.xml
    course_list = []  # stores the course once for each courses
    all_courses_list = []  # stores all the courses

    print("ID  NAME            Course")
    print("---------------------------------")
    for student in students:
        student_id = student.getAttribute("id")
        student_name = student.getElementsByTagName("name")[0].firstChild.data
        student_course = student.getElementsByTagName("course")[0].firstChild.data
        courses = student.getElementsByTagName("course")
        for course in courses:
            current = course.firstChild.data
            all_courses_list.append(current)
            if current not in course_list:
                course_list.append(current)


        print(f"{student_id :<3} {student_name :<15} {student_course}")
    print("\nStudent Count per Course")

    for i in range(0, len(course_list)):    # This is for that dynamic courses output
        count = 0
        for j in range(0, len(all_courses_list)):
            if course_list[i] == all_courses_list[j]:
                count += 1
        print(f"{course_list[i]}: {count}")
    return student_interface()

def addStudent():
    students = docs.getElementsByTagName("student")
    found = False

    input_id = input("Enter Student ID: ")
    for student in students:
        student_id = student.getAttribute("id")
        if input_id.strip() == "".strip():  # Added a handler that checks if the input is blank
            print("Error: ID cannot be blank")
            print("Rolling back to STUDENT XML SYSTEM")
            return student_interface()
        elif input_id in student_id:
            found = True
    if found:
        print("Error: Student ID already Exist. Cannot add duplicate")
        print("Rolling back to STUDENT XML SYSTEM")
        return student_interface()

    name_input = input("Enter name: ")
    course_input = input("Enter course: ")

    # Error handling if one or both inputs are blank
    if name_input.strip() == "".strip() and course_input.strip() == "".strip():
        print("Error: name and course cannot be blank")
        print("Rolling back to STUDENT XML SYSTEM")
        return student_interface()
    elif name_input.strip() == "".strip():
        print("Error: name cannot be blank")
        print("Rolling back to STUDENT XML SYSTEM")
        return student_interface()
    elif course_input.strip() == "".strip():
        print("Error: course cannot be blank")
        print("Rolling back to STUDENT XML SYSTEM")
        return student_interface()

    # this is where the C in CRUD Happens
    new_student = docs.createElement("student") # this creates a new student element
    new_student.setAttribute("id", input_id) # this adds an attribute id in the student as well as the name and value for it

    new_name = docs.createElement("name") # this creates a name element inside the student element
    new_name_text = docs.createTextNode(name_input) # this creates a text node for the name element
    new_name.appendChild(new_name_text) # this adds the new_name_text to our name element

    # the process is the same as the first one
    new_course = docs.createElement("course")
    new_course_text = docs.createTextNode(course_input)
    new_course.appendChild(new_course_text)

    # Basically we now added our new name and course to the student element
    new_student.appendChild(new_name)
    new_student.appendChild(new_course)

    # What I understood is that this adds the new student element to the root element on our document
    docs.documentElement.appendChild(new_student)

    save_xml(docs) # this adds/writes the current changes to the docs

    print("Student Added!")
    return student_interface()
def updateStudent(): # Start here and fix the input/exception handling
    studentId_checkList = [] # I store all ID's in student element for error handling
    load_xml() # this just updates the current function to latest file.xml
    found = False # This is if the targetID is not found

    students = docs.getElementsByTagName("student")

    targetID = input("Enter student ID to update: ")
    for student in students:
        student_id = student.getAttribute("id")
        studentId_checkList.append(student_id)  # this is where we add or append all the studentID for our error handling
        for i in range(0, len(studentId_checkList)):    # So this traverses each element in the list and checks if our targetID is equal to current index of the list
            if targetID == studentId_checkList[i]:
                found = True
    if not found: # this is pretty much self-explanatory
        print("Error: Student ID not found")
        print("Returning to Student XML SYSTEM")
        return student_interface() # We return back to STUDENT XML SYSTEM

    # this is the next part if we didn't encounter any errors
    print("What do you want to update?")
    print("1    -   Name")
    print("2    -   Course")
    print("3    -   Both")
    print("4    -   Return")
    userInput = input("Enter choice: ")

    # So if the user inputs anything above there this if statements handles that
    if userInput == "1":
        updateName_input = input("Enter new name: ")
        if updateName_input.strip() == "".strip():
            print("Error: name cannot be blank")
            print("Rolling back to STUDENT XML SYSTEM")
            return student_interface()
        for student in students:
            student_id = student.getAttribute("id")
            student_name = student.getElementsByTagName("name")
            if student_id == targetID: # Basically if the current studentID is matched with our targetID then we execute the code below
                student_name[0].firstChild.data = updateName_input  # Then the current student_name will be updated by whatever we input on the updateName_input
                save_xml(docs)  # Then we apply the current changes to our file
                print("Name updated!")

    # Everything processes the same as the first one
    elif userInput == "2":
        updateCourse_input = input("Enter new course: ")
        if updateCourse_input.strip() == "".strip():
            print("Error: course cannot be blank")
            print("Rolling back to STUDENT XML SYSTEM")
            return student_interface()
        for student in students:
            student_id = student.getAttribute("id")
            student_course = student.getElementsByTagName("course")
            if student_id == targetID:
                student_course[0].firstChild.data = updateCourse_input
                save_xml(docs)
                print("Course updated!")

    elif userInput == "3":
        updateName_input = input("Enter new name: ")
        updateCourse_input = input("Enter new course: ")
        # This check if the inputs are blank
        if updateCourse_input.strip() == "".strip() and updateName_input.strip() == "".strip():
            print("Error: name and course cannot be blank")
            print("Rolling back to STUDENT XML SYSTEM")
            return student_interface()
        elif updateName_input.strip() == "".strip():
            print("Error: name cannot be blank")
            print("Rolling back to STUDENT XML SYSTEM")
            return student_interface()
        elif updateCourse_input.strip() == "".strip():
            print("Error: course cannot be blank")
            print("Rolling back to STUDENT XML SYSTEM")
            return student_interface()

        for student in students:
            student_id = student.getAttribute("id")
            student_name = student.getElementsByTagName("name")
            student_course = student.getElementsByTagName("course")

            if student_id == targetID:
                student_name[0].firstChild.data = updateName_input
                student_course[0].firstChild.data = updateCourse_input
                save_xml(docs)
                print("Name and Course updated!")


    elif userInput == "4": # this just adds a layer of functionality if the user changes their mind mid-operation
        print("Rolling back to STUDENT XML SYSTEM")
        return student_interface()  #   Brings you back to the STUDENT XML SYSTEM
    else:   # This brings them back to updateStudent() function again if they input an invalid choice
        print("Error: That's not a valid choice")
        print("Rolling back to previous selection")
        return updateStudent()  # Bring you back to start of the updateStudent() function

    return student_interface() # Now if everything goes smoothly this just brings us back to the start

def deleteStudent():
    students  = docs.getElementsByTagName("student")
    studentID_checkList = [] # store all the ID for error handling purposes
    found = False   # Condition for our error handling
    load_xml()  # This is if the targetID is not found

    input_ID = input("Enter Student ID to delete: ")
    for student in students:
        student_id = student.getAttribute("id")
        studentID_checkList.append(student_id)  # this is where we add or append all the studentID for our error handling
        for i in range(0, len(studentID_checkList)):    # this has the same explanation as line 102
            if input_ID == studentID_checkList[i]:
                found = True
        if input_ID == student.getAttribute("id"):  # So this is where we delete the specific student element it checks if our input_ID is equal to the current studentID
            student.parentNode.removeChild(student) # So this accesses the parent node of the current node and removes it
    if not found:   # So if it errors it will execute this block of code below
        print("Error: Student ID not found")
        print("Rolling back to STUDENT XML SYSTEM")
        return student_interface()


    print("Student Deleted")
    save_xml(docs)  # Save the current changes and writes it in the file
    return student_interface() # Now if everything goes smoothly this just brings us back to the start

student_interface()