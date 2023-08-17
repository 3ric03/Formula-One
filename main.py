from search import Search_Info
from datetime import datetime
from plotting import load_race_event

from plotting import plot_driver_race_laptime
from plotting import plot_laptimes_comparison
from plotting import plot_q3_flying_laps
from plotting import plot_telemetry_data

from analysis import analysis_menu
import fastf1

import customtkinter as customtk
from PIL import Image
    

f1_logo = my_image = customtk.CTkImage(light_image=Image.open("png/f1_logo.png"),
                                  size=(30, 30))

customtk.set_appearance_mode("dark")
customtk.set_default_color_theme("dark-blue")

entry_width = 300
button_width = 90
race = None
quali = None
plotType = -1

def load_gp (search_info):
    global race
    global quali
    race = search_info.get_race()
    quali = search_info.get_qualifying()
    race.load()
    quali.load()
    
class App (customtk.CTk):
    frames = {}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("F1 data Analysis")
        self.geometry("700x500")
        self.minsize(600,500)
        
        
        self.create_frames()
        self.display_frame(0)
        self.mainloop()
        
        
    def create_frames(self):
        self.frames[0] = MainMenu(self)
        self.frames[1] = RaceSearch(self)
        self.frames[2] = PlottingMenu(self)
        self.frames[3] = DriveSearch(self)
    
    def display_frame(self, frame_num):
        if hasattr(self, "current_frame"):
            self.current_frame.pack_forget()  # Hide the current frame
        
        self.current_frame = App.frames[frame_num]  # Set the current frame to the new frame
        self.current_frame.pack(fill="both", expand=True)    # Show the new frame
        
        
class RaceSearch(customtk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets(parent)
    
    def return_to_menu(self):
        self.master.display_frame(0)
        
    def load_grand_prix(self, year_entry, name_entry):
        
        year = int(year_entry.get())
        location = name_entry.get()
        
        search_obj = Search_Info(year, location, " ")
        searched_event = None
        bad_search = False
        try:
            searched_event = fastf1.get_event(search_obj._year, search_obj._location)
        except ValueError:
            print("Sorry, Event not found.")
            bad_search = True
            
            
        if not bad_search:
            load_gp(searched_event)
            self.master.display_frame(2)
            
        
    def create_widgets(self, parent):
        
        self.title = customtk.CTkLabel(self, text="Data Visualization Menu", font=("Helvetica", 20), compound="left").pack(pady=20)
        
        
        self.year_entry = customtk.CTkEntry(self, placeholder_text="Enter Year", width=entry_width)
        self.year_entry.pack(pady=10)
        
        self.name_entry = customtk.CTkEntry(self, placeholder_text="Enter Grand Prix Name", width=entry_width)
        self.name_entry.pack(pady=10)
        
        self.back_button = customtk.CTkButton(self, text="Back", width = button_width, command = self.return_to_menu)
        self.back_button.place(x=250, y=175)
        
        self.search_button = customtk.CTkButton(self, text="Search", width = button_width, command = lambda: self.load_grand_prix(self.year_entry, self.name_entry))
        self.search_button.place(x=360, y=175)

class DriveSearch(customtk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets(parent)
    
    def process_search(self, driver_entry):
        inputValue = driver_entry.get().split()
        if plotType == 1:
            plot_driver_race_laptime(race, (inputValue[0]))
        elif plotType == 2:
            plot_laptimes_comparison(race, inputValue[0], inputValue[1])
        elif plotType == 4 or plotType == 5:
            plot_telemetry_data(quali, inputValue[0], inputValue[1], plotType)
            
    def return_to_prev(self):
        self.master.display_frame(2)
        
    def create_widgets(self, parent):
        if plotType == 1:
            number = 1
        else:
            number = 2
            
        self.title = customtk.CTkLabel(self, text="Driver Search", font=("Helvetica", 20), compound="left").pack(pady=20)
        self.driver_entry = customtk.CTkEntry(self, placeholder_text="Enter " + str(number) + " Drivers", width=entry_width)
        self.driver_entry.pack(pady=10)
        
        self.search_button = customtk.CTkButton(self, text="Process", width = button_width, command = lambda: self.process_search(self.driver_entry))
        self.search_button.place(x=370, y=130)
        
        self.back_button = customtk.CTkButton(self, text="Back", width = button_width, command = self.return_to_prev)
        self.back_button.place(x=250, y=130)
        
    
class PlottingMenu(customtk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets(parent)
    
    def return_to_prev (self):
        self.master.display_frame(1)
    
    def display_plots (self, index):
        global plotType
        plotType = index
        self.master.display_frame(3)
        
    def view_hotlaps(self):
        plot_q3_flying_laps(quali)
    def create_widgets(self, parent):
        button_width = 300
        customtk.CTkLabel(self, text="Plotting Menu", font=("Helvetica", 20), compound="left").pack(pady=10)
        
        btn_race_laptimes = customtk.CTkButton(self, text="View Race Laptimes", width=button_width, 
                                               command = lambda: self.display_plots(1))
        btn_race_laptimes.pack(pady=5)

        btn_compare_laptimes = customtk.CTkButton(self, text="Compare Race Laptimes", width=button_width,
                                                  command = lambda: self.display_plots(2))
        btn_compare_laptimes.pack(pady=5)

        btn_view_hotlaps = customtk.CTkButton(self, text="View Q3 Hotlaps", width=button_width,
                                              command=self.view_hotlaps)
        btn_view_hotlaps.pack(pady=5)

        btn_telemetry = customtk.CTkButton(self, text="View Telemetry Data", width=button_width,
                                           command = lambda: self.display_plots(4))
        btn_telemetry.pack(pady=5)
        
        btn_track_strength = customtk.CTkButton(self, text="Track Strength Comparison", width=button_width,
                                                command = lambda: self.display_plots(5))
        btn_track_strength.pack(pady=5)

        btn_exit = customtk.CTkButton(self, text="Back", command=self.return_to_prev, width=button_width)
        btn_exit.pack(pady=10)
        
        toggle_display_mode = customtk.CTkSwitch(self, switch_height=15, switch_width=40, text = "Dark Mode", 
                                                 command=lambda: self.toggle_light_mode(toggle_display_mode) )
        toggle_display_mode.pack(pady=10)
        
    
        

        
        
        
        
        
class MainMenu(customtk.CTkFrame):
    
    def __init__(self, parent):
        super().__init__(parent)
        #self.pack(fill="both", expand=True)
        self.create_widgets(parent)
        
    def open_visualization(self, parent):
        # Code to open Race Data Visualization page
        self.pack_forget()
        self.master.display_frame(1)

    def toggle_light_mode(self, switch):
        if switch.get_value() == False:
            customtk.set_appearance_mode("dark")
        else:
            customtk.set_appearance_mode("light")
    def open_analysis(self):
        # Code to open Race Data Analysis page
        pass

    def open_past_search(self):
        # Code to open View past search page
        pass

    def open_set_driver(self):
        # Code to open Set favourite driver page
        pass

    def exit_program(self):
        self.quit()
    
    def create_widgets(self, parent):
        button_width = 300
        customtk.CTkLabel(self, text=" F1 Data Visualizer v1.1", font=("Helvetica", 20), compound="left").pack(pady=10)
        
        self.btn_visualization = customtk.CTkButton(self, text="Race Data Visualization", command=lambda: self.open_visualization(parent), width=button_width)
        self.btn_visualization.pack(pady=5)

        btn_analysis = customtk.CTkButton(self, text="Race Data Analysis", command=self.open_analysis, width=button_width)
        btn_analysis.pack(pady=5)

        btn_past_search = customtk.CTkButton(self, text="View Past Search (soon)", command=self.open_past_search, width=button_width, state="disabled")
        btn_past_search.pack(pady=5)

        btn_set_driver = customtk.CTkButton(self, text="Set Favourite Driver (soon)", command=self.open_set_driver, width=button_width, state = "disabled")
        btn_set_driver.pack(pady=5)

        btn_exit = customtk.CTkButton(self, text="Exit", command=self.exit_program, width=button_width)
        btn_exit.pack(pady=10)
        
        toggle_display_mode = customtk.CTkSwitch(self, switch_height=15, switch_width=40, text = "Dark Mode", 
                                                 command=lambda: self.toggle_light_mode(toggle_display_mode) )
        toggle_display_mode.pack(pady=10)
        

        
app = App()




    
    