import mysql.connector
from datetime import datetime, timedelta

conn = mysql.connector.connect(
    host="localhost", user="root", password="", database="python"
)
mycursor = conn.cursor()


def is_admin(username):
    admin_usernames = [
        "admin",
        "superadmin",
    ]
    return username in admin_usernames


def login(username, password):
    sql = "SELECT id, is_suspended FROM utilisateur WHERE username = %s AND mdp = %s"
    val = (username, password)
    try:
        mycursor.execute(sql, val)
        user = mycursor.fetchone()
        if user:
            id, is_suspended = user
            if is_suspended == 1:
                return -2  # Account suspended, returns -2
            if is_admin(username):
                return 1  # Authenticated as an administrator
            else:
                return id  # Authenticated as a normal user
        else:
            return -1  # Incorrect credentials, returns -1
    except mysql.connector.Error as err:
        return -3  # Database error, returns -3
    finally:
        close_connection()


def create_account(username, nom, prenom, mail, mdp):
    conn = mysql.connector.connect(
    host="localhost", user="root", password="", database="python"
    )
    mycursor = conn.cursor()
    check_existing_user_query = "SELECT username FROM utilisateur WHERE username = %s"
    mycursor.execute(check_existing_user_query, (username,))
    existing_user = mycursor.fetchone()
    if existing_user:
        print("Username already in use")  # Username already exists, returns -1
    else:
        sql = "INSERT INTO utilisateur (nom, Prenom, mail, username, mdp,statut) VALUES (%s, %s, %s, %s, %s,0)"
        val = (nom, prenom, mail, username, mdp)
        try:
            mycursor.execute(sql, val)
            conn.commit()
            return 1  # Success, everything is inserted correctly
        except mysql.connector.Error as err:
            return -2  # Database error, returns -2
        finally:
            close_connection()


def close_connection():
    try:
        if mycursor:
            mycursor.close()
        if conn:
            conn.close()
    except Exception as e:
        print(f"Error while closing connection: {e}")


# Example usage:
# result = create_account(username, nom, prenom, mail, mdp)
# print(result)

# Make sure to handle exceptions appropriately in your actual application.
