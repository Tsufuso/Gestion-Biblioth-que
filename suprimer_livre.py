import customtkinter
from CTkTable import *
import mysql.connector
import tkinter
from GestionDeStock import *


def suprimerlivre():
    # Connect to the database
    conn = mysql.connector.connect(
        host="localhost", user="root", password="", database="python"
    )

    # Create a cursor
    cursor = conn.cursor()
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")
    # Window
    root = customtkinter.CTk()

    root.geometry("850x240")

    # Fetch data from the database
    cursor.execute("SELECT * FROM livre")

    # Fetch the data
    data_from_database = cursor.fetchall()

    # Create a list to store the values from the database
    value = []

    # Update the value list with data from the database
    for row in data_from_database:
        value.append(list(row))

    # Create the CTkTable using the updated value list
    table = CTkTable(master=root, row=len(value), column=len(value[0]), values=value)
    table.pack(expand=False, fill="both", padx=20, pady=20)

    def button_click():
        # Get user ID from the input dialog
        dialog = customtkinter.CTkInputDialog(
            text="Enter Id of the book you want to delete:", title="delete a book"
        )
        book_id_input = dialog.get_input()
        # call the delete function
        supprimer_livre(book_id_input)
        root.destroy()


    # add a button to retriev the id of the book we want to delete
    button = customtkinter.CTkButton(
        master=root, text="delete a book", command=button_click
    )
    button.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)

    root.mainloop()
