import mysql.connector
from datetime import datetime, timedelta


def get_users_7_days_ago():
    # Establish a connection to your MySQL database
    mydb = mysql.connector.connect(
        host="localhost", user="root", password="", database="python"
    )

    mycursor = mydb.cursor()

    # Calculate the date 7 days ago from today
    seven_days_ago = datetime.now() - timedelta(days=7)

    # Construct the query
    query = """
        SELECT DISTINCT nom,Prenom,titre,%s -date_emprunt as Retard
        FROM utilisateur join emprunts on id = id_utilisateur Join livre on id_livre = idLivre
        WHERE date_emprunt < %s
    """

    # Execute the query
    mycursor.execute(query, (seven_days_ago,))

    # Fetch all the results
    users = mycursor.fetchall()

    # Close the database connection
    mydb.close()

    return users


def suspend_user_by_id(user_id):
    # Establish a connection to your MySQL database
    host = ("localhost",)
    user = ("root",)
    password = ("",)
    database = "python"

    try:
        # Establish connection to MySQL
        connection = mysql.connector.connect(
            host=host, user=user, password=password, database=database
        )

        if connection.is_connected():
            print("Connected to MySQL!")
            cursor = connection.cursor()

            # Update query to set is_suspended to true for the provided user ID
            update_query = "UPDATE utilisateur " "SET is_suspended = 1 " "WHERE id = %s"
            # Execute the update query with the provided user_id
            cursor.execute(update_query, (user_id,))

            # Commit the changes to the database
            connection.commit()

            print(f"User with ID {user_id} has been suspended.")

    except mysql.connector.Error as e:
        print("Error connecting to MySQL:", e)

    finally:
        # Close the connection
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
