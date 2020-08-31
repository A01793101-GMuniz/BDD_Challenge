from tkinter import Tk
from tkinter.filedialog import askopenfilename, sys
from tkinter import messagebox


class AskWebDriver:

    def __init__(self):
        self.filename = None

    def ask_web_driver_folder_alert(self):
        result = messagebox.askquestion(title="No WebDriver on PATH",
                                        message="Do you wish to select a WebDriverFile",
                                        icon="warning")
        if result == "yes":
            self.filename = askopenfilename()
        else:
            sys.exit()
        return self.filename
