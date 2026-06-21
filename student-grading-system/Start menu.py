def startFeature():
    import time
    import os
    
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
    import sys
    import os
    
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
    import os
    import time
    
    with open("studentDetails.csv") as D:
        lines = D.readlines()

        for line in lines:
            studentData = line.strip().split(",")
            
            # Ensure the line has exactly 8 values as per your CSV layout
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
    import os
    
    try:
        # Correct file name: The file name is dynamic based on student ID
        file_name = rf"C:\Users\Kaizen Magdaraog\Desktop\finalProject\1234.csv"  # Full path to the file
        
        # Debugging: Print the file path to ensure it's correct
        print(f"Attempting to open file: {file_name}")

        # Check if the file exists before attempting to open it
        if not os.path.exists(file_name):
            print(f"Error: The file {file_name} does not exist.")
            return
        
        with open(file_name, "r", encoding='utf-8') as student_data_file:
            lines = student_data_file.readlines()
            # Strip extra spaces from each field to prevent issues from Excel formatting
            student_data = [line.strip().split(",") for line in lines if line.strip()]

        student_records = [record for record in student_data if record[0] == ID]

        if not student_records:
            print(f"Error: Student with ID {ID} not found in {file_name}.")
            return

        all_grades = []
        grades_by_term = {}
        courses = {}

        for record in student_records:
            # Ensure the record has the expected number of columns (e.g., 8)
            if len(record) >= 8: 
                term = record[2]
                grade = float(record[7])  # Accessing grade
                course_name = record[3]
                course_id = record[4]

                all_grades.append(grade)

                if term not in grades_by_term:
                    grades_by_term[term] = []
                grades_by_term[term].append(grade)

                if course_id not in courses:
                    courses[course_id] = {
                        "name": course_name,
                        "terms": [term]
                    }
                else:
                    courses[course_id]["terms"].append(term)
            else:
                print(f"Skipping malformed record (incorrect number of columns): {record}")

        overall_average = sum(all_grades) / len(all_grades) if all_grades else 0

        term_averages = {}
        for term, grades in grades_by_term.items():
            if grades:
                term_averages[term] = sum(grades) / len(grades)
            else:
                term_averages[term] = "No grades available"

        max_grade = max(all_grades) if all_grades else None
        min_grade = min(all_grades) if all_grades else None

        term_max_grades = {}
        term_min_grades = {}
        for term, grades in grades_by_term.items():
            if grades:
                term_max_grades[term] = max(grades)
            else:
                term_max_grades[term] = None
            if grades:
                term_min_grades[term] = min(grades)
            else:
                term_min_grades[term] = None

        repeated_courses = []
        for course_id, course_info in courses.items():
            if len(course_info["terms"]) > 1:
                repeated_courses.append(course_info["name"])

        print("\nStatistics for Student ID:", ID)
        print(f"Overall Average: {overall_average:.2f}")
        print("Term Averages:")
        for term, avg in term_averages.items():
            print(f"  {term}: {avg}")
        print(f"Maximum Grade: {max_grade}")
        print(f"Minimum Grade: {min_grade}")
        print("Term Maximum Grades:")
        for term, max_grade in term_max_grades.items():
            print(f"  {term}: {max_grade}")
        print("Term Minimum Grades:")
        for term, min_grade in term_min_grades.items():
            print(f"  {term}: {min_grade}")
        print("Repeated Courses:", ", ".join(repeated_courses) or "None")

        # Correct file naming for student statistics
        with open(rf"C:\Users\Kaizen Magdaraog\Desktop\finalProject\student_{ID}_statistics.txt", "w", encoding='utf-8') as stats_file:
            stats_file.write("Statistics for Student ID: {}\n".format(ID))
            stats_file.write(f"Overall Average: {overall_average:.2f}\n")
            stats_file.write("Term Averages:\n")
            for term, avg in term_averages.items():
                stats_file.write(f"  {term}: {avg:.2f}\n")
            stats_file.write(f"Maximum Grade: {max_grade}\n")
            stats_file.write(f"Minimum Grade: {min_grade}\n")
            stats_file.write("Term Maximum Grades:\n")
            for term, max_grade in term_max_grades.items():
                stats_file.write(f"  {term}: {max_grade}\n")
            stats_file.write("Term Minimum Grades:\n")
            for term, min_grade in term_min_grades.items():
                stats_file.write(f"  {term}: {min_grade}\n")
            stats_file.write("Repeated Courses: ")
            stats_file.write(", ".join(repeated_courses) or "None\n")

    except FileNotFoundError:
        print(f"Error: The file {file_name} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

startFeature()
