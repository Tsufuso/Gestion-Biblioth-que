import customtkinter as ctk
from CTkTable import *
import mysql.connector
from login_function import *
from Admin_Dashboard import PageGestionEleves
from Student_Dashboard import page_profile
import os
import sys

conn = mysql.connector.connect(
    host="localhost", user="root", password="", database="python"
)
mycursor = conn.cursor()


def login_page():
    class App(ctk.CTk):
        def __init__(self):
            super().__init__()

            self.title("Student Dashboard")
            self.geometry(f"{650}x{380}")

            self.username_label = ctk.CTkLabel(
                self, text="Username", font=("Roboto", 15)
            )
            self.username_label.pack()

            self.username_entry = ctk.CTkEntry(self)
            self.username_entry.pack()

            self.password_label = ctk.CTkLabel(
                self, text="Password", font=("Roboto", 15)
            )
            self.password_label.pack()

            self.password_entry = ctk.CTkEntry(self, show="*")
            self.password_entry.pack()

            self.login_button = ctk.CTkButton(
                self, text="Login", font=("Roboto", 15), command=self.button_click
            )
            self.login_button.pack(pady=12, padx=10)

        def button_click(self):
            username = self.username_entry.get()
            password = self.password_entry.get()

            login_result = login(username, password)

            if login_result == -2:
                # Account suspended
                print("Compte Suspendu")
                restart_program()
            elif login_result == 1:
                # Authenticated as an administrator
                print("1")
                # Hide the current window
                self.withdraw()

                # Pass a callback function to App2 to handle the return to App
                app2 = PageGestionEleves(login_result, return_callback=self.show_app)
                app2.protocol("WM_DELETE_WINDOW", app2.on_close)
                app2.mainloop()
            elif isinstance(login_result, int) and login_result > 1:
                # Authenticated as a normal user
                print(f"Student ID: {login_result}")
                self.withdraw()

                # Pass a callback function to App1 to handle the return to App
                app1 = page_profile(login_result, return_callback=self.show_app)
                app1.protocol("WM_DELETE_WINDOW", app1.on_close)
                app1.mainloop()
                return login_result
            elif login_result == -1:
                # Incorrect credentials
                print("Identifiants incorrects")
                restart_program()

        def show_app(self):
            self.deiconify()  # Show the window again
            self.destroy()

    app = App()
    return app

def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)

# Assume you have the necessary functions and modules imported
app = login_page()
app.mainloop()
