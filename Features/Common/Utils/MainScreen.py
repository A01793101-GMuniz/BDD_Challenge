import glob
import os
import tkinter as tk
from tkinter.ttk import Combobox


class MainScreen:

    def __init__(self, feature_path):
        self.root = tk.Tk()
        self.root.title("BDD Framework")
        self.root.geometry('450x300')

        # --------------------------Elements of Window --------------------------#

        self.available_features_label = \
            tk.Label(text="Features", font="Helvetica 16 bold italic").place(x=10, y=0)
        self.browsers_label = \
            tk.Label(text="Choose a Browser", font="Helvetica 16 bold italic").place(x=250, y=0)
        self.features_combo = Combobox(self.root)
        self.browsers_combo = Combobox(self.root)
        self.feature_path = feature_path + "/Features"
        os.chdir(self.feature_path)
        self.feature_files = []
        for file in glob.glob("*.feature"):
            self.feature_files.append(file)
        self.features_combo["values"] = self.feature_files
        self.browsers_combo["values"] = ("Chrome", "Firefox", "Edge", "Safari")
        self.features_combo.current(0)
        self.features_combo.place(x=10, y=50)
        self.browsers_combo.current(0)
        self.browsers_combo.place(x=250, y=50)

        self.btn_image = tk.PhotoImage(file=f"{feature_path}/Features/Common/Utils/start_button_image.gif")
        self.start_test_button = \
            tk.Button(self.root, text="Start Test", command=self.click_start_test_button)
        self.start_test_button.config(image=self.btn_image,width="130", height="130")

        self.start_test_button.place(x=130, y=150)

        # --------------------------Wrap Element of Window and Display --------------------------#
        self.root.mainloop()

    def click_start_test_button(self):
        self.feature_to_run = self.features_combo.get()
        self.browser_to_run = self.browsers_combo.get()
        print("Running Feature...")
        self.root.destroy()
