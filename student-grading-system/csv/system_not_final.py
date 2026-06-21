from datetime import datetime
import numpy as np
import os        #Module for clear screen
import sys       #Importing module to terminate the system one finished
import time      #Module for adding loading time to the menus

#This is the starting point of the program
#This is the the function for Initiating the program
def startFeature(request_count):
    with open("studentDetails.csv") as D:  # Opens the database CSV file
        next(D)  # Skips the header row
        database = D.readlines()  # Reads all lines from the file

        # Extract all student IDs from the database
        student_ids = [rows.strip().split(",")[0] for rows in database]

        # Ask the user for the student level
        level = input("Student level (Undergrad(U), Grad(G), Both(B)): ").upper()
        
        # Validate the level input
        if level not in ["U", "G", "B"]:
            print("You must enter a valid level (U, G, or B).")
            startFeature(request_count)  # Restart the function if the input is invalid
            return

        # If the level is Graduate (G) or Both (B), ask for the degree
        if level in ["G", "B"]:
            degree = input("Master(M), Doctorate(D), Both(BO): ").upper()
            if degree not in ["M", "D", "BO"]:
                print("You must enter a valid degree (M, D, or BO).")
                startFeature(request_count)  # Restart the function if the input is invalid
                return

        # Ask the user for the student ID
        while True:
            ID = input("Please enter ID: ")
            if ID in student_ids:  # Check if the ID exists in the database
                print("ID found. Redirecting to the menu...")
                time.sleep(1)  # Wait for 1 second
                menuFeature(ID, request_count)  # Redirect to the menu
                break
            else:
                print("Invalid ID. Please enter a valid ID.")
            
def menuFeature(ID, request_count):
    ''' WE NEED A FUNCTION TO CLEAR THE OUTPUT AFTER RETURNING TO THE MENU '''           
    clearScreen()
    #The output of the menu itself   #It shows the user the possible options
    print(" \033[1m Student Transcript Generation System \033[0;0m")
    print(" ", "=" * 45)
    print(" 1. Student details\n 2. Statistics\n 3. Transcript based on major courses\n 4. Transcript based on minor courses\n 5. Full transcript\n 6. Previous transcript requests\n 7. Select another student\n 8. Ternminate the system")
    print(" ", "=" * 45)
    select_feature = int(input("\033[1m  Enter your feature: \033[0;0m"))     #The feature that asks the user for selection


    if select_feature == 1:         #Condition if user chose #1 
        clearScreen()
        detailsFeature(ID, request_count)          #The user would be sent to the details function and would be presented with details of the entered student ID
    
    elif select_feature == 2:       #Condition if user chose #2
        clearScreen()
        statisticsFeature(ID, request_count)        #The user would be sent to the statistics function 
    
    elif select_feature == 3:       #Condition if user chose #3
        clearScreen()
        request_count += 1
        majorTranscriptFeature(ID, request_count)    #The user would be sent to the details function and would be presented a transcript of all Major courses taken 
    elif select_feature == 4:       #Condition if user chose #4 
        clearScreen()
        request_count += 1
        minorTranscriptFeature(ID, request_count)     #The user would be sent to the details function and would be presented a transcript of all Minor courses taken
    elif select_feature == 5:      #Condition if user chose #5
        clearScreen()
        request_count += 1
        fullTranscriptFeature(ID, request_count)      #The user would be sent to the Full transcript function and then would be presented a transcript of both Major and Minor courses taken
    elif select_feature == 6:      #Condition if user chose #6
        clearScreen()
        previousRequestsFeature(ID, request_count)      #The user would be sent to the Previous transcript requests function which shows the user a record of previous trancsript requests
    
    elif select_feature == 7:      #Condition if user chose #7
        clearScreen()
        newStudentFeature(request_count)      #The user would be sent to the Select another student function which the program allows the user to input another ID 
    
    elif select_feature == 8:       #Condition if user chose #8 
        clearScreen()
        terminateFeature(request_count) 
        
    else:
        print("Invalid selection! Please enter a number between 1 and 8.")
        print("Redirecting back to menu...")
        time.sleep(3)
        return menuFeature(ID, request_count)
    
def detailsFeature(ID, request_count):
    # Read student details from the database
    with open("studentDetails.csv") as D:  # Open the database CSV file
        next(D)  # Skip the header row
        for row in D:
            data = row.strip().split(",")
            if data[0] == ID:  # Check if the current row matches the student ID
                # Extract student details
                name = data[1]
                stdID = data[0]
                num_terms = data[4]
                college = data[2]
                department = data[3]
                break
        else:
            print(f"Student with ID {ID} not found in the database.")
            return

    # Display student details on the screen
    print("\nStudent Details:")
    print(f"Name: {name}")
    print(f"Student ID: {stdID}")
    print(f"Number of Terms: {num_terms}")
    print(f"College: {college}")
    print(f"Department: {department}")

    # Save student details to a file
    filename = f"std{ID}details.txt"
    with open(filename, "w") as file:
        file.write(f"Name: {name}\n")
        file.write(f"Student ID: {stdID}\n")
        file.write(f"Number of Terms: {num_terms}\n")
        file.write(f"College: {college}\n")
        file.write(f"Department: {department}\n")

    # Wait for a few seconds
    time.sleep(3)

    # Redirect to the menu window
    menuFeature(ID, request_count)

def statisticsFeature(ID, request_count):
    import numpy as np
    # Step 1: Read the student's course data from the CSV file using NumPy
    filename = f"{ID}.csv"
    try:
        data = np.genfromtxt(filename, delimiter=',', dtype=str, skip_header=1)
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return

    # Step 2: Extract relevant columns
    terms = data[:, 2]  # Term column
    grades = data[:, 7].astype(float)  # Grade column (convert to float)
    course_ids = data[:, 4]  # Course ID column
    levels = data[:, 0]  # Level column (first column)

    # Step 3: Group data by level
    unique_levels = np.unique(levels)  # Get unique levels (e.g., "U", "G")
    level_data = {level: data[levels == level] for level in unique_levels}

    # Step 4: Initialize output list
    output = []

    # Step 5: Process each level and append results to the same output
    for level, level_courses in level_data.items():
        # Standardize the level to either "Undergraduate" or "Graduate"
        if level.lower() in ["u"]:
            level_name = "Undergraduate"
        elif level.lower() in ["g"]:
            level_name = "Graduate"
        else:
            level_name = "Unknown Level"  # Fallback for unexpected values

        # Extract relevant columns for this level
        level_terms = level_courses[:, 2]  # Term column
        level_grades = level_courses[:, 7].astype(float)  # Grade column
        level_course_ids = level_courses[:, 4]  # Course ID column

        # Calculate statistics for this level
        overall_avg = np.mean(level_grades)  # Overall average for this level
        unique_terms = np.unique(level_terms)  # Unique terms for this level
        term_avg = {term: np.mean(level_grades[level_terms == term]) for term in unique_terms}  # Term averages
        max_grades = {term: np.max(level_grades[level_terms == term]) for term in unique_terms}  # Max grades
        min_grades = {term: np.min(level_grades[level_terms == term]) for term in unique_terms}  # Min grades

        # Check for repeated courses for this level
        unique_course_ids, counts = np.unique(level_course_ids, return_counts=True)
        repeated_courses = unique_course_ids[counts > 1]

        # Step 6: Format the statistics output for this level
        output.append("=" * 65)
        if level_name == "Undergraduate":
            output.append("*" * 15 + " " * 8 + f"{level_name} Level" + " " * 8 + "*" * 15)
        elif level_name == "Graduate":
            output.append("*" * 18 + " " * 8 + f"{level_name} Level" + " " * 8 + "*" * 17)
        else:
            output.append("*" * 19 + " " * 8 + f"{level_name} Level" + " " * 8 + "*" * 19)
        output.append("=" * 65)
        output.append(" Overall average (major and minor) for all terms: ")
        output.append(f" \t {overall_avg:.2f}")
        output.append(" Average (major and minor) of each term: ")
        for term, avg in term_avg.items():
            output.append(f" \t Term {term}: {avg:.2f}")
        output.append(" Maximum grade(s) and in which term(s): ")
        for term, max_grade in max_grades.items():
            output.append(f" \t Term {term}: {max_grade}")
        output.append(" Minimum grade(s) and in which term(s): ")
        for term, min_grade in min_grades.items():
            output.append(f" \t Term {term}: {min_grade}")
        output.append(" Do you have repeated course(s): ")
        if len(repeated_courses) > 0:
            output.append(f" \t Repeated Courses: {', '.join(repeated_courses)}")
        else:
            output.append(" \t No repeated courses.")
            
    # Step 7: Display the statistics on the screen
    print("\n".join(output))

    # Step 8: Save the statistics to a file
    output_filename = f"std{ID}statistics.txt"
    with open(output_filename, "w") as file:
        file.write("\n".join(output))

    # Step 9: Wait and redirect to the menu
    time.sleep(3)  # Wait for 3 seconds
    menuFeature(ID, request_count)  # Redirect to the menu

def majorTranscriptFeature(ID, request_count):
    # Step 1: Read the student's details from studentDetails.csv using NumPy
    try:
        student_details_data = np.genfromtxt("studentDetails.csv", delimiter=',', dtype=str, skip_header=1)
        student_details = None
        for row in student_details_data:
            if row[0] == ID:  # Check if the stdID matches
                student_details = {
                    "name": row[1],
                    "stdID": row[0],
                    "college": row[2],
                    "department": row[3],
                    "num_terms": row[6],
                    "level": row[4]  # Level from studentDetails.csv
                }
                break
        if not student_details:
            print(f"Student with ID {ID} not found in studentDetails.csv.")
            return
    except FileNotFoundError:
        print("File studentDetails.csv not found.")
        return

    # Step 2: Read the student's course data from the CSV file using NumPy
    filename = f"{ID}.csv"
    try:
        data = np.genfromtxt(filename, delimiter=',', dtype=str, skip_header=1)
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return

    # Step 3: Extract relevant columns
    course_types = data[:, 5]  # Course type column
    levels = data[:, 0]  # Level column (first column)

    # Step 4: Group data by level
    unique_levels = np.unique(levels)  # Get unique levels (e.g., "U", "G")
    level_data = {level: data[levels == level] for level in unique_levels}

    # Step 5: Initialize output list
    output = []

    # Step 6: Process each level and append results to the same output
    for level, level_courses in level_data.items():
        # Standardize the level to either "Undergraduate" or "Graduate"
        if level.lower() in ["u"]:
            level_name = "Undergraduate"
        elif level.lower() in ["g"]:
            level_name = "Graduate"
        else:
            level_name = "Unknown Level"  # Fallback for unexpected values

        # Filter major courses for this level
        major_mask = np.char.lower(level_courses[:, 5]) == "major"  # Mask for major courses
        minor_mask = np.char.lower(level_courses[:, 5]) == "minor"  # Mask for minor courses

        major_courses = level_courses[major_mask]  # Filter major courses
        minor_courses = level_courses[minor_mask]  # Filter minor courses

        # Count the number of major and minor courses
        num_major_courses = len(major_courses)
        num_minor_courses = len(minor_courses)

        if major_courses.size == 0:
            output.append(f"No major courses found for {level_name} Level.")
            continue

        # Step 7: Group courses by term and calculate averages
        unique_terms = np.unique(major_courses[:, 2])  # Get unique terms
        term_avg = {}  # Dictionary to store term averages
        overall_grades = []  # List to store all major course grades

        for term in unique_terms:
            # Filter major courses for the current term
            term_mask = (major_courses[:, 2] == term)
            term_grades = major_courses[term_mask][:, 7].astype(float)
            term_avg[term] = np.mean(term_grades) if term_grades.size > 0 else 0
            overall_grades.extend(term_grades)

        # Calculate overall major average
        overall_avg = np.mean(overall_grades) if overall_grades else 0

        # Step 8: Format the transcript for this level
        output.append("=" * 60)
        if level_name == "Undergraduate":
            output.append("*" * 12 + " " * 8 + f"{level_name} Level" + " " * 8 + "*" * 13)
        elif level_name == "Graduate":
            output.append("*" * 16 + " " * 8 + f"{level_name} Level" + " " * 8 + "*" * 14)
        else:
            output.append("*" * 18 + " " * 8 + f"{level_name} Level" + " " * 8 + "*" * 18)
        output.append("=" * 60)
        output.append(f"{'Name:':<20}{student_details['name']:<30}{'stdID:':<20}{student_details['stdID']}")
        output.append(f"{'College:':<20}{student_details['college']:<30}{'Department:':<20}{student_details['department']}")
        output.append(f"{'Major:':<20}{num_major_courses:<30}{'Minor:':<20}{num_minor_courses}")
        output.append(f"{'Level:':<20}{level_name:<30}{'Number of terms:':<20}{student_details['num_terms']}")
        output.append("=" * 60)

        for term in unique_terms:
            output.append("*" * 18 + " " * 9 + " Term " + term + " " * 8 + "*" * 18)
            output.append("=" * 60)
            output.append(f"{'course ID':<12}{'course name':<25}{'credit hours':<15}{'grade'}")

            # Add major courses for the term
            term_mask = (major_courses[:, 2] == term)
            term_courses = major_courses[term_mask]
            for course in term_courses:
                output.append(f"{course[4]:<12}{course[3]:<25}{course[6]:<15}{course[7]}")

            # Add averages for the term
            output.append(f"{'Major Average =':<20}{term_avg[term]:.2f}")
            output.append("=" * 60)

        # Add end of transcript for this level
        if level_name == "Undergraduate":
            output.append("*" * 9 + " End of Transcript for " + f"{level_name} Level " + "*" * 8)
        elif level_name == "Graduate":
            output.append("*" * 11 + " End of Transcript for " + f"{level_name} Level " + "*" * 11)
        else:
            output.append("*" * 8 + " End of Transcript for " + f"{level_name} Level " + "*" * 8)
        output.append("=" * 60)

    # Step 9: Display the transcript on the screen
    print("\n".join(output))

    # Step 10: Save the transcript to a file
    output_filename = f"std{ID}MajorTranscript.txt"
    with open(output_filename, "w") as file:
        file.write("\n".join(output))

    # Step 11: Log, wait, and redirect to the menu
    log_transaction(ID, "Major Transcript")
    time.sleep(3)  # Wait for 3 seconds
    menuFeature(ID, request_count)  # Redirect to the menu
    
def minorTranscriptFeature(ID, request_count):
    # Step 1: Read the student's details from studentDetails.csv using NumPy
    try:
        student_details_data = np.genfromtxt("studentDetails.csv", delimiter=',', dtype=str, skip_header=1)
        student_details = None
        for row in student_details_data:
            if row[0] == ID:  # Check if the stdID matches
                student_details = {
                    "name": row[1],
                    "stdID": row[0],
                    "college": row[2],
                    "department": row[3],
                    "num_terms": row[6],
                    "level": row[4]  # Level from studentDetails.csv
                }
                break
        if not student_details:
            print(f"Student with ID {ID} not found in studentDetails.csv.")
            return
    except FileNotFoundError:
        print("File studentDetails.csv not found.")
        return

    # Step 2: Read the student's course data from the CSV file using NumPy
    filename = f"{ID}.csv"
    try:
        data = np.genfromtxt(filename, delimiter=',', dtype=str, skip_header=1)
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return

    # Step 3: Extract relevant columns
    course_types = data[:, 5]  # Course type column
    levels = data[:, 0]  # Level column (first column)

    # Step 4: Group data by level
    unique_levels = np.unique(levels)  # Get unique levels (e.g., "U", "G")
    level_data = {level: data[levels == level] for level in unique_levels}

    # Step 5: Initialize output list
    output = []

    # Step 6: Process each level and append results to the same output
    for level, level_courses in level_data.items():
        # Standardize the level to either "Undergraduate" or "Graduate"
        if level.lower() in ["u"]:
            level_name = "Undergraduate"
        elif level.lower() in ["g"]:
            level_name = "Graduate"
        else:
            level_name = "Unknown Level"  # Fallback for unexpected values

        # Filter minor courses for this level
        major_mask = np.char.lower(level_courses[:, 5]) == "major"  # Mask for major courses
        minor_mask = np.char.lower(level_courses[:, 5]) == "minor"  # Mask for minor courses

        major_courses = level_courses[major_mask]  # Filter major courses
        minor_courses = level_courses[minor_mask]  # Filter minor courses

        # Count the number of major and minor courses
        num_major_courses = len(major_courses)
        num_minor_courses = len(minor_courses)

        if minor_courses.size == 0:
            output.append(f"No minor courses found for {level_name} Level.")
            continue

        # Step 7: Group courses by term and calculate averages
        unique_terms = np.unique(minor_courses[:, 2])  # Get unique terms
        term_avg = {}  # Dictionary to store term averages
        overall_grades = []  # List to store all minor course grades

        for term in unique_terms:
            # Filter minor courses for the current term
            term_mask = (minor_courses[:, 2] == term)
            term_grades = minor_courses[term_mask][:, 7].astype(float)
            term_avg[term] = np.mean(term_grades) if term_grades.size > 0 else 0
            overall_grades.extend(term_grades)

        # Calculate overall minor average
        overall_avg = np.mean(overall_grades) if overall_grades else 0

        # Step 8: Format the transcript for this level
        output.append("=" * 60)
        if level_name == "Undergraduate":
            output.append("*" * 12 + " " * 8 + f"{level_name} Level" + " " * 8 + "*" * 13)
        elif level_name == "Graduate":
            output.append("*" * 16 + " " * 8 + f"{level_name} Level" + " " * 8 + "*" * 14)
        else:
            output.append("*" * 18 + " " * 8 + f"{level_name} Level" + " " * 8 + "*" * 18) 
        output.append("=" * 60)
        output.append(f"{'Name:':<20}{student_details['name']:<30}{'stdID:':<20}{student_details['stdID']}")
        output.append(f"{'College:':<20}{student_details['college']:<30}{'Department:':<20}{student_details['department']}")
        output.append(f"{'Major:':<20}{num_major_courses:<30}{'Minor:':<20}{num_minor_courses}")
        output.append(f"{'Level:':<20}{level_name:<30}{'Number of terms:':<20}{student_details['num_terms']}")
        output.append("=" * 60)

        for term in unique_terms:
            output.append("*" * 18 + " " * 9 + " Term " + term + " " * 8 + "*" * 18)
            output.append("=" * 60)
            output.append(f"{'course ID':<12}{'course name':<25}{'credit hours':<15}{'grade'}")

            # Add minor courses for the term
            term_mask = (minor_courses[:, 2] == term)
            term_courses = minor_courses[term_mask]
            for course in term_courses:
                output.append(f"{course[4]:<12}{course[3]:<25}{course[6]:<15}{course[7]}")

            # Add averages for the term
            output.append(f"{'Minor Average =':<20}{term_avg[term]:.2f}")
            output.append("=" * 60)

        # Add end of transcript for this level
        if level_name == "Undergraduate":
            output.append("*" * 9 + " End of Transcript for " + f"{level_name} Level " + "*" * 8)
        elif level_name == "Graduate":
            output.append("*" * 11 + " End of Transcript for " + f"{level_name} Level " + "*" * 11)
        else:
            output.append("*" * 8 + " End of Transcript for " + f"{level_name} Level " + "*" * 8)
        output.append("=" * 60)

    # Step 9: Display the transcript on the screen
    print("\n".join(output))

    # Step 10: Save the transcript to a file
    output_filename = f"std{ID}MinorTranscript.txt"
    with open(output_filename, "w") as file:
        file.write("\n".join(output))

    # Step 11: Log, wait, and redirect to the menu
    log_transaction(ID, "Minor Transcript")
    time.sleep(3)  # Wait for 3 seconds
    menuFeature(ID, request_count)  # Redirect to the menu

def fullTranscriptFeature(ID, request_count):
    # Step 1: Read the student's details from studentDetails.csv using NumPy
    try:
        student_details_data = np.genfromtxt("studentDetails.csv", delimiter=',', dtype=str, skip_header=1)
        student_details = None
        for row in student_details_data:
            if row[0] == ID:  # Check if the stdID matches
                student_details = {
                    "name": row[1],
                    "stdID": row[0],
                    "college": row[2],
                    "department": row[3],
                    "num_terms": row[6],
                    "level": row[4]  # Level from studentDetails.csv
                }
                break
        if not student_details:
            print(f"Student with ID {ID} not found in studentDetails.csv.")
            return
    except FileNotFoundError:
        print("File studentDetails.csv not found.")
        return

    # Step 2: Read the student's course data from the CSV file using NumPy
    filename = f"{ID}.csv"
    try:
        data = np.genfromtxt(filename, delimiter=',', dtype=str, skip_header=1)
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return

    # Step 3: Extract relevant columns
    terms = data[:, 2]  # Term column
    course_types = data[:, 5]  # Course type column
    levels = data[:, 0]  # Level column (first column)

    # Step 4: Group data by level
    unique_levels = np.unique(levels)  # Get unique levels (e.g., "U", "G")
    level_data = {level: data[levels == level] for level in unique_levels}

    # Step 5: Initialize output list
    output = []

    # Step 6: Process each level and append results to the same output
    for level, level_courses in level_data.items():
        # Standardize the level to either "Undergraduate" or "Graduate"
        if level.lower() in ["u"]:
            level_name = "Undergraduate"
        elif level.lower() in ["g"]:
            level_name = "Graduate"
        else:
            level_name = "Unknown Level"  # Fallback for unexpected values

        # Filter major and minor courses for this level
        major_mask = np.char.lower(level_courses[:, 5]) == "major"  # Mask for major courses
        minor_mask = np.char.lower(level_courses[:, 5]) == "minor"  # Mask for minor courses

        major_courses = level_courses[major_mask]  # Filter major courses
        minor_courses = level_courses[minor_mask]  # Filter minor courses

        # Count the number of major and minor courses
        num_major_courses = len(major_courses)
        num_minor_courses = len(minor_courses)

        if major_courses.size == 0 and minor_courses.size == 0:
            output.append(f"No courses found for {level_name} Level.")
            continue

        # Step 7: Group courses by term and calculate averages
        unique_terms = np.unique(level_courses[:, 2])  # Get unique terms
        term_major_avg = {}  # Dictionary to store major averages per term
        term_minor_avg = {}  # Dictionary to store minor averages per term
        term_overall_avg = {}  # Dictionary to store overall averages per term
        overall_major_grades = []  # List to store all major course grades
        overall_minor_grades = []  # List to store all minor course grades

        for term in unique_terms:
            # Filter major courses for the current term
            term_major_mask = (major_courses[:, 2] == term)
            term_major_grades = major_courses[term_major_mask][:, 7].astype(float)
            term_major_avg[term] = np.mean(term_major_grades) if term_major_grades.size > 0 else 0
            overall_major_grades.extend(term_major_grades)

            # Filter minor courses for the current term
            term_minor_mask = (minor_courses[:, 2] == term)
            term_minor_grades = minor_courses[term_minor_mask][:, 7].astype(float)
            term_minor_avg[term] = np.mean(term_minor_grades) if term_minor_grades.size > 0 else 0
            overall_minor_grades.extend(term_minor_grades)

            # Calculate overall average for the term
            term_all_grades = np.concatenate((term_major_grades, term_minor_grades))
            term_overall_avg[term] = np.mean(term_all_grades) if term_all_grades.size > 0 else 0

        # Step 8: Format the transcript for this level
        output.append("=" * 60)
        if level_name == "Undergraduate":
            output.append("*" * 12 + " " * 8 + f"{level_name} Level" + " " * 8 + "*" * 13)
        elif level_name == "Graduate":
            output.append("*" * 16 + " " * 8 + f"{level_name} Level" + " " * 8 + "*" * 14)
        else:
            output.append("*" * 18 + " " * 8 + f"{level_name} Level" + " " * 8 + "*" * 18)
        output.append("=" * 60)
        output.append(f"{'Name:':<20}{student_details['name']:<30}{'stdID:':<20}{student_details['stdID']}")
        output.append(f"{'College:':<20}{student_details['college']:<30}{'Department:':<20}{student_details['department']}")
        output.append(f"{'Major:':<20}{num_major_courses:<30}{'Minor:':<20}{num_minor_courses}")
        output.append(f"{'Level:':<20}{level_name:<30}{'Number of terms:':<20}{student_details['num_terms']}")
        output.append("=" * 60)

        for term in unique_terms:
            output.append("*" * 18 + " " * 9 + " Term " + term + " " * 8 + "*" * 18)
            output.append("=" * 60)
            output.append(f"{'course ID':<12}{'course name':<25}{'credit hours':<15}{'grade'}")

            # Add major courses for the term
            term_major_mask = (major_courses[:, 2] == term)
            term_major_courses = major_courses[term_major_mask]
            for course in term_major_courses:
                output.append(f"{course[4]:<12}{course[3]:<25}{course[6]:<15}{course[7]}")

            # Add minor courses for the term
            term_minor_mask = (minor_courses[:, 2] == term)
            term_minor_courses = minor_courses[term_minor_mask]
            for course in term_minor_courses:
                output.append(f"{course[4]:<12}{course[3]:<25}{course[6]:<15}{course[7]}")

            # Add averages for the term
            output.append(f"{'Major Average =':<20}{term_major_avg[term]:.2f}")
            output.append(f"{'Minor Average =':<20}{term_minor_avg[term]:.2f}")
            output.append(f"{'Term Average =':<20}{term_overall_avg[term]:.2f}")
            output.append("=" * 60)

        # Add end of transcript for this level
        if level_name == "Undergraduate":
            output.append("*" * 9 + " End of Transcript for " + f"{level_name} Level " + "*" * 8)
        elif level_name == "Graduate":
            output.append("*" * 11 + " End of Transcript for " + f"{level_name} Level " + "*" * 11)
        else:
            output.append("*" * 8 + " End of Transcript for " + f"{level_name} Level " + "*" * 8)
        output.append("=" * 60)

    # Step 9: Display the transcript on the screen
    print("\n".join(output))

    # Step 10: Save the transcript to a file
    output_filename = f"std{ID}FullTranscript.txt"
    with open(output_filename, "w") as file:
        file.write("\n".join(output))

    # Step 11: Log, wait, and redirect to the menu
    log_transaction(ID, "Full Transcript ")
    time.sleep(3)  # Wait for 3 seconds
    menuFeature(ID, request_count)  # Redirect to the menu
    
def previousRequestsFeature(ID, request_count):
    filename = f"std{ID}PreviousRequests.txt"

    # Step 1: Check if the file exists
    if not os.path.exists(filename):
        print("No previous requests found.")
        time.sleep(2)  # Wait for 2 seconds
        menuFeature(ID, request_count)  # Redirect to the menu
        return

    # Step 2: Read and display the previous requests
    output = []
    output.append("=" * 60)
    output.append("*" * 14 + "\t\t  Previous Requests\t      " + "*" * 14)
    output.append("=" * 60)
    output.append("Request\t\tDate\t\tTime\t\t")
    output.append("=" * 60)

    with open(filename, "r") as file:
        for line in file:
            output.append(line.strip())

    output.append("=" * 60)

    # Step 3: Display the previous requests on the screen
    print("\n".join(output))

    # Step 4: Wait and redirect to the menu
    time.sleep(3)  # Wait for 3 seconds
    menuFeature(ID, request_count)  # Redirect to the menu
    
def newStudentFeature(request_count): 
    clearScreen()
    startFeature(request_count)
    
def terminateFeature(request_count):
    print(f"\nNumber of requests during this session: {request_count}")
    print("Terminating the program. Goodbye!")
    sys.exit()                  #Program then executes the terminate function if user selected this option

def clearScreen():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # macOS, Linux
        os.system('clear')

def log_transaction(ID, transaction_type):
    """
    Logs a transaction (e.g., major, minor, full transcript request) to the previous requests file.
    """
    timestamp = datetime.now().strftime("%d/%m/%Y\t%H:%M %p")
    with open(f"std{ID}PreviousRequests.txt", "a") as file:
        file.write(f"{transaction_type}\t\t{timestamp}\n")
    
def main():
    request_count = 0
    print("Welcome to the Student Transcript Generation System!")
    startFeature(request_count)  # Start the program by calling the startFeature function

if __name__ == "__main__":
    main()