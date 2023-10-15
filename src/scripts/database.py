import sqlite3
from sqlite3 import Error

from scripts.queries import *
from scripts.prolog_interface import PrologQueryHandler as Prolog


def create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return connection


class DatabaseManager:
    def __init__(self, db_file):
        self.conn = create_connection(db_file)

    def close_connection(self):
        try:
            self.conn.close()
        except Error as e:
            print(e)

    def create_table(self, create_table_sql):
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def insert_students(self):
        for student in Prolog.get_student_list():
            c = self.conn.cursor()
            c.execute(sql_insert_students,
                      (student['Id'], student['Name'], student['Email'], student['School'], student['Programme']))

    def insert_modules(self):
        for module in Prolog.get_module_list():
            c = self.conn.cursor()
            c.execute(sql_insert_modules,
                      (module['Code'], module['Name'], module['Credits']))

    def insert_details(self):
        for detail in Prolog.get_details_list():
            c = self.conn.cursor()
            c.execute(sql_insert_details,
                      (detail['Id'], detail['Code'], detail['Grade_Points'], detail['Semester'],
                       detail['Year']))

    def commit_changes(self):
        try:
            self.conn.commit()
        except Error as e:
            print(e)


# Usage
db_manager = DatabaseManager('../../data/student_grades.db')

# Create tables
db_manager.create_table(sql_create_students_table)
db_manager.create_table(sql_create_modules_table)
db_manager.create_table(sql_create_details_table)

# Insert data
db_manager.insert_students()
db_manager.insert_modules()
db_manager.insert_details()

# Commit changes
db_manager.commit_changes()

# Close the connection
db_manager.close_connection()
