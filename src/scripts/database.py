import logging
import sqlite3
from sqlite3 import Error

from queries import *


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
        c.execute(sql_get_students)
        return c.fetchall()

    def get_modules(self):
        c = self.conn.cursor()
        c.execute(sql_get_modules)
        return c.fetchall()

        # for module in modules:
        #    Prolog.add_module(module)

    def get_details(self):
        c = self.conn.cursor()
        c.execute(sql_get_details)
        return c.fetchall()

    def remove_student(self, student_id):
        c = self.conn.cursor()
        sql_remove_student = f"""DELETE FROM student_master WHERE id = {student_id}"""
        try:
            c.execute(sql_remove_student)
            self.commit_changes()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    def remove_module(self, module_code):
        c = self.conn.cursor()
        sql_remove_module = f"""DELETE FROM module_master WHERE code = '{module_code}'"""
        try:
            c.execute(sql_remove_module)
            self.commit_changes()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    def remove_details(self, student_id, module_code, semester):
        c = self.conn.cursor()
        sql_remove_student = f"""DELETE FROM module_details WHERE student_id = {student_id}, 
        module_code = {module_code}, semester = {semester}"""
        try:
            c.execute(sql_remove_student)
            self.commit_changes()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    def commit_changes(self):
        try:
            self.conn.commit()
        except Error as e:
            print(e)
