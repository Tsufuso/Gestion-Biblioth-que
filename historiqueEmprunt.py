import mysql.connector
from datetime import datetime, timedelta

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost", user="root", password="", database="python"
)
cursor = conn.cursor()

def update_outdated():
    # variable that will take time
    seven_days_ago = datetime.now() - timedelta(days=7)
    # query that will update the database to where the user will be suspended and unvalidate his resa
    query = "UPDATE emprunts SET outdated=1 WHERE idEmprunt IN (SELECT idEmprunt FROM emprunts WHERE date_Emprunt < %s AND is_validated = 0)"
    # cursor that will execute the query and take as a variable the variable that takes the time
    cursor.execute(query, (seven_days_ago,))
    # Syntax that will execute the query
    conn.commit()


def move_outdated_to_history():
    try:
        conn = mysql.connector.connect(
            host="localhost", user="root", password="", database="python"
        )
        cursor = conn.cursor()

        seven_days_ago = datetime.now() - timedelta(days=7)
        
        # Retrieve outdated loans
        query = "SELECT * FROM emprunts WHERE date_emprunt < %s"
        cursor.execute(query, (seven_days_ago,))
        outdated_emprunts = cursor.fetchall()

        for emprunt in outdated_emprunts:
            id_emprunt, id_utilisateur, id_livre, date_emprunt, is_validated, outdated = emprunt
            print(id_emprunt, id_utilisateur, id_livre, date_emprunt, is_validated, outdated)
            
            # Insert into the historique table without the return date
            insert_query = "INSERT INTO historique (id_emprunt, id_user, id_book, dateEmprunt, is_validated, outdated) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(
                insert_query,
                (id_emprunt, id_utilisateur, id_livre, date_emprunt, is_validated, outdated),
            )

        # Delete outdated loans from the emprunts table
        delete_query = "DELETE FROM emprunts WHERE date_emprunt < %s"
        cursor.execute(delete_query, (seven_days_ago,))
        
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()
        conn.close()

# Call the function
move_outdated_to_history()


# Appeler la fonction pour déplacer les emprunts périmés vers l'historique
update_outdated()
move_outdated_to_history()