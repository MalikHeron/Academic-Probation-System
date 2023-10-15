import sqlite3
from sqlite3 import Error


# install SQLite from the database tab

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('student_grades.db')
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


# SQL for creating table
sql_create_students_table = """CREATE TABLE IF NOT EXISTS student_master (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    email text NOT NULL,
                                    school text NOT NULL,
                                    programme text NOT NULL
                                );"""

sql_create_modules_table = """CREATE TABLE IF NOT EXISTS module_master (
                                    code text PRIMARY KEY,
                                    name text NOT NULL,
                                    credits integer NOT NULL
                                );"""

sql_create_details_table = """CREATE TABLE IF NOT EXISTS module_details (
                                student_id integer NOT NULL,
                                module_code text NOT NULL,
                                grade_points integer NOT NULL,
                                semester integer NOT NULL,
                                year integer NOT NULL,
                                FOREIGN KEY (student_id) REFERENCES student_master (id),
                                FOREIGN KEY (module_code) REFERENCES module_master (code)
                            );"""

# create a database connection
conn = create_connection()

# create tables
if conn is not None:
    # create students table
    create_table(conn, sql_create_students_table)

    # create modules table
    create_table(conn, sql_create_modules_table)

    # create grades table
    create_table(conn, sql_create_details_table)
else:
    print("Error! cannot create the database connection.")

# close the connection
close_connection(conn)
