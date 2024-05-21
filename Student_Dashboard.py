import customtkinter
import mysql.connector
from login_function import *
import sys
from CTkTable import *
from login import *
import os
import sys

customtkinter.set_appearance_mode(
    "dark"
)  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "blue"
)  # Themes: "blue" (standard), "green", "dark-blue"


def page_catalogue(login_result):
    # Page Catalogue
    class App(customtkinter.CTk):
        def __init__(self, login_result):
            super().__init__()
            self.conn = None
            self.cursor = None
            # configure window
            self.title("Student Dashboard")
            self.geometry(f"{650}x{380}")
            # configure grid layout (4x4)
            self.grid_columnconfigure(1, weight=1)
            self.grid_columnconfigure((2, 3), weight=0)
            self.grid_rowconfigure((0, 1, 2), weight=1)
            # create sidebar frame with widgets
            self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
            self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
            self.sidebar_frame.grid_rowconfigure(4, weight=1)
            # Changer le nom en haut de la page
            self.label = customtkinter.CTkLabel(
                self.sidebar_frame,
                text="Catalogue",
                font=customtkinter.CTkFont(size=20, weight="bold"),
            )
            self.label.grid(row=0, column=0, padx=20, pady=(20, 10))
            # Premier bouton ammenant ou profile
            self.Profile_button = customtkinter.CTkButton(
                self.sidebar_frame,
                text="Profile",
                command=self.redirect_to_Profile,  # add command to redirect to App1()
            )
            # caracteristique de boutton
            self.Profile_button.grid(row=1, column=0, padx=20, pady=10)
            # Deuxieme boutton du catalogue
            self.Catalogue_button = customtkinter.CTkButton(
                self.sidebar_frame,
                text="Catalogue",  # command=
            )
            # caracteristique de boutton
            self.Catalogue_button.grid(row=2, column=0, padx=20, pady=10)
            # Troisieme Boutton emprunt
            self.Emprunt_button = customtkinter.CTkButton(
                self.sidebar_frame,
                text="Emprunt",
                command=self.redirect_to_Emprunt,
            )
            # caracteristique de boutton
            self.Emprunt_button.grid(row=3, column=0, padx=20, pady=10)
            # bouton Deconnexion
            self.Deconnexion_button = ctk.CTkButton(
                self.sidebar_frame,
                text="Deconnexion",
                command=self.restart_program,
            )

            # caracteristique de bouton
            self.Deconnexion_button.grid(row=6, column=0, padx=20, pady=10)
            self.protocol("WM_DELETE_WINDOW", self.on_close)
            self.setup_widgets()

            self.label_livre = customtkinter.CTkLabel(
                self,
                text="Liste des Livres",
                font=customtkinter.CTkFont(size=20, weight="bold"),
            )
            self.label_livre.grid(row=0, column=1, padx=(0, 0), pady=(0, 0), sticky="nsew")

            self.table_frame = customtkinter.CTkFrame(self)
            self.table_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

            self.emprunt_button = customtkinter.CTkButton(
                self, text="Emprunter", command=self.Emprunt_book
            )
            self.emprunt_button.grid(row=2, column=1, padx=(0, 5), pady=5, sticky="e")

            self.List_button = customtkinter.CTkButton(
                self, text="Afficher Livres", command=self.display_data_from_database
            )
            self.List_button.grid(row=2, column=1, padx=(5, 0), pady=5, sticky="w")

            self.login_result = login_result

        def setup_widgets(self):
            # Label pour afficher le message si le nombre d'emprunts est dépassé
            self.limit_message_label = customtkinter.CTkLabel(
                self, text="", font=customtkinter.CTkFont(size=12)
            )
            self.limit_message_label.grid(row=4, column=1, columnspan=2, padx=20, pady=5)

        def connect_to_database(self):
            try:
                self.conn = mysql.connector.connect(
                    host="localhost", user="root", password="", database="python"
                )
                self.cursor = self.conn.cursor()
                print("Connected to database successfully!")
            except mysql.connector.Error as e:
                print("Error connecting to database:", e)

        def close_connection(self):
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
                print("Database connection closed.")

        def display_data_from_database(self):
            value = []  # Initialisation de la variable value pour stocker les données
            try:
                if not self.conn or not self.cursor:
                    self.connect_to_database()

                # Fetch data from the database
                if self.cursor:
                    self.cursor.execute(
                        "SELECT idLivre, titre, auteur, editeur, ISBN, LivrePresent FROM livre WHERE LivrePresent > 0 "
                    )
                    data_from_database = self.cursor.fetchall()

                    # Update the value list with data from the database
                    for row in data_from_database:
                        row_data = list(row)
                        value.append(row_data)

                    # Define column names
                    column_names = ["ID Livre","Titre du Livre", "Auteur", "Editeur", "ISBN", "Exemplaires Restants",]

                    # Add column names to the beginning of the value list
                    value.insert(0, column_names)
                    
                    # Clear the existing table
                    for widget in self.table_frame.winfo_children():
                        widget.destroy()

                    # Check if the value list is not empty and has at least one row and one column
                    if value and len(value) > 0 and len(value[0]) > 0:
                        # Create the CTkTable using the updated value list
                        table = CTkTable(
                            master=self.table_frame,
                            row=len(value),
                            column=len(value[0]),
                            values=value,
                        )
                        table.pack(expand=False, fill="none", padx=20, pady=20)
                    else:
                        print("Error: Empty or invalid data from the database")

            except mysql.connector.Error as e:
                print("Error:", e)
            finally:
                # Ne fermez pas la connexion ici
                pass

        def update_book_list(self):
            # Méthode pour mettre à jour la liste des livres
            self.display_data_from_database()
            

        def Emprunt_book(self):
            try:
                if not self.conn or not self.cursor:
                    self.connect_to_database()

                user_id = login_result  # Remplacez par l'ID de l'utilisateur

                # Vérifier si l'utilisateur a déjà emprunté trois livres non validés
                self.cursor.execute(
                    f"SELECT COUNT(*) FROM emprunts WHERE id_utilisateur = {user_id} AND is_validated = 0"
                )
                current_unvalidated_borrowed = self.cursor.fetchone()[0]
                max_borrow_allowed = 3

                if current_unvalidated_borrowed >= max_borrow_allowed:
                    self.limit_message_label.configure(
                        text="Vous avez atteint la limite de tentatives d'emprunt.",
                        style="custom.TLabel",
                    )
                    return

                # Récupérer l'ID du livre à emprunter depuis l'utilisateur
                dialog = customtkinter.CTkInputDialog(
                    text="Entrez l'ID du livre que vous voulez emprunter:",
                    title="Emprunter Livre",
                )
                book_id_input = dialog.get_input()

                if book_id_input is None:
                    return

                book_id = int(book_id_input)

                # Récupérer LivrePresent actuel depuis la base de données
                self.cursor.execute(
                    f"SELECT LivrePresent FROM livre WHERE idLivre = {book_id}"
                )
                current_livre_present = self.cursor.fetchone()[0]

                # Vérifier si le livre est disponible (LivrePresent > 0)
                if current_livre_present > 0:
                    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Mettre à jour LivrePresent à LivrePresent - 1 et ajouter l'emprunt à la table 'emprunts'
                    updated_livre_present = current_livre_present - 1
                    self.cursor.execute(
                        f"UPDATE livre SET LivrePresent = {updated_livre_present} WHERE idLivre = {book_id}"
                    )
                    self.cursor.execute(
                        f"INSERT INTO emprunts (id_utilisateur, id_livre, date_emprunt, is_validated) VALUES ({user_id}, {book_id}, '{current_date}', 0)"
                    )
                    self.conn.commit()

                    print(f"Livre avec l'ID {book_id} emprunté avec succès.")
                    # Actualiser la liste après l'emprunt du livre
                    self.update_book_list()

                else:
                    print("Ce livre n'est pas disponible.")

            except (ValueError, mysql.connector.Error) as e:
                print("Erreur :", e)

        def on_close(self):
            self.destroy()
            sys.exit()

        def redirect_to_Profile(self):
            self.withdraw()
            app1 = page_profile(login_result, return_callback=self.show_app)
            app1.mainloop()

        def redirect_to_Emprunt(self):
            self.withdraw()
            app_Emprunt = page_emprunt(login_result)
            app_Emprunt.mainloop()
            
        def restart_program(self):
            python = sys.executable
            os.execl(python, python, *sys.argv)
        
        def show_app(self):
            self.deiconify()  # Show the window again
            self.destroy()    

    # Instantiate the App class
    app = App(login_result)
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()


# Page Profile
def page_profile(login_result, return_callback):
    class App1(ctk.CTk):
        def __init__(self, login_result, return_callback=None):
            super().__init__()
            # configure window
            self.title("Profile")
            self.geometry(f"{650}x{380}")
            # configure grid layout (4x4)
            self.grid_columnconfigure(1, weight=1)
            self.grid_columnconfigure((2, 3), weight=0)
            self.grid_rowconfigure((0, 1, 2), weight=1)
            # create sidebar frame with widgets
            self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
            self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
            self.sidebar_frame.grid_rowconfigure(4, weight=1)
            # Changer le nom en haut de la page
            self.label = ctk.CTkLabel(
                self.sidebar_frame,
                text="Profile",
                font=ctk.CTkFont(size=20, weight="bold"),
            )
            self.label.grid(row=0, column=0, padx=20, pady=(20, 10))
            # Premier bouton ammenant ou profile
            self.Profile_button = ctk.CTkButton(
                self.sidebar_frame,
                text="Profile",
            )
            # caracteristique de bouton
            self.Profile_button.grid(row=1, column=0, padx=20, pady=10)
            # Deuxieme boutton du catalogue
            self.Catalogue_button = ctk.CTkButton(
                self.sidebar_frame,
                text="Catalogue",
                command=self.redirect_to_Catalogue,
            )
            # caracteristique de bouton
            self.Catalogue_button.grid(row=2, column=0, padx=20, pady=10)
            # Troisieme Boutton emprunt
            self.Emprunt_button = ctk.CTkButton(
                self.sidebar_frame,
                text="Emprunt",
                command=self.redirect_to_Emprunt,
            )
            # caracteristique de bouton
            self.Emprunt_button.grid(row=3, column=0, padx=20, pady=10)
            # bouton Deconnexion
            self.Deconnexion_button = ctk.CTkButton(
                self.sidebar_frame,
                text="Deconnexion",
                command=self.restart_program,
            )
            
            # caracteristique de bouton
            self.Deconnexion_button.grid(row=6, column=0, padx=20, pady=10)
            self.protocol("WM_DELETE_WINDOW", self.on_close)

            # Set the callback function to be called when this window is closed
            self.return_callback = return_callback
            self.login_result = login_result

            # Partie droite de la fenêtre pour afficher le profil
            self.profile_frame = customtkinter.CTkFrame(self)
            self.profile_frame.grid(row=0, column=1, rowspan=6, sticky="nsew")

            self.nom_label = customtkinter.CTkLabel(self.profile_frame, text="Nom: ")
            self.nom_label.grid(row=2, column=1, padx=20, pady=10)

            self.prenom_label = customtkinter.CTkLabel(self.profile_frame, text="Prénom: ")
            self.prenom_label.grid(row=3, column=1, padx=20, pady=10)

            self.mail_label = customtkinter.CTkLabel(self.profile_frame, text="Mail: ")
            self.mail_label.grid(row=4, column=1, padx=20, pady=10)

            self.username_label = customtkinter.CTkLabel(self.profile_frame, text="Nom d'utilisateur: ")
            self.username_label.grid(row=5, column=1, padx=20, pady=10)

            self.show_profile_button = customtkinter.CTkButton(
            self,
            text="Afficher mon Profile",
            command=self.display_user_profile,
            )
            self.show_profile_button.grid(row=6, column=1, padx=20, pady=10)

            

        def connect_to_database(self):
            try:
                self.conn = mysql.connector.connect(
                host="localhost", user="root", password="", database="python"
                )
                self.cursor = self.conn.cursor()
                print("Connected to database successfully!")
            except mysql.connector.Error as e:
                print("Error connecting to database:", e)

        def close_connection(self):
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
                print("Database connection closed.")

        def display_user_profile(self):

            user_id = self.login_result

            # Connectez-vous à la base de données
            self.connect_to_database()
    
            # Remplacez 'YOUR_TABLE_NAME' par le nom de votre table contenant les données de l'utilisateur
            query = "SELECT id, nom, prenom, mail, username FROM utilisateur WHERE id = %s"

            try:
                self.cursor.execute(query, (user_id,))
                user_data = self.cursor.fetchone()  # Récupérer les données de l'utilisateur

                # Afficher les détails de l'utilisateur dans l'interface
                self.nom_label.configure(text=f"Nom: {user_data[1]}")
                self.prenom_label.configure(text=f"Prénom: {user_data[2]}")
                self.mail_label.configure(text=f"Mail: {user_data[3]}")
                self.username_label.configure(text=f"Nom d'utilisateur: {user_data[4]}")
            except mysql.connector.Error as e:
                print("Error fetching user data:", e)
            
            # Fermer la connexion à la base de données
            self.close_connection()
        
        
        def redirect_to_Catalogue(self):
            self.withdraw()
            app = page_catalogue(login_result)
            app.mainloop()
        
        def redirect_to_Emprunt(self):
            self.withdraw()
            app2 = page_emprunt(login_result)
            app2.mainloop()

        def restart_program(self):
            python = sys.executable
            os.execl(python, python, *sys.argv)
        
        def on_close(self):
            self.destroy()
            sys.exit()

    app1 = App1(login_result, return_callback=return_callback)
    app1.protocol("WM_DELETE_WINDOW", app1.on_close)
    app1.mainloop()


def page_emprunt(login_result):
    class App2(ctk.CTk):
        def __init__(self, login_result):
            super().__init__()
            # configure window
            self.title("Emprunt")
            self.geometry(f"{650}x{380}")
            # configure grid layout (4x4)
            self.grid_columnconfigure(1, weight=1)
            self.grid_columnconfigure((2, 3), weight=0)
            self.grid_rowconfigure((0, 1, 2), weight=1)
            # create sidebar frame with widgets
            self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
            self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
            self.sidebar_frame.grid_rowconfigure(4, weight=1)
            # Changer le nom en haut de la page
            self.label = ctk.CTkLabel(
                self.sidebar_frame,
                text="Liste Emprunt",
                font=ctk.CTkFont(size=20, weight="bold"),
            )
            self.label.grid(row=0, column=0, padx=20, pady=(20, 10))
            # Premier bouton ammenant ou profile
            self.Profile_button = ctk.CTkButton(
                self.sidebar_frame,
                text="Profile",
                command=self.redirect_to_Profile,
            )
            # caracteristique de bouton
            self.Profile_button.grid(row=1, column=0, padx=20, pady=10)
            # Deuxieme boutton du catalogue
            self.Catalogue_button = ctk.CTkButton(
                self.sidebar_frame,
                text="Catalogue",
                command=self.redirect_to_Catalogue,
            )
            # caracteristique de bouton
            self.Catalogue_button.grid(row=2, column=0, padx=20, pady=10)
            # Troisieme Boutton emprunt
            self.Emprunt_button = ctk.CTkButton(
                self.sidebar_frame,
                text="Emprunt", #command=
            )

            self.label_livre = customtkinter.CTkLabel(
                self,
                text="Liste Emprunt",
                font=customtkinter.CTkFont(size=20, weight="bold"),
            )
            self.label_livre.grid(row=0, column=1, padx=(0, 0), pady=(0, 0), sticky="nsew")

            self.table_frame = customtkinter.CTkFrame(self)
            self.table_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

            self.emprunt2_button = customtkinter.CTkButton(
                self, text="Emprunts en cours", command=self.display_user_borrowed_books
            )
            self.emprunt2_button.grid(row=2, column=1, padx=(5, 0), pady=5, sticky="w")

            self.historique_button = customtkinter.CTkButton(
                self, text="Historique Emprunt", command=self.display_user_history_books
            )
            self.historique_button.grid(row=2, column=1, padx=(0, 5), pady=5, sticky="e")

            # caracteristique de bouton
            self.Emprunt_button.grid(row=3, column=0, padx=20, pady=10)
            # bouton Deconnexion
            self.Deconnexion_button = ctk.CTkButton(
                self.sidebar_frame,
                text="Deconnexion",
                command=self.restart_program,
            )

            # caracteristique de bouton
            self.Deconnexion_button.grid(row=6, column=0, padx=20, pady=10)
            self.protocol("WM_DELETE_WINDOW", self.on_close)

            self.login_result = login_result

        def display_user_borrowed_books(self):
            # Créer une connexion à la base de données
            conn = mysql.connector.connect(
                host="localhost", user="root", password="", database="python"
            )
            # Créer un curseur pour exécuter des requêtes SQL
            cursor = conn.cursor()

            user_id = login_result

            # Exécuter la requête SQL pour récupérer les emprunts de l'utilisateur
            sql = "SELECT emprunts.idEmprunt, livre.titre, emprunts.date_emprunt FROM emprunts JOIN livre ON emprunts.id_livre = livre.idLivre WHERE emprunts.id_utilisateur = %s and is_validated=0;"
            val = (user_id,)
            cursor.execute(sql, val)

            # Récupérer les données
            borrowed_books_data = cursor.fetchall()

            # Afficher les emprunts
            # Create a list to store the values from the database
            value = []

            for row in borrowed_books_data:
                # Add a new column for the suspend button (let's assume 'Suspend' is the button text)
                row_data = list(row)
                value.append(row_data)

            # Define column names
            column_names = ["ID Emprunt","Titre du Livre", "Date d'Emprunt"]

            # Add column names to the beginning of the value list
            value.insert(0, column_names)

            # Clear the existing table
            for widget in self.table_frame.winfo_children():
                widget.destroy()

            # Check if the value list is not empty and has at least one row and one column
            if value and len(value) > 0 and len(value[0]) > 0:
                # Create the CTkTable using the updated value list
                table = CTkTable(
                    master=self.table_frame,
                    row=len(value),
                    column=len(value[0]),
                    values=value,
                )
                table.pack(expand=False, fill="none", padx=20, pady=20)
            else:
                print("Error: Empty or invalid data from the database.")

        def display_user_history_books(self):
            # Créer une connexion à la base de données
            conn = mysql.connector.connect(
                host="localhost", user="root", password="", database="python"
            )
            # Créer un curseur pour exécuter des requêtes SQL
            cursor = conn.cursor()

            user_id = login_result

            # Exécuter la requête SQL pour récupérer l'historique de l'utilisateur
            sql = "SELECT livre.titre, historique.dateEmprunt FROM historique JOIN livre ON historique.id_book = livre.idLivre WHERE historique.id_user = %s;"
            val = (user_id,)
            cursor.execute(sql, val)

            # Récupérer les données
            borrowed_books_data = cursor.fetchall()

            # Afficher l'historique
            # Create a list to store the values from the database
            value = []

            for row in borrowed_books_data:
                # Add a new column for the suspend button (let's assume 'Suspend' is the button text)
                row_data = list(row)
                value.append(row_data)

            # Define column names
            column_names = ["Titre du Livre", "Date d'Emprunt"]

            # Add column names to the beginning of the value list
            value.insert(0, column_names)

            # Clear the existing table
            for widget in self.table_frame.winfo_children():
                widget.destroy()

            # Check if the value list is not empty and has at least one row and one column
            if value and len(value) > 0 and len(value[0]) > 0:
                # Create the CTkTable using the updated value list
                table = CTkTable(
                    master=self.table_frame,
                    row=len(value),
                    column=len(value[0]),
                    values=value,
                )
                table.pack(expand=False, fill="none", padx=20, pady=20)
            else:
                print("Error: Empty or invalid data from the database.")
        
        def on_close(self):
            self.destroy()
            sys.exit()

        def redirect_to_Profile(self):
            self.withdraw()
            page_profile(login_result, return_callback=self.show_app)

        def redirect_to_Catalogue(self):
            self.withdraw()
            app_Catalogue = page_catalogue(login_result)
            app_Catalogue.mainloop()

        def restart_program(self):
            python = sys.executable
            os.execl(python, python, *sys.argv)
        
        def show_app(self):
            self.deiconify()  # Show the window again
            self.destroy()
        
    app2 = App2(login_result)
    app2.protocol("WM_DELETE_WINDOW", app2.on_close)
    app2.mainloop()


if __name__ == "__main__":
    app = page_catalogue()
    app.mainloop()
