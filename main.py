from search import Search_Info
from datetime import datetime
from plotting_funcs import load_race_event
from plotting_funcs import inner_menu
import fastf1

print("Welcome to F1 App version 1.0\n")
print("Thhis app will allow you to view race data, race analysis, and fun facts from all events starting in 2018\n")
exit = False
search_history = []
while not exit:
    print("\n\n ----- MAIN MENU -----\n")
    print("1. Initiate new search ")
    print("2. View past search ")
    print("3. Set favourite driver ")
    print("4. Bonus")
    print("5. Exit")
    
    command = int(input("Enter command: "))

    if command == 1:
        year = int(input("Enter championship year: "))
        location = input("Enter race location: ")
        search_obj = Search_Info(year, location, " ")
        searched_event = None
        bad_search = False
        try:
            searched_event = fastf1.get_event(search_obj._year, search_obj._location)
        except ValueError:
            print("Sorry, Event not found.")
            bad_search = True
            
            
        if not bad_search:
            while True:
                load_race_event(searched_event)
                print("\n1. View Race Laptimes")
                print("2. Compare Race Laptimes")
                print("3. Q3 Hotlaps")
                print("4. Speed/Throttle/Brake Comparison")
                print("5. Track Strength Comparison")
                print("6. Exit to Main Menu")
                command2 = int(input("Enter command: "))
                if command2 == 6:
                    break
                inner_menu(command2, searched_event)

            
    ##elif command == 2:
    ##elif command == 3:
    ##elif command == 4:
    elif command == 5:
        exit = True
    else:
        print("Bad input, try again")

print("Thanks for using!")
    
        
    
    
    
    
    