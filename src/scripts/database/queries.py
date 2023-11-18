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
            LEFT JOIN school ON student_master.school_code = school.school_code
            LEFT JOIN programme ON student_master.programme_code = programme.programme_code
            LEFT JOIN staff ON student_master.advisor_id = staff.staff_id
            ORDER BY id
        """)
        return c.fetchall()

    def get_modules(self):
        c = self.conn.cursor()
        c.execute("""SELECT * FROM module_master ORDER BY name""")
        return c.fetchall()

    def get_details(self):
        c = self.conn.cursor()
        c.execute("""SELECT student_id, module_master.name AS module_name, grade_points, semester, year 
            FROM module_details 
            JOIN module_master ON module_details.module_code = module_master.code
            ORDER BY student_id
        """)
        return c.fetchall()

    def get_staff(self):
        c = self.conn.cursor()
        c.execute("""SELECT * FROM staff ORDER BY staff_id""")
        return c.fetchall()

    def get_faculties(self):
        c = self.conn.cursor()
        c.execute("""
                SELECT faculty_code, faculty_name, staff.name AS admin_name
                FROM faculty 
                LEFT JOIN staff ON faculty.admin_id = staff.staff_id
                ORDER BY faculty_code
            """)
        return c.fetchall()

    def get_schools(self):
        c = self.conn.cursor()
        c.execute("""
                SELECT school_code, school_name, faculty.faculty_name AS faculty_name, staff.name AS admin_name
                FROM school 
                LEFT JOIN faculty ON school.faculty_code = faculty.faculty_code
                LEFT JOIN staff ON faculty.admin_id = staff.staff_id
                ORDER BY school_code
            """)
        return c.fetchall()

    def get_programmes(self, school_code=None):
        c = self.conn.cursor()
        if school_code is None:
            c.execute("""
                SELECT programme_code, programme_name, school.school_name AS school_name,
                staff.name AS director_name
                FROM programme 
                LEFT JOIN school ON programme.school_code = school.school_code
                LEFT JOIN staff ON programme.director_id = staff.staff_id
                ORDER BY programme_code
            """)
        else:
            c.execute(f"""SELECT * FROM programme WHERE school_code = '{school_code}' ORDER BY programme_name""")
        return c.fetchall()

    def get_advisors(self):
        c = self.conn.cursor()
        c.execute(f"""SELECT * FROM staff WHERE position = 'Advisor' ORDER BY name""")
        return c.fetchall()

    def get_directors(self):
        c = self.conn.cursor()
        c.execute(f"""SELECT * FROM staff WHERE position = 'Director' ORDER BY name""")
        return c.fetchall()

    def get_administrator(self):
        c = self.conn.cursor()
        c.execute(f"""SELECT * FROM staff WHERE position = 'Administrator' ORDER BY name""")
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

    def get_module_code(self, module):
        c = self.conn.cursor()
        # Check if the module is a code
        c.execute(f"""SELECT * FROM module_master WHERE code = '{module}'""")
        if c.fetchone() is not None:
            return module  # Return the module as is if it's a code

        # If the module is not a code, assume it's a name and get the code
        c.execute(f"""SELECT code FROM module_master WHERE name = '{module}'""")
        result = c.fetchone()
        if result is not None:
            return result[0]  # Return the code corresponding to the module name

        return None  # Return None if the module is neither a code nor a name

    def get_faculty_code(self, faculty):
        c = self.conn.cursor()
        # Check if the faculty is a code
        c.execute(f"""SELECT * FROM faculty WHERE faculty_code = '{faculty}'""")
        if c.fetchone() is not None:
            return faculty  # Return the faculty as is if it's a code

        # If the faculty is not a code, assume it's a name and get the code
        c.execute(f"""SELECT faculty_code FROM faculty WHERE faculty_name = '{faculty}'""")
        result = c.fetchone()
        if result is not None:
            return result[0]  # Return the code corresponding to the faculty name

        return None  # Return None if the faculty is neither a code nor a name

    def get_school_code(self, school):
        c = self.conn.cursor()
        # Check if the school is a code
        c.execute(f"""SELECT * FROM school WHERE school_code = '{school}'""")
        if c.fetchone() is not None:
            return school  # Return the school as is if it's a code

        # If the school is not a code, assume it's a name and get the code
        c.execute(f"""SELECT school_code FROM school WHERE school_name = '{school}'""")
        result = c.fetchone()
        if result is not None:
            return result[0]  # Return the code corresponding to the school name

        return None  # Return None if the school is neither a code nor a name

    def get_programme_code(self, programme):
        c = self.conn.cursor()
        # Check if the programme is a code
        c.execute(f"""SELECT * FROM programme WHERE programme_code = '{programme}'""")
        if c.fetchone() is not None:
            return programme  # Return the programme as is if it's a code

        # If the programme is not a code, assume it's a name and get the code
        c.execute(f"""SELECT programme_code FROM programme WHERE programme_name = '{programme}'""")
        result = c.fetchone()
        if result is not None:
            return result[0]  # Return the code corresponding to the programme name

        return None  # Return None if the programme is neither a code nor a name

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

    def insert_staff(self, id_number, name, email, position):
        try:
            c = self.conn.cursor()
            # Insert details
            c.execute(
                f"""INSERT INTO staff VALUES ({id_number}, '{name}', '{email}', '{position}')""")

            # Commit changes
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    def insert_faculty(self, faculty_code, admin_name, faculty_name):
        try:
            c = self.conn.cursor()
            # Get admin id
            c.execute(f"""SELECT staff_id FROM staff WHERE name = '{admin_name}'""")
            admin_id = c.fetchone()[0]

            # Insert details
            c.execute(
                f"""INSERT INTO faculty VALUES ('{faculty_code}', '{faculty_name}', {admin_id})""")

            # Commit changes
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    def insert_programme(self, programme_code, school_code, director_name, programme_name):
        try:
            c = self.conn.cursor()
            # Get director id
            c.execute(f"""SELECT staff_id FROM staff WHERE name = '{director_name}'""")
            director_id = c.fetchone()[0]

            # Insert details
            c.execute(
                f"""INSERT INTO programme VALUES ('{programme_code}', '{school_code}', {director_id}, 
                '{programme_name}')""")

            # Commit changes
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    def insert_school(self, school_code, faculty_name, school_name):
        try:
            c = self.conn.cursor()
            # Get faculty code
            c.execute(f"""SELECT faculty_code FROM faculty WHERE faculty_name = '{faculty_name}'""")
            faculty_code = c.fetchone()[0]

            # Insert details
            c.execute(
                f"""INSERT INTO school VALUES ('{school_code}', '{faculty_code}', '{school_name}')""")

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
                case "staff":
                    c.execute(f"""UPDATE staff SET name='{data[1]}', email='{data[2]}', position='{data[3]}' 
                    WHERE staff_id={data[0]}""")
                case "faculty":
                    # Get admin id
                    c.execute(f"""SELECT * FROM staff WHERE name = '{data[2]}'""")
                    admin_id = c.fetchone()[0]

                    c.execute(f"""UPDATE faculty SET admin_id={admin_id}, faculty_name='{data[1]}' 
                    WHERE faculty_code='{data[0]}'""")
                case "school":
                    # Get faculty code
                    c.execute(f"""SELECT * FROM faculty WHERE faculty_name = '{data[2]}'""")
                    faculty_code = c.fetchone()[0]

                    c.execute(f"""UPDATE school SET faculty_code='{faculty_code}', school_name='{data[1]}' 
                    WHERE school_code='{data[0]}'""")
                case "programme":
                    # Get director id
                    c.execute(f"""SELECT * FROM staff WHERE name = '{data[3]}'""")
                    director_id = c.fetchone()[0]

                    # Get school code
                    c.execute(f"""SELECT * FROM school WHERE school_name = '{data[2]}'""")
                    school_code = c.fetchone()[0]

                    c.execute(
                        f"""UPDATE programme SET director_id={director_id},  programme_name='{data[1]}', 
                        school_code='{school_code}' WHERE programme_code='{data[0]}'""")
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
        try:
            c = self.conn.cursor()
            # Get module code
            module_code = self.get_module_code(module)
            if module_code is None:
                logging.error(f"Module [{module}] doesn't exist.")
                return False

            # Check if the module exists
            c.execute(f"""SELECT * FROM module_master WHERE code = '{module_code}'""")
            if c.fetchone() is None:
                logging.error(f"Module with code [{module_code}] doesn't exist.")
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

    def remove_staff(self, staff_id):
        try:
            c = self.conn.cursor()
            # Check if the staff exists
            c.execute(f"""SELECT * FROM staff WHERE staff_id = {staff_id}""")
            if c.fetchone() is None:
                logging.error(f"Staff with id [{staff_id}] doesn't exist.")
                return False

            # Delete record
            c.execute(f"""DELETE FROM staff WHERE staff_id = {staff_id}""")
            c.execute(f"""UPDATE student_master SET advisor_id = 'None' WHERE advisor_id = {staff_id}""")
            c.execute(f"""UPDATE programme SET director_id = 'None' WHERE director_id = {staff_id}""")
            c.execute(f"""UPDATE faculty SET admin_id = 'None' WHERE admin_id = {staff_id}""")

            # Commit changes
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    def remove_faculty(self, faculty):
        try:
            c = self.conn.cursor()
            # Get faculty code
            faculty_code = self.get_faculty_code(faculty)
            if faculty_code is None:
                logging.error(f"Faculty [{faculty}] doesn't exist.")
                return False

            # Check if the faculty exists
            c.execute(f"""SELECT * FROM faculty WHERE faculty_code = '{faculty_code}'""")
            if c.fetchone() is None:
                logging.error(f"Faculty with code [{faculty_code}] doesn't exist.")
                return False

            # Delete record
            c.execute(f"""DELETE FROM faculty WHERE faculty_code = '{faculty_code}'""")
            c.execute(f"""UPDATE school SET faculty_code = 'None' WHERE faculty_code = '{faculty_code}'""")

            # Commit changes
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    def remove_school(self, school):
        try:
            c = self.conn.cursor()
            # Get school code
            school_code = self.get_school_code(school)
            if school_code is None:
                logging.error(f"School [{school}] doesn't exist.")
                return False

            # Check if the school exists
            c.execute(f"""SELECT * FROM school WHERE school_code = '{school_code}'""")
            if c.fetchone() is None:
                logging.error(f"School with code [{school_code}] doesn't exist.")
                return False

            # Delete record
            c.execute(f"""DELETE FROM school WHERE school_code = '{school_code}'""")
            c.execute(f"""UPDATE programme SET school_code = 'None' WHERE school_code = '{school_code}'""")
            c.execute(f"""UPDATE student_master SET school_code = 'None' WHERE school_code = '{school_code}'""")

            # Commit changes
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    def remove_programme(self, programme):
        try:
            c = self.conn.cursor()
            # Get programme code
            programme_code = self.get_programme_code(programme)
            if programme_code is None:
                logging.error(f"Programme [{programme}] doesn't exist.")
                return False

            # Check if the programme exists
            c.execute(f"""SELECT * FROM programme WHERE programme_code = '{programme_code}'""")
            if c.fetchone() is None:
                logging.error(f"Programme with code [{programme_code}] doesn't exist.")
                return False

            # Delete record
            c.execute(f"""DELETE FROM programme WHERE programme_code = '{programme_code}'""")
            c.execute(
                f"""UPDATE student_master SET programme_code = 'None' WHERE programme_code = '{programme_code}'""")

            # Commit changes
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False
