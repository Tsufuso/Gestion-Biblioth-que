import customtkinter
from CTkTable import *
import mysql.connector
from login_function import *
import sys
import os
from login_function import *
from Ajouter_livre import *
from suprimer_livre import *
from modifier_livre import *
from login import *
from historiqueEmprunt import *

conn = mysql.connector.connect(
    host="localhost", user="root", password="", database="python"
)
cursor = conn.cursor()
customtkinter.set_appearance_mode(
    "System"
)  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "blue"
)  # Themes: "blue" (standard), "green", "dark-blue"


# Page catalogue
def PageGestionEleves(login_result, return_callback):
    class App(customtkinter.CTk):
        def __init__(self, login_result, return_callback=None):
            super().__init__()

            # configure window
            self.title("Admin Dashboard")
            self.geometry(f"{800}x380")

            # configure grid layout (4x4)
            self.grid_columnconfigure(1, weight=1)
            self.grid_columnconfigure((2, 3), weight=0)
            self.grid_rowconfigure((0, 1, 2), weight=1)

            # create sidebar frame with widgets
            self.sidebar_frame = customtkinter.CTkFrame(
                self, width=140, corner_radius=0
            )
            self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
            self.sidebar_frame.grid_rowconfigure(4, weight=1)
            # Changer le nom en haut de la page
            self.label = customtkinter.CTkLabel(
                self.sidebar_frame,
                text="Gestion Élèves",
                font=customtkinter.CTkFont(size=20, weight="bold"),
            )
            self.label.grid(row=0, column=0, padx=20, pady=(20, 10))
            # Premier bouton ammenant ou profile
            self.Gestion_Eleves = customtkinter.CTkButton(
                self.sidebar_frame,
                text="Gestion Élèves",
                # command=self.redirect_to_Gestion_Eleve,
            )
            # caracteristique de boutton
            self.Gestion_Eleves.grid(row=1, column=0, padx=20, pady=10)
            # Deuxieme boutton du catalogue
            self.Emprunt_button = customtkinter.CTkButton(
                self.sidebar_frame,
                text="Gestion Emprunt",
                command=self.redirect_to_Emprunt,
            )
            # caracteristique de boutton
            self.Emprunt_button.grid(row=2, column=0, padx=20, pady=10)
            # Troisieme Boutton emprunt
            self.Emprunt_button = customtkinter.CTkButton(
                self.sidebar_frame,
                text="Gestion Livre",
                command=self.redirect_to_Livre,
            )
            # caracteristique de boutton
            self.Emprunt_button.grid(row=3, column=0, padx=20, pady=10)
            # bouton DeconexionP
            self.Deconexion_button = customtkinter.CTkButton(
                self.sidebar_frame,
                text="Deconnexion",  command=self.restart_program
            )
            # caracteristique de boutton
            self.Deconexion_button.grid(row=6, column=0, padx=20, pady=10)

            self.label = customtkinter.CTkLabel(
                self,
                text="Liste Élèves",
                font=customtkinter.CTkFont(size=20, weight="bold"),
            )
            self.label.grid(row=0, column=1, padx=(0, 0), pady=(0, 0), sticky="nsew")

            self.List_button = customtkinter.CTkButton(
                self, text="List Users", command=self.display_data_from_database
            )

            # caracteristique de boutton
            self.List_button.grid(row=0, column=2, padx=0, pady=0)

            self.Suspend_button = customtkinter.CTkButton(
                self, text="Suspend", command=self.suspend_user
            )

            # caracteristique de boutton
            self.Suspend_button.grid(row=2, column=2, padx=0, pady=0)

            self.Add_button = customtkinter.CTkButton(
                self,
                text="Add User",
                command=self.add_user,
            )

            self.Add_button.grid(row=3, column=2, padx=0, pady=0)


            # create table frame
            self.table_frame = customtkinter.CTkFrame(self)
            self.table_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
            self.return_callback = return_callback
            self.protocol("WM_DELETE_WINDOW", self.on_close)

        text = ""  # Define text at the class level

        def suspend_user(self):
            try:
                # Assuming user ID is an integer
                conn = mysql.connector.connect(
                    host="localhost", user="root", password="", database="python"
                )
                cursor = conn.cursor()

                # Get user ID from the input dialog
                dialog = customtkinter.CTkInputDialog(
                    text="Enter Id of the User:", title="Suspend User"
                )
                user_id_input = dialog.get_input()

                # Check if the user canceled the input
                if user_id_input is None:
                    return

                user_id = int(user_id_input)

                # Update the user's suspension status in the database
                cursor.execute(
                    f"UPDATE utilisateur SET is_suspended = 1 WHERE id = {user_id}"
                )

                # Commit the changes to the database
                conn.commit()

                # Close the cursor and connection
                cursor.close()
                conn.close()

                print(f"User with ID {user_id} suspended successfully.")

            except (ValueError, mysql.connector.Error) as e:
                print("Error:", e)

        def Delete_user(self):
            try:
                # Assuming user ID is an integer
                conn = mysql.connector.connect(
                    host="localhost", user="root", password="", database="python"
                )
                cursor = conn.cursor()

                # Get user ID from the input dialog
                dialog = customtkinter.CTkInputDialog(
                    text="Enter Id of the User:", title="Delete User"
                )
                user_id_input = dialog.get_input()

                # Check if the user canceled the input
                if user_id_input is None:
                    return

                user_id = int(user_id_input)

                # Update the user's suspension status in the database
                cursor.execute(f"drop column from utilisateur WHERE id = {user_id}")

                # Commit the changes to the database
                conn.commit()

                # Close the cursor and connection
                cursor.close()
                conn.close()

                print(f"User with ID {user_id} Deleted successfully.")

            except (ValueError, mysql.connector.Error) as e:
                print("Error:", e)

        def add_user(self):
            try:
                # Connect to the database
                conn = mysql.connector.connect(
                    host="localhost", user="root", password="", database="python"
                )
                cursor = conn.cursor()

                # Get user details from the input dialogs
                nom_dialog = customtkinter.CTkInputDialog(
                    text="Enter Nom:", title="Add User"
                )
                nom = nom_dialog.get_input()

                prenom_dialog = customtkinter.CTkInputDialog(
                    text="Enter Prenom:", title="Add User"
                )
                prenom = prenom_dialog.get_input()

                mail_dialog = customtkinter.CTkInputDialog(
                    text="Enter Mail:", title="Add User"
                )
                mail = mail_dialog.get_input()

                username_dialog = customtkinter.CTkInputDialog(
                    text="Enter Username:", title="Add User"
                )
                username = username_dialog.get_input()

                mdp_dialog = customtkinter.CTkInputDialog(
                    text="Enter Mot de Passe:",
                    title="Add User",
                )
                mdp = mdp_dialog.get_input()

                # Check if any of the input dialogs was canceled
                if None in (nom, prenom, mail, username, mdp):
                    return

                create_account(username, nom, prenom, mail, mdp)
                print("User added successfully.")

            except mysql.connector.Error as e:
                print("Error:", e)

        def redirect_to_Emprunt(self):
            self.withdraw()
            app1 = PageGestionEmprunt(login_result)
            app1.mainloop()

        def redirect_to_Livre(self):
            self.withdraw()
            app2 = PageGestionLivre(login_result)
            app2.mainloop()

        def restart_program(self):
            python = sys.executable
            os.execl(python, python, *sys.argv)
        
        def on_close(self):
            self.destroy()
            sys.exit()

        def display_data_from_database(self):
            conn = mysql.connector.connect(
            host="localhost", user="root", password="", database="python"
            )
            cursor = conn.cursor()
            # Fetch data from the database
            cursor.execute(
                "SELECT id, nom, username FROM utilisateur where is_suspended = 0"
            )

            # Fetch data
            data_from_database = cursor.fetchall()

            # Create a list to store the values from the database
            value = []

            # Update the value list with data from the database
            for row in data_from_database:
                # Add a new column for the suspend button (let's assume 'Suspend' is the button text)
                row_data = list(row)
                value.append(row_data)

            # Define column names
            column_names = ["ID utilisateur","Nom", "Username",]

            # Add column names to the beginning of the value list
            value.insert(0, column_names)
            
            # Clear the existing table
            for widget in self.table_frame.winfo_children():
                widget.destroy()

            # Check if the value list is not empty and has at least one row and one column
            if value and len(value) > 0 and len(value[0]) > 0:
                # Create the ble using the updated value list
                table = CTkTable(
                    master=self.table_frame,
                    row=len(value),
                    column=len(value[0]),
                    values=value,
                )
                table.pack(expand=False, fill="none", padx=20, pady=20)

            else:
                print("Error: Empty or invalid data from the database.")

    app = App(login_result, return_callback=return_callback)
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
    return App


def PageGestionEmprunt(login_result):
    # Page Gestion Emprunt
    class App1(customtkinter.CTk):
        def __init__(self, login_result):
            super().__init__()

            # configure window
            self.title("Gestion Emprunt")
            self.geometry(f"{650}x{380}")

            # configure grid layout (4x4)
            self.grid_columnconfigure(1, weight=1)
            self.grid_columnconfigure((2, 3), weight=0)
            self.grid_rowconfigure((0, 1, 2), weight=1)

            # create sidebar frame with widgets
            self.sidebar_frame = customtkinter.CTkFrame(
                self, width=140, corner_radius=0
            )
            self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
            self.sidebar_frame.grid_rowconfigure(4, weight=1)
            # Changer le nom en haut de la page
            self.label = customtkinter.CTkLabel(
                self.sidebar_frame,
                text="Gestion Emprunt",
                font=customtkinter.CTkFont(size=20, weight="bold"),
            )
            self.label.grid(row=0, column=0, padx=20, pady=(20, 10))
            # Premier bouton ammenant ou profile
            self.Profile_button = customtkinter.CTkButton(
                self.sidebar_frame,
                text="Gestion Élèves",
                command=self.redirect_to_Eleves,
            )
            # caracteristique de boutton
            self.Profile_button.grid(row=1, column=0, padx=20, pady=10)
            # Deuxieme boutton du catalogue
            self.Catalogue_button = customtkinter.CTkButton(
                self.sidebar_frame,
                text="Gestion Emprunt",
                # command=self.redirect_to_Catalogue,
            )
            # caracteristique de boutton
            self.Catalogue_button.grid(row=2, column=0, padx=20, pady=10)
            # Troisieme Boutton emprunt
            self.Emprunt_button = customtkinter.CTkButton(
                self.sidebar_frame,
                text="Gestion Livre",
                command=self.redirect_to_Livre,
            )
            # caracteristique de boutton
            self.Emprunt_button.grid(row=3, column=0, padx=20, pady=10)
            # bouton Deconexion
            self.Deconexion_button = customtkinter.CTkButton(
                self.sidebar_frame,
                text="Deconnexion",
                command=self.restart_program,
            )

            # caracteristique de boutton
            self.Deconexion_button.grid(row=6, column=0, padx=20, pady=10)

            self.table_frame = customtkinter.CTkFrame(self)
            self.table_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

            self.List_button = customtkinter.CTkButton(
                self,
                text="Liste Emprunt",
                command=self.display_data_from_database,
            )

            self.List_button.grid(row=0, column=1, padx=0, pady=0)

            self.Listh_button = customtkinter.CTkButton(
                self,
                text="Liste historique",
                command=self.display_data_from_database_h,
            )

            self.Listh_button.grid(row=3, column=1, padx=0, pady=0)

            self.Valid_button = customtkinter.CTkButton(
                self,
                text="Valider",
                command=self.Valid,
            )

            self.Valid_button.grid(row=0, column=2, padx=0, pady=0)

        
        def Valid(self):
            try:
                # user ID is an integer
                conn = mysql.connector.connect(
                    host="localhost", user="root", password="", database="python"
                )
                cursor = conn.cursor()

                # Get user ID from the input dialog
                dialog = customtkinter.CTkInputDialog(text="Valider:", title="Valider")
                Emprunt_id_input = dialog.get_input()

                # Check if the user canceled the input
                if Emprunt_id_input is None:
                    return

                Valid_id = int(Emprunt_id_input)

                print(f"{Valid_id}")
                cursor.execute("UPDATE emprunts SET is_validated=1 WHERE idEmprunt = %s", (Valid_id,))
                cursor.execute("UPDATE livre SET LivrePresent=LivrePresent+1 WHERE idLivre = (select id_livre FROM emprunts where idEmprunt=%s);", (Valid_id,))
            except (ValueError, mysql.connector.Error) as e:
                print("Error:", e)
            conn.commit()
            cursor.close()
            conn.close()
            try:
                # user ID is an integer
                conn = mysql.connector.connect(
                    host="localhost", user="root", password="", database="python"
                )
                cursor = conn.cursor()


                Valid_id = int(Emprunt_id_input)

                
                cursor.execute(
                    "UPDATE historique set is_validated=1 where id_emprunt=%s", (Valid_id,))


                # Commit the changes to the database
                conn.commit()

                # Close the cursor and connection
                cursor.close()
                conn.close()

            except (ValueError, mysql.connector.Error) as e:
                print("Error:", e)
            conn.commit()
            cursor.close()
            conn.close()

        def display_data_from_database_h(self):
            # user ID is an integer
            conn = mysql.connector.connect(
                host="localhost", user="root", password="", database="python"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * from historique ")

            # Fetch data
            data_from_database1 = cursor.fetchall()
            value = []
            for row in data_from_database1:
                # Add a new column for the suspend button (let's assume 'Suspend' is the button text)
                row_data = list(row)
                value.append(row_data)

            # Define column names
            column_names = ["ID Emprunt","ID utilisateur", "ID Livre", "Date d'emprunt", "Validé", "Dépassé",]

            # Add column names to the beginning of the value list
            value.insert(0, column_names)
            
            for widget in self.table_frame.winfo_children():
                widget.destroy()

            # Check if the value list is not empty and has at least one row and one column
            if value and len(value) > 0 and len(value[0]) > 0:
                # Create the table using the updated value list
                table = CTkTable(
                    master=self.table_frame,
                    row=len(value),
                    column=len(value[0]),
                    values=value,
                )
                table.pack(expand=False, fill="none", padx=20, pady=20)
            else:
                print("Error: Empty or invalid data from the database.")

        def display_data_from_database(self):
            conn = mysql.connector.connect(
                host="localhost", user="root", password="", database="python"
            )
            cursor = conn.cursor()

            # Fetch data from the database
            cursor.execute("SELECT * from emprunts ")

            # Fetch data
            data_from_database2 = cursor.fetchall()

            # Create a list to store the values from the database
            value = []

            # Update the value list with data from the database

            for row in data_from_database2:
                # Add a new column for the suspend button (let's assume 'Suspend' is the button text)
                row_data = list(row)
                value.append(row_data)

            # Define column names
            column_names = ["ID Emprunt","ID utilisateur", "ID Livre", "Date d'emprunt", "Validé", "Dépassé",]

            # Add column names to the beginning of the value list
            value.insert(0, column_names)
            
            # Clear the existing table
            for widget in self.table_frame.winfo_children():
                widget.destroy()

            # Check if the value list is not empty and has at least one row and one column
            if value and len(value) > 0 and len(value[0]) > 0:
                # Create the table using the updated value list
                table = CTkTable(
                    master=self.table_frame,
                    row=len(value),
                    column=len(value[0]),
                    values=value,
                )
                table.pack(expand=False, fill="none", padx=20, pady=20)
            else:
                print("Error: Empty or invalid data from the database.")

        def redirect_to_Livre(self):
            self.withdraw()
            app2 = PageGestionLivre(login_result)
            app2.mainloop()

        def redirect_to_Eleves(self):
            self.withdraw()
            app_instance = PageGestionEleves(
                login_result, return_callback=self.show_app
            )  # Use a different variable name
            app_instance.mainloop()

        def restart_program(self):
            python = sys.executable
            os.execl(python, python, *sys.argv)
        
        def show_app(self):
            self.deiconify()  # Show the window again
            self.destroy()

        def on_close(self):
            self.destroy()
            sys.exit()

    app = App1(login_result)
    app.mainloop()
    return App1


def PageGestionLivre(login_result):
    # Page Livre
    class App2(customtkinter.CTk):
        def __init__(self, login_result):
            super().__init__()

            # configure window
            self.title("Livre")
            self.geometry(f"{650}x{380}")

            # configure grid layout (4x4)
            self.grid_columnconfigure(1, weight=1)
            self.grid_columnconfigure((2, 3), weight=0)
            self.grid_rowconfigure((0, 1, 2), weight=1)

            # create sidebar frame with widgets
            self.sidebar_frame = customtkinter.CTkFrame(
                self, width=140, corner_radius=0
            )
            self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
            self.sidebar_frame.grid_rowconfigure(4, weight=1)
            # Changer le nom en haut de la page
            self.label = customtkinter.CTkLabel(
                self.sidebar_frame,
                text="Gestion Livre",
                font=customtkinter.CTkFont(size=20, weight="bold"),
            )
            self.label.grid(row=0, column=0, padx=20, pady=(20, 10))
            # Premier bouton ammenant ou profile
            self.Profile_button = customtkinter.CTkButton(
                self.sidebar_frame,
                text="Gestion Élèves",
                command=self.redirect_to_Eleves,
            )
            # caracteristique de boutton
            self.Profile_button.grid(row=1, column=0, padx=20, pady=10)
            # Deuxieme boutton du catalogue
            self.Catalogue_button = customtkinter.CTkButton(
                self.sidebar_frame,
                text="Gestion Emprunt",
                command=self.redirect_to_Emprunt,
            )
            # caracteristique de boutton
            self.Catalogue_button.grid(row=2, column=0, padx=20, pady=10)
            # Troisieme Boutton emprunt
            self.Emprunt_button = customtkinter.CTkButton(
                self.sidebar_frame,
                text="Gestion Livre",  # command=
            )
            # caracteristique de boutton
            self.Emprunt_button.grid(row=3, column=0, padx=20, pady=10)
            # bouton Deconexion
            self.Deconexion_button = customtkinter.CTkButton(
                self.sidebar_frame,
                text="Deconnexion",  command=self.restart_program
            )
            # caracteristique de boutton
            self.Deconexion_button.grid(row=6, column=0, padx=20, pady=10)
            # bouton ajouter Livre
            self.ajouter_Livre = customtkinter.CTkButton(
                self,
                text="Ajouter Livre",
                command=self.ajouterLivre,
            )
            # caracteristique de boutton
            self.ajouter_Livre.grid(row=0, column=1, padx=20, pady=10)
            self.suprimer_Livre = customtkinter.CTkButton(
                self,
                text="Supprimer Livre",
                command=self.suprimerLivre,
            )
            # caracteristique de boutton
            self.suprimer_Livre.grid(row=1, column=1, padx=20, pady=10)
            self.modifier_Livre = customtkinter.CTkButton(
                self,
                text="Modifier Livre",
                command=self.modifierLivre,
            )
            # caracteristique de boutton
            self.modifier_Livre.grid(row=2, column=1, padx=20, pady=5)
            self.protocol("WM_DELETE_WINDOW", self.on_close)

            self.login_result = login_result

        def modifierLivre(self):
            modifierlivre()

        def suprimerLivre(self):
            suprimerlivre()
            pass

        def ajouterLivre(self):
            create_book_information_interface()

        def redirect_to_Eleves(self):
            self.withdraw()
            app_instance = PageGestionEleves(
                login_result, return_callback=self.show_app
            )  # Use a different variable name
            app_instance.mainloop()

        def redirect_to_Emprunt(self):
            self.withdraw()
            App_Emprunt = PageGestionEmprunt(login_result)
            App_Emprunt.mainloop()

        def restart_program(self):
            python = sys.executable
            os.execl(python, python, *sys.argv)
        
        def on_close(self):
            self.destroy()
            sys.exit()

        def show_app(self):
            self.deiconify()  # Show the window again
            self.destroy()

    app = App2(login_result)

    app.mainloop()
    return App2


if __name__ == "__main__":
    app = PageGestionEleves()
    app.mainloop()
