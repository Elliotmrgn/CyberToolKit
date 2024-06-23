import os
import platform
from title import title
from portscan import PortScan
from robotscan import RobotsScanner



class Menu:
    def __init__(self, options):
        self.options = options
        
    def clear(self):
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')
            
    def display_menu(self):
        print(title())
        for i, option in enumerate(options, 1):
            print(f"{i}) {option["name"]}")
        print("0) Quit")
    
    def get_choice(self):
        choice = input("Enter your choice: ")
        try:
            choice = int(choice)
            if 0 <= choice <= len(self.options):
                return choice
            else:
                print("Invalid choice. Please try again.")
                return self.get_choice()
        except ValueError:
            print("Invalid input. Please enter a number.")
            return self.get_choice()
        
        
    def run(self):
        self.clear()
        self.display_menu()
        choice = self.get_choice()
        if choice == 0:
            print("Exiting the program. Goodbye!")
            return
        else:
            self.options[choice - 1]['action']()

        
if __name__ == "__main__":
    options = [
        {"name": "Port Scanner", "action": PortScan().run},
        {"name": "Robot Search", "action": RobotsScanner().run},
        
    ]
    menu = Menu(options)
    menu.run()