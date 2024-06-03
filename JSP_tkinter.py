# import tkinter
# import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.sidebar_button_1 = False
        self.sidebar_button_2 = False
        self.entry1_value = None
        self.entry2_value = None
        self.batch_value = 10
        self.epoch_value = 20
        self.ga_value3 = 30
        self.ga_value4 = 0.9
        self.ga_value5 = 0.2
        self.ga_value6 = 0.2
        self.ga_value7 = 2000
        
        # configure window
        self.title("Job Shop Scheduling.py")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        # self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_rowconfigure((1, 2), weight=1)
        self.grid_rowconfigure(0, weight=0)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Job Shop Scheduling", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_1_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_2_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        # self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        # self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry1 = customtkinter.CTkEntry(self, placeholder_text="input filename(eng)")
        self.entry1.grid(row=0, column=2, columnspan=2, padx=(20, 20), pady=(20, 170), sticky="nsew")
        self.entry2 = customtkinter.CTkEntry(self, placeholder_text="input filename(num)")
        self.entry2.grid(row=0, column=2, columnspan=2, padx=(20, 20), pady=(100, 90), sticky="nsew")
        self.main_button_e = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.get_entry_value)
        self.main_button_e.grid(row=0, column=3, padx=(0, 20), pady=(200, 20), sticky="nsew")
        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.main_button_1_event)
        self.main_button_1.grid(row=3, column=3, padx=(0, 20), pady=(0, 20), sticky="nsew")
        
        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=1, column=1, padx=(20, 0), pady=(10, 0), sticky="nsew")
        self.tabview.add("Deep Q Network")
        self.tabview.add("Genetic Algorithm")
        self.tabview.tab("Deep Q Network").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Genetic Algorithm").grid_columnconfigure(0, weight=1)

        self.string_input_1 = customtkinter.CTkEntry(self.tabview.tab("Deep Q Network"), width=300, placeholder_text="Batchsize default value is 10")
        self.string_input_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.string_input_2 = customtkinter.CTkEntry(self.tabview.tab("Deep Q Network"), width=300, placeholder_text="Epoch default value is 20")
        self.string_input_2.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.string_input_button_1 = customtkinter.CTkButton(self.tabview.tab("Deep Q Network"), fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),
                                                           command=self.input_dqn_value_event)
        self.string_input_button_1.grid(row=2, column=0, padx=20, pady=(70, 0))
        
        self.string_input_3 = customtkinter.CTkEntry(self.tabview.tab("Genetic Algorithm"), width=300, placeholder_text="Size of population default value is 30")
        self.string_input_3.grid(row=0, column=0, padx=20, pady=(0, 140))
        self.string_input_4 = customtkinter.CTkEntry(self.tabview.tab("Genetic Algorithm"), width=300, placeholder_text="Crossover Rate default value is 0.9")
        self.string_input_4.grid(row=0, column=0, padx=20, pady=(35, 105))
        self.string_input_5 = customtkinter.CTkEntry(self.tabview.tab("Genetic Algorithm"), width=300, placeholder_text="Mutation Rate default value is 0.2")
        self.string_input_5.grid(row=0, column=0, padx=20, pady=(70, 70))
        self.string_input_6 = customtkinter.CTkEntry(self.tabview.tab("Genetic Algorithm"), width=300, placeholder_text="Mutation selection rate default value is 0.2")
        self.string_input_6.grid(row=0, column=0, padx=20, pady=(105, 35))
        self.string_input_7 = customtkinter.CTkEntry(self.tabview.tab("Genetic Algorithm"), width=300, placeholder_text="Number of iteration default value is 2000")
        self.string_input_7.grid(row=0, column=0, padx=20, pady=(140, 0))
        self.string_input_button_2 = customtkinter.CTkButton(self.tabview.tab("Genetic Algorithm"), fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),
                                                           command=self.input_ga_value_event)
        self.string_input_button_2.grid(row=2, column=0, padx=20, pady=(10, 0))
        # self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Genetic Algorithm"), text="CTkLabel on QA")
        # self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)


        # set default values
        self.sidebar_button_1.configure(text="Deep Q Network")
        self.sidebar_button_2.configure(text="Genetic Algorithm")
        self.string_input_button_1.configure(text="Enter Parameters.")
        self.string_input_button_2.configure(text="Enter Parameters.")
        self.main_button_e.configure(text="Enter Filename.")
        self.main_button_1.configure(text="GET SCHEDULING!")
        # self.checkbox_3.configure(state="disabled")
        # self.checkbox_1.select()
        # self.scrollable_frame_switches[0].select()
        # self.scrollable_frame_switches[4].select()
        # self.radio_button_3.configure(state="disabled")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        # self.optionmenu_1.set("CTkOptionmenu")
        #self.combobox_1.set("CTkComboBox")
        # self.slider_1.configure(command=self.progressbar_2.set)
        # self.slider_2.configure(command=self.progressbar_3.set)
        # self.progressbar_1.configure(mode="indeterminnate")
        # self.progressbar_1.start()
        self.textbox.insert("0.0", "Job Shop Scheduling\n\n" + "Step.1  Select the Method: DQN or GA\n\n" 
                            + "Step.2  Input the filename\n\n"+ "Step.3  Modify the Model parameters\n\n"
                            + "-filename-\n"+ "abz:  5 ~ 9\n"+ "ft:      6, 10, 20\n"+ "la:      1 ~ 40\n"+ "swv:  1 ~ 20\n"+ "yn:     1 ~ 4\n")
        # self.seg_button_1.configure(values=["CTkSegmentedButton", "Value 2", "Value 3"])
        # self.seg_button_1.set("Value 2")
        
        self.frame_with_border = customtkinter.CTkFrame(self, corner_radius=7)
        self.frame_with_border.grid(row=1, column=2, columnspan=2, padx=(20, 20), pady=(27, 0), sticky="nsew")
        self.label_print = customtkinter.CTkLabel(self.frame_with_border, anchor='center', text='Message:', width=200)
        self.label_print.grid(padx=(80, 80), pady=(10, 0), sticky="nsew")
        
    def input_dqn_value_event(self):
        try:
            self.batch_value = int(self.string_input_1.get() or 10)
            self.epoch_value = int(self.string_input_2.get() or 20)
            self.label_print.configure(text=self.label_print.cget('text')+
                                       '\nBatchsize=%d , Epoch=%d'%(self.batch_value, self.epoch_value))
        except:
            self.label_print.configure(text=self.label_print.cget('text')+'\nCheck DQN parameters.')
        
    def input_ga_value_event(self):
        try:
            self.ga_value3 = int(self.string_input_3.get() or 30)
            self.ga_value4 = float(self.string_input_4.get() or 0.9)
            self.ga_value5 = float(self.string_input_5.get() or 0.2)
            self.ga_value6 = float(self.string_input_6.get() or 0.2)
            self.ga_value7 = int(self.string_input_7.get() or 2000)
            self.label_print.configure(text=self.label_print.cget('text')+
                                       '\nSize of population=%d,\n Crossover Rate=%.2f,\n Mutation Rate=%.2f,\n Mutation selection rate=%.2f,\n Number of iteration=%d'
                                       %(self.ga_value3, self.ga_value4, self.ga_value5, self.ga_value6, self.ga_value7))
        except:
            self.label_print.configure(text=self.label_print.cget('text')+'\nCheck GA parameters.')

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_1_event(self):
        self.sidebar_button_1 = True
        self.sidebar_button_2 = False
        self.label_print.configure(text=self.label_print.cget('text')+'\nSelect Deep Q Network')
        print("sidebar_button_1 click",self.sidebar_button_1,self.sidebar_button_2)
        
    def sidebar_button_2_event(self):
        self.sidebar_button_2 = True
        self.sidebar_button_1 = False
        self.label_print.configure(text=self.label_print.cget('text')+'\nSelect Genetic Algorithm')
        print("sidebar_button_2 click",self.sidebar_button_1,self.sidebar_button_2)
    
    def get_entry_value(self):
        self.entry1_value = self.entry1.get()
        try:
            self.entry2_value = int(self.entry2.get())
            self.label_print.configure(text=self.label_print.cget('text')+'\nenter filename')
        except:
            self.label_print.configure(text=self.label_print.cget('text')+'\nfilename(num) is wrong')
        print("main_button_1 click", self.entry1_value, self.entry2_value)
        return self.entry1_value, self.entry2_value
    
    def main_button_1_event(self):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
