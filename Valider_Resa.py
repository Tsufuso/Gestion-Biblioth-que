import mysql.connector

# library that will take the time
from datetime import datetime, timedelta

# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost", user="root", password="", database="python"
)
# create cursor
cursor = conn.cursor()


# function to validate reservation
def valider_Emprunt(id_Emprunt):
    # query that the cursor will execute (%s is a placeholder for the variable id_Emprunt)
    query = "UPDATE Emprunts SET is_validated=TRUE WHERE id_Emprunt=%s"
    cursor.execute(query, (id_Emprunt,))
    # Syntax that will execute the query
    conn.commit()
    """Function That will validate resa"""


# function that will suspend somebody if he goes after 7 days
def check_and_suspend_users():
    # variable that will take time
    seven_days_ago = datetime.now() - timedelta(days=7)
    # query that will update the database to where the user will be suspended and unvalidate his resa
    query = "UPDATE utilisateur SET is_suspended=TRUE WHERE id IN (SELECT id FROM Emprunt WHERE date_Emprunt < %s AND is_validated=FALSE)"
    # cursor that will execute the query and take as a variable the variable that takes the time
    cursor.execute(query, (seven_days_ago,))
    # Syntax that will execute the query
    conn.commit()
    """This Function will automatically ban users that their resa > 7days"""
