import customtkinter
import mysql.connector
from GestionDeStock import *
import sys


def create_book_information_interface():
    conn = mysql.connector.connect(
        host="localhost", user="root", password="", database="python"
    )
    cursor = conn.cursor()

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

    # Button to trigger the insertion function
    def insert_book():
        insertion_livre(
            entry_titre.get(),
            entry_auteur.get(),
            entry_editeur.get(),
            entry_ISBN.get(),
            entry_AnneePublication.get(),
            entry_NbrExemple.get(),
        )
        app.destroy()

    insert_button = customtkinter.CTkButton(
        app, text="Insert Book", command=insert_book
    )
    insert_button.grid(row=8, column=1, columnspan=2, pady=20)

    app.mainloop()
