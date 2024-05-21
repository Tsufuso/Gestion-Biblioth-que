import customtkinter
from CTkTable import *
import mysql.connector
import tkinter
from GestionDeStock import *

def formulaire(id):
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")

    app = customtkinter.CTk()
    app.geometry("400x450")
    app.title("Insert Book Information")

    def create_label_and_entry(app, text, grid_row, grid_column, padx, pady):
        label = customtkinter.CTkLabel(app, text=text)
        label.grid(row=grid_row, column=grid_column, padx=padx, pady=pady)
        entry = customtkinter.CTkEntry(app)
        entry.grid(row=grid_row, column=grid_column + 1, padx=padx, pady=pady)
        return label, entry

    # Label and Entry for information
    label_titre, entry_titre = create_label_and_entry(app, "titre:", 1, 0, 10, 10)
    label_auteur, entry_auteur = create_label_and_entry(app, "auteur:", 2, 0, 10, 10)
    label_editeur, entry_editeur = create_label_and_entry(app, "editeur:", 3, 0, 10, 10)
    label_ISBN, entry_ISBN = create_label_and_entry(app, "ISBN:", 4, 0, 10, 10)
    label_NbrExemple, entry_NbrExemple = create_label_and_entry(
        app, "NbrExemplaire:", 5, 0, 10, 10
    )
    label_AnneePublication, entry_AnneePublication = create_label_and_entry(
        app, "AnneePublication:", 6, 0, 10, 10
    )
    label_LivrePresent, entry_LivrePresent = create_label_and_entry(app, "LivrePresent:", 7, 0, 10, 10)

    # Button to trigger the insertion function
    def insert_book():
        modifier_livre(
            id,
            entry_titre.get(),
            entry_auteur.get(),
            entry_editeur.get(),
            entry_ISBN.get(),
            entry_AnneePublication.get(),
            entry_NbrExemple.get(),
            entry_LivrePresent.get()
        )
        app.destroy()
        


    insert_button = customtkinter.CTkButton(
        app, text="modify Book", command=insert_book
    )
    insert_button.grid(row=12, column=1, columnspan=2, pady=20)

    app.mainloop()
    


def modifierlivre():

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
            text="Enter Id of the book you want to modify:", title="modify a book"
        )
        book_id_input = dialog.get_input()
        formulaire(book_id_input)
        root.destroy()

        
        
    # add a button to retriev the id of the book we want to delete
    button = customtkinter.CTkButton(master=root, text="modify a book",command=button_click)
    button.place(relx=0.5,rely=0.75,anchor=tkinter.CENTER)

    root.mainloop()