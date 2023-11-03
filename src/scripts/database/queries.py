import logging
import sqlite3
from sqlite3 import Error

from src.scripts.prolog_interface import PrologQueryHandler as Prolog
from scripts.database.sql import *


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

        if not self.get_students() and not self.get_modules() and not self.get_details():
            # Insert data
            self.insert_students()
            self.insert_modules()
            self.insert_details()

            # Commit changes
            self.conn.commit()

        # Close the connection
        # self.close_connection()

    def close_connection(self):
        try:
            self.conn.close()
        except Error as e:
            print(e)

    def create_table(self, create_table_sql):
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
            if create_table_sql == sql_create_details_table:
                try:
                    c.execute(sql_create_unique_index)
                except Error as e:
                    logging.warning(e)
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
        c.execute("""SELECT * FROM student_master""")
        return c.fetchall()

    def get_modules(self):
        c = self.conn.cursor()
        c.execute("""SELECT * FROM module_master""")
        return c.fetchall()

    def get_details(self):
        c = self.conn.cursor()
        c.execute("""SELECT * FROM module_details""")
        return c.fetchall()

    def get_student(self, student_id):
        c = self.conn.cursor()
        c.execute(f"""SELECT * FROM student_master WHERE id = {student_id}""")
        Prolog.assert_student(c.fetchone())

    def get_module(self, module_code):
        c = self.conn.cursor()
        c.execute(f"""SELECT * FROM module_master WHERE code = '{module_code}'""")
        Prolog.assert_module(c.fetchone())

    def update_knowledge_base(self, year):
        try:
            c = self.conn.cursor()
            c.execute(f"""SELECT * FROM module_details WHERE year = {year}""")
            results = c.fetchall()

            for result in results:
                Prolog.assert_details(result)
                self.get_student(result[0])
                self.get_module(result[1])
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    def remove_student(self, student_id):
        try:
            c = self.conn.cursor()
            c.execute(f"""DELETE FROM student_master WHERE id = {student_id}""")
            c.execute(f"""DELETE FROM module_details WHERE student_id = '{student_id}'""")

            # Commit changes
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    def remove_module(self, module_code):
        try:
            c = self.conn.cursor()
            c.execute(f"""DELETE FROM module_master WHERE code = '{module_code}'""")
            c.execute(f"""DELETE FROM module_details WHERE module_code = '{module_code}'""")

            # Commit changes
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    def remove_details(self, student_id, module_code, semester):
        sql_remove_student = f"""DELETE FROM module_details WHERE student_id = {student_id} 
                            AND module_code = '{module_code}' AND semester = {semester}"""
        try:
            c = self.conn.cursor()
            c.execute(sql_remove_student)

            # Commit changes
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False
