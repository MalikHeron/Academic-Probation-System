import logging
import sqlite3
from sqlite3 import Error

from src.scripts.database.sql import *
from src.scripts.prolog_interface import PrologQueryHandler as Prolog


class DatabaseManager:

    def __init__(self):
        # Database file path
        self.db_file = '../../data/student_grades.db'

        # Create database connection
        self.conn = self.create_connection()
        # Create cursor
        self.cursor = self.conn.cursor()

        # Create tables
        self.create_table(sql_create_students_table)
        self.create_table(sql_create_modules_table)
        self.create_table(sql_create_details_table)
        self.create_table(sql_create_staff_table)
        self.create_table(sql_create_faculty_table)
        self.create_table(sql_create_programmes_table)
        self.create_table(sql_create_school_table)
        self.create_table(sql_create_credentials_table)

        # Check if database is empty
        if not self.get_students() and not self.get_modules() and not self.get_details() and not self.get_staff() \
                and not self.get_faculties() and not self.get_schools() and not self.get_programmes():
            # Insert data
            self.insert_data(sql_insert_students)
            self.insert_data(sql_insert_modules)
            self.insert_data(sql_insert_details)
            self.insert_data(sql_insert_staff)
            self.insert_data(sql_insert_faculty)
            self.insert_data(sql_insert_programmes)
            self.insert_data(sql_insert_schools)
            self.insert_data(sql_insert_credentials)

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
            self.cursor.execute(create_table_sql)
            if create_table_sql == sql_create_details_table:
                try:
                    self.cursor.execute(sql_create_unique_index)
                except Error as e:
                    logging.warning(e)
        except Error as e:
            logging.error(f"An error occurred: {e}")

    def insert_data(self, insert_data_sql):
        self.cursor.execute(insert_data_sql)

    def get_credentials(self, username, password):
        # Check if the credentials exist
        self.cursor.execute(
            f"""SELECT * FROM credentials WHERE username = '{username}' AND password = '{password}'""")
        # Return None if the credentials don't exist
        if self.cursor.fetchone() is None:
            return None

        # Return the user id if the credentials exist
        self.cursor.execute(
            f"""SELECT user_id FROM credentials WHERE username = '{username}' AND password = '{password}'""")
        return self.cursor.fetchone()[0]

    def get_students(self):
        self.cursor.execute("""
            SELECT id, student_master.name, student_master.email, school.school_name AS school_code, 
            programme.programme_name AS programme_name, staff.name AS advisor_name 
            FROM student_master 
            LEFT JOIN school ON student_master.school_code = school.school_code
            LEFT JOIN programme ON student_master.programme_code = programme.programme_code
            LEFT JOIN staff ON student_master.advisor_id = staff.staff_id
            ORDER BY id
        """)
        return self.cursor.fetchall()

    def get_modules(self):
        self.cursor.execute("""SELECT * FROM module_master ORDER BY name""")
        return self.cursor.fetchall()

    def get_details(self):
        self.cursor.execute("""SELECT student_id, module_master.name AS module_name, grade_points, semester, year 
            FROM module_details 
            JOIN module_master ON module_details.module_code = module_master.code
            ORDER BY student_id
        """)
        return self.cursor.fetchall()

    def get_staff(self):
        self.cursor.execute("""SELECT * FROM staff ORDER BY staff_id""")
        return self.cursor.fetchall()

    def get_faculties(self):
        self.cursor.execute("""
                SELECT faculty_code, faculty_name, staff.name AS admin_name
                FROM faculty 
                LEFT JOIN staff ON faculty.admin_id = staff.staff_id
                ORDER BY faculty_code
            """)
        return self.cursor.fetchall()

    def get_schools(self):
        self.cursor.execute("""
                SELECT school_code, school_name, faculty.faculty_name AS faculty_name, staff.name AS admin_name
                FROM school 
                LEFT JOIN faculty ON school.faculty_code = faculty.faculty_code
                LEFT JOIN staff ON faculty.admin_id = staff.staff_id
                ORDER BY school_code
            """)
        return self.cursor.fetchall()

    def get_programmes(self, school_code=None):
        if school_code is None:
            self.cursor.execute("""
                SELECT programme_code, programme_name, school.school_name AS school_name,
                staff.name AS director_name
                FROM programme 
                LEFT JOIN school ON programme.school_code = school.school_code
                LEFT JOIN staff ON programme.director_id = staff.staff_id
                ORDER BY programme_code
            """)
        else:
            self.cursor.execute(f"""SELECT * FROM programme WHERE school_code = '{school_code}' 
            ORDER BY programme_name""")
        return self.cursor.fetchall()

    def get_advisors(self):

        self.cursor.execute(f"""SELECT * FROM staff WHERE position = 'Advisor' ORDER BY name""")
        return self.cursor.fetchall()

    def get_directors(self):
        self.cursor.execute(f"""SELECT * FROM staff WHERE position = 'Director' ORDER BY name""")
        return self.cursor.fetchall()

    def get_administrator(self):
        self.cursor.execute(f"""SELECT * FROM staff WHERE position = 'Administrator' ORDER BY name""")
        return self.cursor.fetchall()

    def get_student(self, student_id):
        self.cursor.execute(f"""SELECT * FROM student_master WHERE id = {student_id}""")
        Prolog.assert_student(self.cursor.fetchone())

    def get_module(self, module_code):
        self.cursor.execute(f"""SELECT * FROM module_master WHERE code = '{module_code}'""")
        Prolog.assert_module(self.cursor.fetchone())

    def get_programme(self, programme_name):
        self.cursor.execute(f"""SELECT * FROM programme WHERE programme_name = '{programme_name}'""")
        return self.cursor.fetchone()

    def get_school(self, school_name):
        self.cursor.execute(f"""SELECT * FROM school WHERE school_name = '{school_name}'""")
        return self.cursor.fetchone()

    def get_advisor(self, advisor_name):
        self.cursor.execute(f"""SELECT * FROM staff WHERE name = '{advisor_name}'""")
        return self.cursor.fetchone()

    def get_staff_name(self, staff_id):
        self.cursor.execute(f"""SELECT name FROM staff WHERE staff_id = {staff_id}""")
        return self.cursor.fetchone()[0]

    def get_module_code(self, module):
        # Check if the module is a code
        self.cursor.execute(f"""SELECT * FROM module_master WHERE code = '{module}'""")
        if self.cursor.fetchone() is not None:
            return module  # Return the module as is if it's a code

        # If the module is not a code, assume it's a name and get the code
        self.cursor.execute(f"""SELECT code FROM module_master WHERE name = '{module}'""")
        result = self.cursor.fetchone()
        if result is not None:
            return result[0]  # Return the code corresponding to the module name

        return None  # Return None if the module is neither a code nor a name

    def get_faculty_code(self, faculty):
        # Check if the faculty is a code
        self.cursor.execute(f"""SELECT * FROM faculty WHERE faculty_code = '{faculty}'""")
        if self.cursor.fetchone() is not None:
            return faculty  # Return the faculty as is if it's a code

        # If the faculty is not a code, assume it's a name and get the code
        self.cursor.execute(f"""SELECT faculty_code FROM faculty WHERE faculty_name = '{faculty}'""")
        result = self.cursor.fetchone()
        if result is not None:
            return result[0]  # Return the code corresponding to the faculty name

        return None  # Return None if the faculty is neither a code nor a name

    def get_school_code(self, school):
        # Check if the school is a code
        self.cursor.execute(f"""SELECT * FROM school WHERE school_code = '{school}'""")
        if self.cursor.fetchone() is not None:
            return school  # Return the school as is if it's a code

        # If the school is not a code, assume it's a name and get the code
        self.cursor.execute(f"""SELECT school_code FROM school WHERE school_name = '{school}'""")
        result = self.cursor.fetchone()
        if result is not None:
            return result[0]  # Return the code corresponding to the school name

        return None  # Return None if the school is neither a code nor a name

    def get_programme_code(self, programme):
        # Check if the programme is a code
        self.cursor.execute(f"""SELECT * FROM programme WHERE programme_code = '{programme}'""")
        if self.cursor.fetchone() is not None:
            return programme  # Return the programme as is if it's a code

        # If the programme is not a code, assume it's a name and get the code
        self.cursor.execute(f"""SELECT programme_code FROM programme WHERE programme_name = '{programme}'""")
        result = self.cursor.fetchone()
        if result is not None:
            return result[0]  # Return the code corresponding to the programme name

        return None  # Return None if the programme is neither a code nor a name

    def get_student_advisor(self, student_id):
        # Get advisor id
        self.cursor.execute(f"""SELECT advisor_id FROM student_master WHERE id = {student_id}""")
        advisor_id = self.cursor.fetchone()[0]

        if advisor_id is None:
            return None

        # Get advisor details
        self.cursor.execute(f"""SELECT * FROM staff WHERE staff_id = {advisor_id}""")
        return self.cursor.fetchone()

    def get_programme_name(self, programme_code):
        if programme_code == 'None':
            return None
        self.cursor.execute(f"""SELECT programme_name FROM programme WHERE programme_code = '{programme_code}'""")
        return self.cursor.fetchone()[0]

    def get_programme_director(self, programme_code):
        if programme_code == 'None':
            return None

        # Get director id
        self.cursor.execute(f"""SELECT director_id FROM programme WHERE programme_code = '{programme_code}'""")
        director_id = self.cursor.fetchone()[0]

        if director_id is None:
            return None

        # Get director details
        self.cursor.execute(f"""SELECT * FROM staff WHERE staff_id = {director_id}""")
        return self.cursor.fetchone()

    def get_school_name(self, school_code):
        self.cursor.execute(f"""SELECT school_name FROM school WHERE school_code = '{school_code}'""")
        return self.cursor.fetchone()[0]

    def get_school_administrator(self, school_code):
        # Get faculty code
        self.cursor.execute(f"""SELECT faculty_code FROM school WHERE school_code = '{school_code}'""")
        faculty_code = self.cursor.fetchone()[0]

        if faculty_code is None:
            return None

        # Get administrator id
        self.cursor.execute(f"""SELECT admin_id FROM faculty WHERE faculty_code = '{faculty_code}'""")
        admin_id = self.cursor.fetchone()[0]

        if admin_id is None:
            return None

        # Get administrator details
        self.cursor.execute(f"""SELECT * FROM staff WHERE staff_id = {admin_id}""")
        return self.cursor.fetchone()

    def update_knowledge_base(self, year):
        try:
            self.cursor.execute(f"""SELECT * FROM module_details WHERE year = {year}""")
            results = self.cursor.fetchall()

            for result in results:
                Prolog.assert_details(result)
                self.get_student(result[0])
                self.get_module(result[1])
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    def insert_detail(self, id_number, module_name, gpa, semester, year):
        try:
            # Get module code
            self.cursor.execute(f"""SELECT code FROM module_master WHERE name = '{module_name}'""")
            module_code = self.cursor.fetchone()[0]

            # Insert details
            self.cursor.execute(
                f"""INSERT INTO module_details VALUES ({id_number}, '{module_code}', {gpa}, {semester}, {year})""")

            # Commit changes
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    def insert_student(self, student_id, name, email, school_name, programme_name, advisor_name):
        try:
            # Get school, programme and advisor
            school = self.get_school(school_name)
            programme = self.get_programme(programme_name)
            if advisor_name != 'None':
                advisor = self.get_advisor(advisor_name)[0]
            else:
                advisor = 'NULL'

            self.cursor.execute(
                f"""INSERT INTO student_master VALUES ({student_id}, '{name}', '{email}', 
                '{school[0]}', '{programme[0]}', {advisor})""")

            # Commit changes
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    def insert_module(self, module_code, module_name, credit):
        try:
            self.cursor.execute(f"""INSERT INTO module_master VALUES ('{module_code}', '{module_name}', {credit})""")

            # Commit changes
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    def insert_staff(self, id_number, name, email, position, username, password):
        try:
            # Insert details
            self.cursor.execute(
                f"""INSERT INTO staff VALUES ({id_number}, '{name}', '{email}', '{position}')""")

            # Insert credentials
            self.cursor.execute(
                f"""INSERT INTO credentials VALUES ({id_number}, '{username}', '{password}')""")

            # Commit changes
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    def insert_faculty(self, faculty_code, faculty_name, admin_name):
        try:
            # Get admin id
            if admin_name != 'None':
                self.cursor.execute(f"""SELECT staff_id FROM staff WHERE name = '{admin_name}'""")
                admin_id = self.cursor.fetchone()[0]
            else:
                admin_id = 'NULL'

            # Insert details
            self.cursor.execute(
                f"""INSERT INTO faculty VALUES ('{faculty_code}', '{faculty_name}', {admin_id})""")

            # Commit changes
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    def insert_programme(self, programme_code, programme_name, school_name, director_name):
        try:
            # Get director id
            if director_name != 'None':
                self.cursor.execute(f"""SELECT staff_id FROM staff WHERE name = '{director_name}'""")
                director_id = self.cursor.fetchone()[0]
            else:
                director_id = 'NULL'

            # Get school code
            if school_name != 'None':
                self.cursor.execute(f"""SELECT school_code FROM school WHERE school_name = '{school_name}'""")
                school_code = self.cursor.fetchone()[0]
            else:
                school_code = 'NULL'

            # Insert details
            self.cursor.execute(
                f"""INSERT INTO programme VALUES ('{programme_code}', '{programme_name}', {director_id}, 
                '{school_code}')""")

            # Commit changes
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    def insert_school(self, school_code, school_name, faculty_name):
        try:
            # Get faculty code
            if faculty_name != 'None':
                self.cursor.execute(f"""SELECT faculty_code FROM faculty WHERE faculty_name = '{faculty_name}'""")
                faculty_code = self.cursor.fetchone()[0]
            else:
                faculty_code = 'NULL'

            # Insert details
            self.cursor.execute(
                f"""INSERT INTO school VALUES ('{school_code}', '{school_name}', '{faculty_code}')""")

            # Commit changes
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    def update_record(self, data, table_name):
        try:
            match table_name:
                case "student":
                    # Get school, programme and advisor
                    school = self.get_school(data[3])
                    programme = self.get_programme(data[4])
                    if data[5] != 'None':
                        advisor = self.get_advisor(data[5])[0]
                    else:
                        advisor = 'NULL'

                    self.cursor.execute(
                        f"""UPDATE student_master SET name='{data[1]}', email='{data[2]}', school_code='{school[0]}', 
                    programme_code='{programme[0]}', advisor_id={advisor} WHERE id={data[0]}""")
                case "module":
                    self.cursor.execute(f"""UPDATE module_master SET name='{data[1]}', credits={data[2]} 
                    WHERE code='{data[0]}'""")
                case "details":
                    # Get module code
                    self.cursor.execute(f"""SELECT * FROM module_master WHERE name = '{data[1]}'""")
                    module_code = self.cursor.fetchone()[0]

                    self.cursor.execute(f"""UPDATE module_details SET grade_points={data[2]}, 
                    semester={data[3]}, year={data[4]}
                    WHERE student_id={data[0]} AND module_code='{module_code}'""")
                case "staff":
                    self.cursor.execute(f"""UPDATE staff SET name='{data[1]}', email='{data[2]}', position='{data[3]}' 
                    WHERE staff_id={data[0]}""")

                    if data[3] == 'Administrator':
                        if self.cursor.execute(f"""SELECT * FROM credentials WHERE user_id = {data[0]}""").fetchone():
                            # Update credentials
                            self.cursor.execute(f"""UPDATE credentials SET username='{data[4]}', password='{data[5]}' 
                            WHERE user_id={data[0]}""")
                        else:
                            # Insert credentials
                            self.cursor.execute(f"""INSERT INTO credentials VALUES 
                            ({data[0]}, '{data[4]}', '{data[5]}')""")
                case "faculty":
                    # Get admin id
                    if data[2] != 'None':
                        self.cursor.execute(f"""SELECT * FROM staff WHERE name = '{data[2]}'""")
                        admin_id = self.cursor.fetchone()[0]
                    else:
                        admin_id = 'NULL'

                    self.cursor.execute(f"""UPDATE faculty SET admin_id={admin_id}, faculty_name='{data[1]}' 
                    WHERE faculty_code='{data[0]}'""")
                case "school":
                    # Get faculty code
                    if data[2] != 'None':
                        self.cursor.execute(f"""SELECT * FROM faculty WHERE faculty_name = '{data[2]}'""")
                        faculty_code = self.cursor.fetchone()[0]
                    else:
                        faculty_code = 'NULL'

                    self.cursor.execute(f"""UPDATE school SET faculty_code='{faculty_code}', school_name='{data[1]}' 
                    WHERE school_code='{data[0]}'""")
                case "programme":
                    # Get director id
                    if data[3] != 'None':
                        self.cursor.execute(f"""SELECT * FROM staff WHERE name = '{data[3]}'""")
                        director_id = self.cursor.fetchone()[0]
                    else:
                        director_id = 'NULL'

                    # Get school code
                    if data[2] != 'None':
                        self.cursor.execute(f"""SELECT * FROM school WHERE school_name = '{data[2]}'""")
                        school_code = self.cursor.fetchone()[0]
                    else:
                        school_code = 'NULL'

                    self.cursor.execute(
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
            # Check if the student exists
            self.cursor.execute(f"""SELECT * FROM student_master WHERE id = {student_id}""")
            if self.cursor.fetchone() is None:
                logging.error(f"Student with id [{student_id}] doesn't exist.")
                return False

            # Delete record
            self.cursor.execute(f"""DELETE FROM student_master WHERE id = {student_id}""")
            self.cursor.execute(f"""DELETE FROM module_details WHERE student_id = '{student_id}'""")

            # Commit changes
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    def remove_module(self, module):
        try:
            # Get module code
            module_code = self.get_module_code(module)
            if module_code is None:
                logging.error(f"Module [{module}] doesn't exist.")
                return False

            # Check if the module exists
            self.cursor.execute(f"""SELECT * FROM module_master WHERE code = '{module_code}'""")
            if self.cursor.fetchone() is None:
                logging.error(f"Module with code [{module_code}] doesn't exist.")
                return False

            # Delete record
            self.cursor.execute(f"""DELETE FROM module_master WHERE code = '{module_code}'""")
            self.cursor.execute(f"""DELETE FROM module_details WHERE module_code = '{module_code}'""")

            # Commit changes
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    def remove_details(self, student_id, module_name, semester):
        try:
            # Get module code
            self.cursor.execute(f"""SELECT code FROM module_master WHERE name = '{module_name}'""")
            module_code = self.cursor.fetchone()[0]

            # Check if the module exists
            self.cursor.execute(f"""SELECT * FROM module_details WHERE student_id = {student_id} 
                            AND module_code = '{module_code}' AND semester = {semester}""")
            if self.cursor.fetchone() is None:
                logging.error(
                    f"Record with student id [{student_id}], module code [{module_code}] "
                    f"and semester [{semester}] doesn't exist.")
                return False

            # Delete record
            self.cursor.execute(f"""DELETE FROM module_details WHERE student_id = {student_id} 
                            AND module_code = '{module_code}' AND semester = {semester}""")

            # Commit changes
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    def remove_staff(self, staff_id):
        try:
            # Check if the staff exists
            self.cursor.execute(f"""SELECT * FROM staff WHERE staff_id = {staff_id}""")
            if self.cursor.fetchone() is None:
                logging.error(f"Staff with id [{staff_id}] doesn't exist.")
                return False

            # Delete record
            self.cursor.execute(f"""DELETE FROM staff WHERE staff_id = {staff_id}""")
            self.cursor.execute(f"""UPDATE student_master SET advisor_id = 'None' WHERE advisor_id = {staff_id}""")
            self.cursor.execute(f"""UPDATE programme SET director_id = 'None' WHERE director_id = {staff_id}""")
            self.cursor.execute(f"""UPDATE faculty SET admin_id = 'None' WHERE admin_id = {staff_id}""")

            # Delete credentials
            if self.cursor.execute(f"""SELECT * FROM credentials WHERE user_id = {staff_id}""").fetchone():
                self.cursor.execute(f"""DELETE FROM credentials WHERE user_id = {staff_id}""")
            # Commit changes
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    def remove_faculty(self, faculty):
        try:
            # Get faculty code
            faculty_code = self.get_faculty_code(faculty)
            if faculty_code is None:
                logging.error(f"Faculty [{faculty}] doesn't exist.")
                return False

            # Check if the faculty exists
            self.cursor.execute(f"""SELECT * FROM faculty WHERE faculty_code = '{faculty_code}'""")
            if self.cursor.fetchone() is None:
                logging.error(f"Faculty with code [{faculty_code}] doesn't exist.")
                return False

            # Delete record
            self.cursor.execute(f"""DELETE FROM faculty WHERE faculty_code = '{faculty_code}'""")
            self.cursor.execute(f"""UPDATE school SET faculty_code = 'None' WHERE faculty_code = '{faculty_code}'""")

            # Commit changes
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    def remove_school(self, school):
        try:
            # Get school code
            school_code = self.get_school_code(school)
            if school_code is None:
                logging.error(f"School [{school}] doesn't exist.")
                return False

            # Check if the school exists
            self.cursor.execute(f"""SELECT * FROM school WHERE school_code = '{school_code}'""")
            if self.cursor.fetchone() is None:
                logging.error(f"School with code [{school_code}] doesn't exist.")
                return False

            # Delete record
            self.cursor.execute(f"""DELETE FROM school WHERE school_code = '{school_code}'""")
            self.cursor.execute(f"""UPDATE programme SET school_code = 'None' WHERE school_code = '{school_code}'""")
            self.cursor.execute(f"""UPDATE student_master SET school_code = 'None' 
            WHERE school_code = '{school_code}'""")

            # Commit changes
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    def remove_programme(self, programme):
        try:
            # Get programme code
            programme_code = self.get_programme_code(programme)
            if programme_code is None:
                logging.error(f"Programme [{programme}] doesn't exist.")
                return False

            # Check if the programme exists
            self.cursor.execute(f"""SELECT * FROM programme WHERE programme_code = '{programme_code}'""")
            if self.cursor.fetchone() is None:
                logging.error(f"Programme with code [{programme_code}] doesn't exist.")
                return False

            # Delete record
            self.cursor.execute(f"""DELETE FROM programme WHERE programme_code = '{programme_code}'""")
            self.cursor.execute(
                f"""UPDATE student_master SET programme_code = 'None' WHERE programme_code = '{programme_code}'""")

            # Commit changes
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False
