import itertools
import sqlite3
import threading
import time
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
    def __init__(self):
        # Create database connection
        self.done = None
        self.conn = create_connection('../../data/student_grades.db')

        # Create tables
        self.create_table(sql_create_students_table)
        self.create_table(sql_create_modules_table)
        self.create_table(sql_create_details_table)

        # Insert data
        self.insert_students()
        self.insert_modules()
        self.insert_details()

        # Commit changes
        self.commit_changes()

        # Update knowledge base
        self.update_knowledge_base()

        # Close the connection
        self.close_connection()

    def close_connection(self):
        try:
            self.conn.close()
        except Error as e:
            print(e)

    def create_table(self, create_table_sql):
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
            c.execute(sql_create_unique_index)
        except Error as e:
            print(e)

    def insert_students(self):
        c = self.conn.cursor()
        c.execute(sql_insert_students)

    def insert_modules(self):
        c = self.conn.cursor()
        c.execute(sql_insert_modules)

    def insert_details(self):
        c = self.conn.cursor()
        c.execute(sql_insert_details)

    def get_students(self):
        c = self.conn.cursor()
        c.execute(sql_get_students)
        students = c.fetchall()

        for student in students:
            Prolog.add_student(student)

    def get_modules(self):
        c = self.conn.cursor()
        c.execute(sql_get_modules)
        modules = c.fetchall()

        for module in modules:
            Prolog.add_module(module)

    def get_details(self):
        c = self.conn.cursor()
        c.execute(sql_get_details)
        details = c.fetchall()

        for detail in details:
            Prolog.add_details(detail)

    def animate(self):
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if self.done:
                break
            print('\rUpdating Knowledge Base... ' + c, end='', flush=True)
            time.sleep(0.1)

    def update_knowledge_base(self):
        self.done = False
        t = threading.Thread(target=self.animate)
        t.start()

        self.get_students()
        self.get_modules()
        self.get_details()

        self.done = True
        t.join()  # Wait for the animation thread to finish

        print('\rKnowledge Base Updated.', flush=True)

    def commit_changes(self):
        try:
            self.conn.commit()
        except Error as e:
            print(e)
