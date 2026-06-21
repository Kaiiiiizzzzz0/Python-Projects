class User:
    def __init__(self, name, age, user_Id):
        self.name = name
        self.age = age
        self.user_Id = user_Id

class Ticket: 
    def __init__(self, ticket_Tier, date, start_Location, end_Location, kilometers):
        self.ticket_Tier = ticket_Tier
        self.date = date
        self.start_Location = start_Location
        self.end_Location = end_Location
        self.kilometers = kilometers

    def calculate_Fare(self):
        fare = self.kilometers * 2.5

        if self.ticket_Tier.lower() in ["student","senior","pwd"]:
            fare *= 0.80
        
        return fare

class Ticket_Manager: #should only store the user info 
    
    def __init__(self, users):
        self.user_List = []
        self.user_List.append(users)

class Input_Receiver: #should only receive the user info then pass it to Ticket_Manager class

    def string_Checker(self, prompt):
        while True:
            name = input(prompt)
            if name.replace(" ", "").isalpha() and name.strip():
                return name
            print("Invalid Name, use letters only.")
    
    def get_Number(self, prompt):
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Put only a number.")

    def user_Info(self):
        name = self.string_Checker("Name: ")
        age = self.get_Number("Age: ")
        user_Id = self.get_Number("ID: ")
    
        return User(name, age, user_Id)

    def ticket_Info(self):
        ticket_Tier = input("Ticket Tier: ")
        date = input("Date: ")
        start_Location = input("Start Location: ")
        end_Location = input("End Location: ")
        kilometers = self.get_Number("Kilometers: ")

        return Ticket(
            ticket_Tier,
            date,
            start_Location,
            end_Location,
            kilometers
        )

receiver = Input_Receiver()
user = receiver.user_Info()
manager = Ticket_Manager(user)
ticket = receiver.ticket_Info()

print(manager.user_List[0].name)
print(manager.user_List[0].age)
print(manager.user_List[0].user_Id)
print(ticket.calculate_Fare())
