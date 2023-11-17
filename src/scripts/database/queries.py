import logging
import sqlite3
from sqlite3 import Error

from src.scripts.database.sql import *
from src.scripts.prolog_interface import PrologQueryHandler as Prolog


def create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect(db_file)
    except Error as e:
        logging.error(f"An error occurred: {e}")
    return connection


class DatabaseManager:

    def __init__(self):
        # Database file path
        self.db_file = '../../data/student_grades.db'

        # Create database connection
        self.conn = self.create_connection()

        # Create tables
        self.create_table(sql_create_students_table)
        self.create_table(sql_create_modules_table)
        self.create_table(sql_create_details_table)
        self.create_table(sql_create_staff_table)
        self.create_table(sql_create_faculty_table)
        self.create_table(sql_create_programmes_table)
        self.create_table(sql_create_school_table)

        # Check if database is empty
        if not self.get_students() and not self.get_modules() and not self.get_details():
            # Insert data
            self.insert_data(sql_insert_students)
            self.insert_data(sql_insert_modules)
            self.insert_data(sql_insert_details)
            self.insert_data(sql_insert_staff)
            self.insert_data(sql_insert_faculty)
            self.insert_data(sql_insert_programmes)
            self.insert_data(sql_insert_schools)

            # Commit changes
            self.conn.commit()

    def create_connection(self):
        connection = None
        try:
            connection = sqlite3.connect(self.db_file)
        except Error as e:
            logging.error(f"An error occurred: {e}")
        return connection

    def close_connection(self):
        try:
            self.conn.close()
        except Error as e:
            logging.error(f"An error occurred: {e}")

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
            logging.error(f"An error occurred: {e}")

    def insert_data(self, insert_data_sql):
        c = self.conn.cursor()
        c.execute(insert_data_sql)

    def get_students(self):
        c = self.conn.cursor()
        c.execute("""
            SELECT id, student_master.name, student_master.email, school.school_name AS school_code, 
            programme.programme_name AS programme_name, staff.name AS advisor_name 
            FROM student_master 
            JOIN school ON student_master.school_code = school.school_code
            JOIN programme ON student_master.programme_code = programme.programme_code
            JOIN staff ON student_master.advisor_id = staff.staff_id
        """)
        return c.fetchall()

    def get_modules(self):
        c = self.conn.cursor()
        c.execute("""SELECT * FROM module_master""")
        return c.fetchall()

    def get_details(self):
        c = self.conn.cursor()
        c.execute("""SELECT student_id, module_master.name AS module_name, grade_points, semester, year 
            FROM module_details 
            JOIN module_master ON module_details.module_code = module_master.code""")
        return c.fetchall()

    def get_schools(self):
        c = self.conn.cursor()
        c.execute(f"""SELECT * FROM school""")
        return c.fetchall()

    def get_programmes(self, school_code):
        c = self.conn.cursor()
        c.execute(f"""SELECT * FROM programme WHERE school_code = '{school_code}'""")
        return c.fetchall()

    def get_advisors(self):
        c = self.conn.cursor()
        c.execute(f"""SELECT * FROM staff WHERE position = 'Advisor'""")
        return c.fetchall()

    def get_student(self, student_id):
        c = self.conn.cursor()
        c.execute(f"""SELECT * FROM student_master WHERE id = {student_id}""")
        Prolog.assert_student(c.fetchone())

    def get_module(self, module_code):
        c = self.conn.cursor()
        c.execute(f"""SELECT * FROM module_master WHERE code = '{module_code}'""")
        Prolog.assert_module(c.fetchone())

    def get_programme(self, programme_name):
        c = self.conn.cursor()
        c.execute(f"""SELECT * FROM programme WHERE programme_name = '{programme_name}'""")
        return c.fetchone()

    def get_school(self, school_name):
        c = self.conn.cursor()
        c.execute(f"""SELECT * FROM school WHERE school_name = '{school_name}'""")
        return c.fetchone()

    def get_advisor(self, advisor_name):
        c = self.conn.cursor()
        c.execute(f"""SELECT * FROM staff WHERE name = '{advisor_name}'""")
        return c.fetchone()

    def get_module_code(self, module_name):
        c = self.conn.cursor()
        c.execute(f"""SELECT code FROM module_master WHERE name = '{module_name}'""")
        return c.fetchone()[0]

    def get_student_advisor(self, student_id):
        c = self.conn.cursor()
        # Get advisor id
        c.execute(f"""SELECT advisor_id FROM student_master WHERE id = {student_id}""")
        advisor_id = c.fetchone()[0]

        # Get advisor details
        c.execute(f"""SELECT * FROM staff WHERE staff_id = {advisor_id}""")
        return c.fetchone()

    def get_programme_name(self, programme_code):
        c = self.conn.cursor()
        c.execute(f"""SELECT programme_name FROM programme WHERE programme_code = '{programme_code}'""")
        return c.fetchone()[0]

    def get_programme_director(self, programme_code):
        c = self.conn.cursor()
        # Get director id
        c.execute(f"""SELECT director_id FROM programme WHERE programme_code = '{programme_code}'""")
        director_id = c.fetchone()[0]

        # Get director details
        c.execute(f"""SELECT * FROM staff WHERE staff_id = {director_id}""")
        return c.fetchone()

    def get_school_name(self, school_code):
        c = self.conn.cursor()
        c.execute(f"""SELECT school_name FROM school WHERE school_code = '{school_code}'""")
        return c.fetchone()[0]

    def get_school_administrator(self, school_code):
        c = self.conn.cursor()
        # Get faculty code
        c.execute(f"""SELECT faculty_code FROM school WHERE school_code = '{school_code}'""")
        faculty_code = c.fetchone()[0]

        # Get administrator id
        c.execute(f"""SELECT admin_id FROM faculty WHERE faculty_code = '{faculty_code}'""")
        admin_id = c.fetchone()[0]

        # Get administrator details
        c.execute(f"""SELECT * FROM staff WHERE staff_id = {admin_id}""")
        return c.fetchone()

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

    def insert_detail(self, id_number, module_name, gpa, semester, year):
        try:
            c = self.conn.cursor()
            # Get module code
            c.execute(f"""SELECT code FROM module_master WHERE name = '{module_name}'""")
            module_code = c.fetchone()[0]

            # Insert details
            c.execute(
                f"""INSERT INTO module_details VALUES ({id_number}, '{module_code}', {gpa}, {semester}, {year})""")

            # Commit changes
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    def insert_student(self, student_id, name, email, school_name, programme_name, advisor_name):
        try:
            c = self.conn.cursor()
            # Get school, programme and advisor
            school = self.get_school(school_name)
            programme = self.get_programme(programme_name)
            advisor = self.get_advisor(advisor_name)

            c.execute(
                f"""INSERT INTO student_master VALUES ({student_id}, '{name}', '{email}', 
                '{school[0]}', '{programme[0]}', {advisor[0]})""")

            # Commit changes
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    def insert_module(self, module_code, module_name, credit):
        try:
            c = self.conn.cursor()
            c.execute(f"""INSERT INTO module_master VALUES ('{module_code}', '{module_name}', {credit})""")

            # Commit changes
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    def update_record(self, data, table_name):
        try:
            c = self.conn.cursor()

            match table_name:
                case "student":
                    # Get school, programme and advisor
                    school = self.get_school(data[3])
                    programme = self.get_programme(data[4])
                    advisor = self.get_advisor(data[5])

                    c.execute(
                        f"""UPDATE student_master SET name='{data[1]}', email='{data[2]}', school_code='{school[0]}', 
                    programme_code='{programme[0]}', advisor_id={advisor[0]} WHERE id={data[0]}""")
                case "module":
                    c.execute(f"""UPDATE module_master SET name='{data[1]}', credits={data[2]} 
                    WHERE code='{data[0]}'""")
                case "details":
                    # Get module code
                    c.execute(f"""SELECT * FROM module_master WHERE name = '{data[1]}'""")
                    module_code = c.fetchone()[0]

                    c.execute(f"""UPDATE module_details SET grade_points={data[2]}, semester={data[3]}, year={data[4]}
                    WHERE student_id={data[0]} AND module_code='{module_code}'""")
                case _:
                    print("Record could not be updated.")

            # Commit changes
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    def remove_student(self, student_id):
        try:
            c = self.conn.cursor()

            # Check if the student exists
            c.execute(f"""SELECT * FROM student_master WHERE id = {student_id}""")
            if c.fetchone() is None:
                logging.error(f"Student with id [{student_id}] doesn't exist.")
                return False

            # Delete record
            c.execute(f"""DELETE FROM student_master WHERE id = {student_id}""")
            c.execute(f"""DELETE FROM module_details WHERE student_id = '{student_id}'""")

            # Commit changes
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    def remove_module(self, module):
        module_code = None
        try:
            c = self.conn.cursor()
            # Check if the module exists
            c.execute(f"""SELECT * FROM module_master WHERE code = '{module}'""")
            if c.fetchone() is None:
                # Get module code
                module_code = self.get_module_code(module)

                # Check if the module exists
                c.execute(f"""SELECT * FROM module_master WHERE code = '{module_code}'""")
                if c.fetchone() is None:
                    logging.error(f"Module with code [{module}] doesn't exist.")
                    return False

            # Delete record
            c.execute(f"""DELETE FROM module_master WHERE code = '{module_code}'""")
            c.execute(f"""DELETE FROM module_details WHERE module_code = '{module_code}'""")

            # Commit changes
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    def remove_details(self, student_id, module_name, semester):
        try:
            c = self.conn.cursor()

            # Get module code
            c.execute(f"""SELECT code FROM module_master WHERE name = '{module_name}'""")
            module_code = c.fetchone()[0]

            # Check if the module exists
            c.execute(f"""SELECT * FROM module_details WHERE student_id = {student_id} 
                            AND module_code = '{module_code}' AND semester = {semester}""")
            if c.fetchone() is None:
                logging.error(
                    f"Record with student id [{student_id}], module code [{module_code}] "
                    f"and semester [{semester}] doesn't exist.")
                return False

            # Delete record
            c.execute(f"""DELETE FROM module_details WHERE student_id = {student_id} 
                            AND module_code = '{module_code}' AND semester = {semester}""")

            # Commit changes
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False
