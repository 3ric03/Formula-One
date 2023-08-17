import customtkinter as customtk
from PIL import Image
    
f1_logo = my_image = customtk.CTkImage(light_image=Image.open("png/f1_logo.png"),
                                  size=(30, 30))

customtk.set_appearance_mode("dark")
customtk.set_default_color_theme("dark-blue")


class App (customtk.CTk):
    frames = {}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("F1 data Analysis")
        self.geometry("700x500")
        self.minsize(600,500)
        self.create_frames()
        self.diplay_frame(0)
        self.mainloop()
        
        
    def create_frames(self):
        self.frames[0] = MainMenu(self)
        self.frames[1] = Visualization_menu(self)
    
    def diplay_frame(self, frame_num):
        if hasattr(self, "current_frame"):
            self.current_frame.pack_forget()  # Hide the current frame
        
        self.current_frame = App.frames[frame_num]  # Set the current frame to the new frame
        self.current_frame.pack(fill="both", expand=True)    # Show the new frame
        
        
class Visualization_menu(customtk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets(parent)
    
    def return_to_menu(self):
        self.master.diplay_frame(0)
        
        
    def create_widgets(self, parent):
        
        self.title = customtk.CTkLabel(self, text="Data Visualization Menu", font=("Helvetica", 20), compound="left").pack(pady=20)
        
        entry_width = 300
        button_width = 90
        self.year_entry = customtk.CTkEntry(self, placeholder_text="Enter Year", width=entry_width)
        self.year_entry.pack(pady=10)
        
        self.name_entry = customtk.CTkEntry(self, placeholder_text="Enter Grand Prix Name", width=entry_width)
        self.name_entry.pack(pady=10)
        
        self.back_button = customtk.CTkButton(self, text="Back", width = button_width, command = self.return_to_menu)
        self.back_button.place(x=250, y=175)
        
        self.search_button = customtk.CTkButton(self, text="Search", width = button_width)
        self.search_button.place(x=360, y=175)
    

class MainMenu(customtk.CTkFrame):
    
    def __init__(self, parent):
        super().__init__(parent)
        #self.pack(fill="both", expand=True)
        self.create_widgets(parent)
        
    def open_visualization(self, parent):
        # Code to open Race Data Visualization page
        self.pack_forget()
        self.master.diplay_frame(1)

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
        
        print("reach")
        self.btn_visualization = customtk.CTkButton(self, text="Race Data Visualization", command=lambda: self.open_visualization(parent), width=button_width)
        self.btn_visualization.pack(pady=5)

        btn_analysis = customtk.CTkButton(self, text="Race Data Analysis", command=self.open_analysis, width=button_width)
        btn_analysis.pack(pady=5)

        btn_past_search = customtk.CTkButton(self, text="View past search", command=self.open_past_search, width=button_width)
        btn_past_search.pack(pady=5)

        btn_set_driver = customtk.CTkButton(self, text="Set favourite driver", command=self.open_set_driver, width=button_width)
        btn_set_driver.pack(pady=5)

        btn_exit = customtk.CTkButton(self, text="Exit", command=self.exit_program, width=button_width)
        btn_exit.pack(pady=10)
        
        toggle_display_mode = customtk.CTkSwitch(self, switch_height=10, switch_width=20)

        
app = App()







