from src.search import Search_Info

from src.plotting import plot_driver_race_laptime
from src.plotting import plot_laptimes_comparison
from src.plotting import plot_q3_flying_laps
from src.plotting import plot_telemetry_data

from src.analysis import practise_pace_plotter
from src.analysis import tyre_dict
from src.analysis import race_pace_plotter

import fastf1

import customtkinter as customtk
from PIL import Image
    

f1_logo = my_image = customtk.CTkImage(light_image=Image.open("png/f1_logo.png"),
                                  size=(30, 30))

customtk.set_appearance_mode("dark")
customtk.set_default_color_theme("dark-blue")

entry_width = 300
entry_width_narrow = 245
button_width = 90
analysis = False
race = None
quali = None
searched_event = None
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
        self.title("F1 Data Analysis")
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
        self.frames[4] = AnalysisMenu(self)
    
    def display_frame(self, frame_num):
        if hasattr(self, "current_frame"):
            self.current_frame.pack_forget()  # Hide the current frame
            if self.current_frame == App.frames[3]:
                for widget in self.current_frame.winfo_children():
                    widget.destroy()
        
        self.current_frame = App.frames[frame_num]  # Set the current frame to the new frame
        if frame_num == 3:
            self.current_frame.create_widgets()
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
        global searched_event
        bad_search = False
        try:
            searched_event = fastf1.get_event(search_obj._year, search_obj._location)
        except ValueError:
            print("Sorry, Event not found.")
            bad_search = True
            
            
        if not bad_search:
            load_gp(searched_event)
            if analysis:
                print("reached")
                self.master.display_frame(4)
            else:
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
    chosen_tyre = None
    tyre_selector = None
    def __init__(self, parent):
        super().__init__(parent)
        
    
    def process_search(self, driver_entry):
        
        inputValue = driver_entry.get().split()
        if plotType == 1:
            plot_driver_race_laptime(race, (inputValue[0]))
            
        elif plotType == 2:
            plot_laptimes_comparison(race, inputValue[0], inputValue[1])
            
        elif plotType == 4 or plotType == 5:
            plot_telemetry_data(quali, inputValue[0], inputValue[1], plotType)
            
        elif plotType == 6:
            fp1 = searched_event.get_practice(1)
            fp2 = searched_event.get_practice(2)
            fp1.load()
            fp2.load()
            self.select_tyre()
            tyre = tyre_dict[self.chosen_tyre]
            practise_pace_plotter(fp1, fp2, inputValue, tyre)
            
        elif plotType == 7:
            race_pace_plotter(race, inputValue)
            
            
    def return_to_prev(self):
        if plotType == 6 or plotType == 7:
            self.master.display_frame(4)
        else:
            self.master.display_frame(2)
    def select_tyre(self):
        self.chosen_tyre = self.tyre_selector.get()
        print(self.chosen_tyre)
    
    def create_widgets(self):
        tyre_select = False
        
        if plotType == 6 or plotType == 7:
            if plotType == 6:
                tyre_select = True
            number = 4
        elif plotType == 1:
            number = 1
        else:
            number = 2
        
        if tyre_select:
            title = "Driver & Tyre Selection"
        else:
            title = "Driver Selection"
        
        self.title = customtk.CTkLabel(self, text=title, font=("Helvetica", 20), compound="left").pack(pady=20)
        
        self.driver_entry = customtk.CTkEntry(self, placeholder_text="Enter " + str(number) + " Driver Numbers:", width=entry_width_narrow)
        self.driver_entry.pack(pady=10)
        
        self.search_button = customtk.CTkButton(self, text="Process", width = button_width, command = lambda: self.process_search(self.driver_entry))
        self.back_button = customtk.CTkButton(self, text="Back", width = button_width, command = self.return_to_prev)

        
        if tyre_select:
            self.tyre_selector = customtk.CTkSegmentedButton(self, 
                                     values=["Soft Tyre", "Medium Tyre", "Hard Tyre"])
            self.tyre_selector.pack(pady=10)
            self.search_button.place(x=365, y=180)
            self.back_button.place(x=245, y=180)
        else:
            self.search_button.place(x=370, y=130)
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
        
    
        
class AnalysisMenu(customtk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets(parent)
    
    def return_to_prev (self):
        self.master.display_frame(1)
        
    def display_plots (self, index):
        global plotType
        plotType = index
        self.master.display_frame(3)
        
        
    def create_widgets(self, parent):
        button_width = 300
        customtk.CTkLabel(self, text="Analysis Menu", font=("Helvetica", 20), compound="left").pack(pady=10)
        
        btn_fp_analysis = customtk.CTkButton(self, text="Race Pace Analysis - Free Practise", width=button_width, 
                                               command = lambda: self.display_plots(6))
        btn_fp_analysis.pack(pady=5)

        btn_race_analysis = customtk.CTkButton(self, text="Race Pace Analysis - Race", width=button_width,
                                                  command = lambda: self.display_plots(7))
        btn_race_analysis.pack(pady=5)

        btn_tyre_deg = customtk.CTkButton(self, text="Tyre Degradation Analysis (Coming Soon)", width=button_width,
                                                  state="disabled")
        btn_tyre_deg.pack(pady=5)

        btn_exit = customtk.CTkButton(self, text="Back", command=self.return_to_prev, width=button_width)
        btn_exit.pack(pady=10)
        
        
class MainMenu(customtk.CTkFrame):
    
    def __init__(self, parent):
        super().__init__(parent)
        #self.pack(fill="both", expand=True)
        self.create_widgets(parent)
        
    def open_visualization(self, parent):
        # Code to open Race Data Visualization page
        global analysis
        analysis = False
        self.pack_forget()
        self.master.display_frame(1)

    def toggle_light_mode(self, switch):
        if switch.get_value() == False:
            customtk.set_appearance_mode("dark")
        else:
            customtk.set_appearance_mode("light")
    def open_analysis(self):
        # Code to open Race Data Analysis page
        global analysis
        analysis = True
        self.master.display_frame(1)

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
        
        toggle_display_mode = customtk.CTkSwitch(self, switch_height=15, switch_width=40, text = "Light Mode", 
                                                 command=lambda: self.toggle_light_mode(toggle_display_mode) )
        toggle_display_mode.pack(pady=10)
        

        
app = App()




    
    