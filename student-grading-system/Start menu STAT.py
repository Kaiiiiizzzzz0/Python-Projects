import time
import os
import sys

def startFeature():
    with open("studentDetails.csv") as D:
        database = D.read()
        database.strip()

        while True:
            level = input("Student level (Undergrad(U), Grad(G), Both(B)): ")
            if level == "G" or level == "B" or level == "U":
                break

        while True:
            ID = input("Please enter ID: ")
            if ID in database:
                time.sleep(1)
                menuFeature(ID)
                break
            else:
                print("ID does not exist in the database. Please try again.")

def menuFeature(ID):
    print("\033[1m Student Transcript Generation System \033[0;0m")
    print("=" * 45)
    print(" 1. Student details\n 2. Statistics\n 3. Transcript based on major courses\n 4. Transcript based on minor courses\n 5. Full transcript\n 6. Previous transcript requests\n 7. Select another student\n 8. Terminate the system")
    print("=" * 45)
    
    while True:
        try:
            select_feature = int(input("\033[1m Enter your feature: \033[0;0m"))
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    if select_feature == 1:
        detailsFeature(ID)  
    elif select_feature == 2:
        statistics_feature(ID)  
    elif select_feature == 8:
        sys.exit()
    else:
        print("Invalid selection. Please try again.")
        menuFeature(ID)

def detailsFeature(ID):
    with open("studentDetails.csv") as D:
        lines = D.readlines()

        for line in lines:
            studentData = line.strip().split(",")
            
            if len(studentData) == 8:  
                if studentData[0] == ID:  
                    print(f"Details for ID {ID}:")
                    print(f"Name: {studentData[1]}")
                    print(f"Student ID: {studentData[0]}")
                    print(f"College: {studentData[2]}")
                    print(f"Department: {studentData[3]}")
                    print(f"Level: {studentData[4]}")
                    print(f"Degree: {studentData[5]}")
                    print(f"Terms: {studentData[6]}")
                    print(f"Grade: {studentData[7]}")

                    studentDetailsFile = f"C:\\Users\\Kaizen Magdaraog\\Desktop\\finalProject\\std{ID}details.txt"
                    with open(studentDetailsFile, "w") as studentFile:
                        studentFile.write(f"Name: {studentData[1]}\n")
                        studentFile.write(f"College: {studentData[2]}\n")
                        studentFile.write(f"Department: {studentData[3]}\n")
                        studentFile.write(f"Level: {studentData[4]}\n")
                        studentFile.write(f"Degree: {studentData[5]}\n")
                        studentFile.write(f"Terms: {studentData[6]}\n")
                        studentFile.write(f"Grade: {studentData[7]}\n")

                    time.sleep(3)
                    os.system("cls")
                    menuFeature(ID)
                    break
            else:
                print(f"Skipping malformed line (incorrect number of columns): {line}")
def statistics_feature(ID):
    try:
        
        file_name = f"C:\\Users\\Kaizen Magdaraog\\Desktop\\finalProject\\{ID}.csv"
        
        
        print(f"Attempting to open file: {file_name}")

        
        if not os.path.exists(file_name):
            print(f"Error: The file {file_name} does not exist.")
            return

        
        with open(file_name, "r") as student_data_file:
            lines = student_data_file.readlines()

        
        student_data = [line.strip().split(",") for line in lines[1:] if line.strip()]  

        all_grades = []
        grades_by_term = {}
        courses = {}

        for record in student_data:
            if len(record) >= 8:  
                term = record[2]
                grade = float(record[7])  
                course_name = record[3]
                course_id = record[4]

                all_grades.append(grade)

                if term not in grades_by_term:
                    grades_by_term[term] = []
                grades_by_term[term].append(grade)

                if course_id not in courses:
                    courses[course_id] = {"name": course_name, "terms": [term]}
                else:
                    courses[course_id]["terms"].append(term)

        overall_average = sum(all_grades) / len(all_grades) if all_grades else 0

        print("\nStatistics for Student ID:", ID)
        print(f"Overall Average: {overall_average:.2f}")
        print("Term Averages:")
        for term, grades in grades_by_term.items():
            print(f"  {term}: {sum(grades) / len(grades):.2f}" if grades else f"  {term}: No grades available")
        print("Maximum Grade:", max(all_grades) if all_grades else "No grades available")
        print("Minimum Grade:", min(all_grades) if all_grades else "No grades available")

    except Exception as e:
        print(f"An error occurred while reading the file: {e}")

startFeature()
