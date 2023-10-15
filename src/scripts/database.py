import sqlite3
from sqlite3 import Error

from scripts.queries import sql_create_students_table, sql_create_modules_table, sql_create_details_table


# install SQLite from the database tab

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('../../data/student_grades.db')
    except Error as e:
        print(e)

    return conn


def close_connection(conn):
    try:
        conn.close()
    except Error as e:
        print(e)


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


# create a database connection
conn = create_connection()

# create tables
if conn is not None:
    # create students table
    create_table(conn, sql_create_students_table)

    # create modules table
    create_table(conn, sql_create_modules_table)

    # create details table
    create_table(conn, sql_create_details_table)
else:
    print("Error! cannot create the database connection.")

# close the connection
close_connection(conn)
