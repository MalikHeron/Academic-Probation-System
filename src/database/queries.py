import logging
import sqlite3
from sqlite3 import Error

from database.sql import *
from prolog_interface import PrologQueryHandler as Prolog


class DatabaseManager:

    def __init__(self, db_file_path='../data/student_grades.db'):
        self.db_file = db_file_path
        self.create_tables()
        self.check_and_insert_data()

    def create_connection(self):
        try:
            return sqlite3.connect(self.db_file)
        except Error as e:
            logging.error(f"An error occurred: {e}")

    @staticmethod
    def close_connection(conn):
        try:
            conn.close()
        except Error as e:
            logging.error(f"An error occurred: {e}")

    def execute_sql(self, sql, values=None):
        conn = self.create_connection()
        cursor = conn.cursor()
        try:
            if values:
                cursor.execute(sql, values)
            else:
                cursor.execute(sql)
                if sql == sql_create_details_table:
                    try:
                        cursor.execute(sql_create_unique_index)
                    except Error:
                        # Ignore error if the index already exists
                        pass
            conn.commit()
        except Error as e:
            logging.error(f"An error occurred: {e}")
        finally:
            self.close_connection(conn)

    def create_tables(self):
        tables = [sql_create_students_table, sql_create_modules_table, sql_create_details_table,
                  sql_create_staff_table, sql_create_faculty_table, sql_create_programmes_table,
                  sql_create_school_table, sql_create_credentials_table]
        for table in tables:
            self.execute_sql(table)

    def check_and_insert_data(self):
        data_check = [self.get_students(), self.get_modules(), self.get_details(), self.get_staff(),
                      self.get_faculties(), self.get_schools(), self.get_programmes()]
        if not all(data_check):
            data_insert = [sql_insert_students, sql_insert_modules, sql_insert_details, sql_insert_staff,
                           sql_insert_faculty, sql_insert_programmes, sql_insert_schools, sql_insert_credentials]
            for data in data_insert:
                self.execute_sql(data)

    def get_credentials(self, username, password):
        conn = self.create_connection()
        cursor = conn.cursor()
        # Check if the credentials exist
        cursor.execute(
            f"""SELECT * FROM credentials WHERE username = '{username}' AND password = '{password}'""")
        # Return None if the credentials don't exist
        if cursor.fetchone() is None:
            self.close_connection(conn)
            return None

        # Return the user id if the credentials exist
        cursor.execute(
            f"""SELECT user_id FROM credentials WHERE username = '{username}' AND password = '{password}'""")
        user_id = cursor.fetchone()[0]
        self.close_connection(conn)
        return user_id

    def get_students(self):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, student_master.name, student_master.email, school.school_name AS school_code, 
            programme.programme_name AS programme_name, staff.name AS advisor_name 
            FROM student_master 
            LEFT JOIN school ON student_master.school_code = school.school_code
            LEFT JOIN programme ON student_master.programme_code = programme.programme_code
            LEFT JOIN staff ON student_master.advisor_id = staff.staff_id
            ORDER BY id
        """)
        data = cursor.fetchall()
        self.close_connection(conn)
        return data

    def get_modules(self):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM module_master ORDER BY name""")
        data = cursor.fetchall()
        self.close_connection(conn)
        return data

    def get_details(self):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute("""SELECT student_id, module_master.name AS module_name, grade_points, semester, year 
            FROM module_details 
            JOIN module_master ON module_details.module_code = module_master.code
            ORDER BY student_id
        """)
        data = cursor.fetchall()
        self.close_connection(conn)
        return data

    def get_staff(self):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM staff ORDER BY staff_id""")
        data = cursor.fetchall()
        self.close_connection(conn)
        return data

    def get_faculties(self):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute("""
                SELECT faculty_code, faculty_name, staff.name AS admin_name
                FROM faculty 
                LEFT JOIN staff ON faculty.admin_id = staff.staff_id
                ORDER BY faculty_code
            """)
        data = cursor.fetchall()
        self.close_connection(conn)
        return data

    def get_schools(self):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute("""
                SELECT school_code, school_name, faculty.faculty_name AS faculty_name, staff.name AS admin_name
                FROM school 
                LEFT JOIN faculty ON school.faculty_code = faculty.faculty_code
                LEFT JOIN staff ON faculty.admin_id = staff.staff_id
                ORDER BY school_code
            """)
        data = cursor.fetchall()
        self.close_connection(conn)
        return data

    def get_programmes(self, school_code=None):
        conn = self.create_connection()
        cursor = conn.cursor()
        if school_code is None:
            cursor.execute("""
                SELECT programme_code, programme_name, school.school_name AS school_name,
                staff.name AS director_name
                FROM programme 
                LEFT JOIN school ON programme.school_code = school.school_code
                LEFT JOIN staff ON programme.director_id = staff.staff_id
                ORDER BY programme_code
            """)
        else:
            cursor.execute(f"""SELECT * FROM programme WHERE school_code = '{school_code}' 
            ORDER BY programme_name""")
        data = cursor.fetchall()
        self.close_connection(conn)
        return data

    def get_years(self):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute("""SELECT DISTINCT year FROM module_details ORDER BY year""")
        data = cursor.fetchall()
        self.close_connection(conn)
        return data

    def get_advisors(self):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute(f"""SELECT * FROM staff WHERE position = 'Advisor' ORDER BY name""")
        data = cursor.fetchall()
        self.close_connection(conn)
        return data

    def get_directors(self):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute(f"""SELECT * FROM staff WHERE position = 'Director' ORDER BY name""")
        data = cursor.fetchall()
        self.close_connection(conn)
        return data

    def get_administrators(self):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute(f"""SELECT * FROM staff WHERE position = 'Administrator' ORDER BY name""")
        data = cursor.fetchall()
        self.close_connection(conn)
        return data

    def get_student(self, student_id):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute(f"""SELECT * FROM student_master WHERE id = {student_id}""")
        Prolog.assert_student(cursor.fetchone())
        self.close_connection(conn)

    def get_module(self, module_code):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute(f"""SELECT * FROM module_master WHERE code = '{module_code}'""")
        Prolog.assert_module(cursor.fetchone())
        self.close_connection(conn)

    def get_programme(self, programme_name):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute(f"""SELECT * FROM programme WHERE programme_name = '{programme_name}'""")
        data = cursor.fetchone()
        self.close_connection(conn)
        return data

    def get_school(self, school_name):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute(f"""SELECT * FROM school WHERE school_name = '{school_name}'""")
        data = cursor.fetchone()
        self.close_connection(conn)
        return data

    def get_advisor(self, advisor_name):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute(f"""SELECT * FROM staff WHERE name = '{advisor_name}'""")
        data = cursor.fetchone()
        self.close_connection(conn)
        return data

    def get_staff_name(self, staff_id):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute(f"""SELECT name FROM staff WHERE staff_id = {staff_id}""")
        data = cursor.fetchone()[0]
        self.close_connection(conn)
        return data

    def get_module_code(self, module):
        conn = self.create_connection()
        cursor = conn.cursor()
        # Check if the module is a code
        cursor.execute(f"""SELECT * FROM module_master WHERE code = '{module}'""")
        if cursor.fetchone() is not None:
            self.close_connection(conn)
            return module  # Return the module as is if it's a code

        # If the module is not a code, assume it's a name and get the code
        cursor.execute(f"""SELECT code FROM module_master WHERE name = '{module}'""")
        result = cursor.fetchone()
        if result is not None:
            self.close_connection(conn)
            return result[0]  # Return the code corresponding to the module name

        self.close_connection(conn)
        return None  # Return None if the module is neither a code nor a name

    def get_faculty_code(self, faculty):
        conn = self.create_connection()
        cursor = conn.cursor()
        # Check if the faculty is a code
        cursor.execute(f"""SELECT * FROM faculty WHERE faculty_code = '{faculty}'""")
        if cursor.fetchone() is not None:
            self.close_connection(conn)
            return faculty  # Return the faculty as is if it's a code

        # If the faculty is not a code, assume it's a name and get the code
        cursor.execute(f"""SELECT faculty_code FROM faculty WHERE faculty_name = '{faculty}'""")
        result = cursor.fetchone()
        if result is not None:
            self.close_connection(conn)
            return result[0]  # Return the code corresponding to the faculty name

        self.close_connection(conn)
        return None  # Return None if the faculty is neither a code nor a name

    def get_school_code(self, school):
        conn = self.create_connection()
        cursor = conn.cursor()
        # Check if the school is a code
        cursor.execute(f"""SELECT * FROM school WHERE school_code = '{school}'""")
        if cursor.fetchone() is not None:
            self.close_connection(conn)
            return school  # Return the school as is if it's a code

        # If the school is not a code, assume it's a name and get the code
        cursor.execute(f"""SELECT school_code FROM school WHERE school_name = '{school}'""")
        result = cursor.fetchone()
        if result is not None:
            self.close_connection(conn)
            return result[0]  # Return the code corresponding to the school name

        self.close_connection(conn)
        return None  # Return None if the school is neither a code nor a name

    def get_programme_code(self, programme):
        conn = self.create_connection()
        cursor = conn.cursor()
        # Check if the programme is a code
        cursor.execute(f"""SELECT * FROM programme WHERE programme_code = '{programme}'""")
        if cursor.fetchone() is not None:
            self.close_connection(conn)
            return programme  # Return the programme as is if it's a code

        # If the programme is not a code, assume it's a name and get the code
        cursor.execute(f"""SELECT programme_code FROM programme WHERE programme_name = '{programme}'""")
        result = cursor.fetchone()
        if result is not None:
            self.close_connection(conn)
            return result[0]  # Return the code corresponding to the programme name

        self.close_connection(conn)
        return None  # Return None if the programme is neither a code nor a name

    def get_student_advisor(self, student_id):
        conn = self.create_connection()
        cursor = conn.cursor()
        # Get advisor id
        cursor.execute(f"""SELECT advisor_id FROM student_master WHERE id = {student_id}""")
        advisor_id = cursor.fetchone()[0]

        if advisor_id == 'None':
            self.close_connection(conn)
            return None

        # Get advisor details
        cursor.execute(f"""SELECT * FROM staff WHERE staff_id = {advisor_id}""")
        data = cursor.fetchone()
        self.close_connection(conn)
        return data

    def get_programme_name(self, programme_code):
        conn = self.create_connection()
        cursor = conn.cursor()
        if programme_code == 'None':
            return None
        cursor.execute(f"""SELECT programme_name FROM programme WHERE programme_code = '{programme_code}'""")
        data = cursor.fetchone()[0]
        self.close_connection(conn)
        return data

    def get_programme_director(self, programme_code):
        conn = self.create_connection()
        cursor = conn.cursor()
        if programme_code == 'None':
            self.close_connection(conn)
            return None

        # Get director id
        cursor.execute(f"""SELECT director_id FROM programme WHERE programme_code = '{programme_code}'""")
        director_id = cursor.fetchone()[0]

        if director_id is None:
            self.close_connection(conn)
            return None

        # Get director details
        cursor.execute(f"""SELECT * FROM staff WHERE staff_id = {director_id}""")
        data = cursor.fetchone()
        self.close_connection(conn)
        return data

    def get_school_name(self, school_code):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute(f"""SELECT school_name FROM school WHERE school_code = '{school_code}'""")
        data = cursor.fetchone()[0]
        self.close_connection(conn)
        return data

    def get_school_administrator(self, school_code):
        conn = self.create_connection()
        cursor = conn.cursor()
        # Get faculty code
        cursor.execute(f"""SELECT faculty_code FROM school WHERE school_code = '{school_code}'""")
        faculty_code = cursor.fetchone()[0]

        if faculty_code is None:
            self.close_connection(conn)
            return None

        # Get administrator id
        cursor.execute(f"""SELECT admin_id FROM faculty WHERE faculty_code = '{faculty_code}'""")
        admin_id = cursor.fetchone()[0]

        if admin_id is None:
            self.close_connection(conn)
            return None

        # Get administrator details
        cursor.execute(f"""SELECT * FROM staff WHERE staff_id = {admin_id}""")
        data = cursor.fetchone()
        self.close_connection(conn)
        return data

    def update_knowledge_base(self, year):
        conn = self.create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(f"""SELECT * FROM module_details WHERE year = '{year}'""")
            results = cursor.fetchall()

            for result in results:
                Prolog.assert_details(result)
                self.get_student(result[0])
                self.get_module(result[1])

            self.close_connection(conn)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False
        finally:
            self.close_connection(conn)

    def insert_detail(self, id_number, module_name, gpa, semester, year):
        conn = self.create_connection()
        cursor = conn.cursor()
        try:
            # Get module code
            cursor.execute(f"""SELECT code FROM module_master WHERE name = '{module_name}'""")
            module_code = cursor.fetchone()[0]

            # Insert details
            cursor.execute(
                f"""INSERT INTO module_details VALUES ({id_number}, '{module_code}', {gpa}, {semester}, '{year}')""")

            # Commit changes
            conn.commit()
            self.close_connection(conn)
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False
        finally:
            self.close_connection(conn)

    def insert_student(self, student_id, name, email, school_name, programme_name, advisor_name):
        conn = self.create_connection()
        cursor = conn.cursor()
        try:
            # Get school, programme and advisor
            school = self.get_school(school_name)
            programme = self.get_programme(programme_name)
            if advisor_name != 'None':
                advisor = self.get_advisor(advisor_name)[0]
            else:
                advisor = 'NULL'

            cursor.execute(
                f"""INSERT INTO student_master VALUES ({student_id}, '{name}', '{email}', 
                '{school[0]}', '{programme[0]}', {advisor})""")

            # Commit changes
            conn.commit()
            self.close_connection(conn)
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False
        finally:
            self.close_connection(conn)

    def insert_module(self, module_code, module_name, credit):
        conn = self.create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(f"""INSERT INTO module_master VALUES ('{module_code}', '{module_name}', {credit})""")

            # Commit changes
            conn.commit()
            self.close_connection(conn)
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False
        finally:
            self.close_connection(conn)

    def insert_staff(self, id_number, name, email, position, username, password):
        conn = self.create_connection()
        cursor = conn.cursor()
        try:
            # Insert details
            cursor.execute(
                f"""INSERT INTO staff VALUES ({id_number}, '{name}', '{email}', '{position}')""")

            # Insert credentials
            cursor.execute(
                f"""INSERT INTO credentials VALUES ({id_number}, '{username}', '{password}')""")

            # Commit changes
            conn.commit()
            self.close_connection(conn)
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False
        finally:
            self.close_connection(conn)

    def insert_faculty(self, faculty_code, faculty_name, admin_name):
        conn = self.create_connection()
        cursor = conn.cursor()
        try:
            # Get admin id
            if admin_name != 'None':
                cursor.execute(f"""SELECT staff_id FROM staff WHERE name = '{admin_name}'""")
                admin_id = cursor.fetchone()[0]
            else:
                admin_id = 'NULL'

            # Insert details
            cursor.execute(
                f"""INSERT INTO faculty VALUES ('{faculty_code}', '{faculty_name}', {admin_id})""")

            # Commit changes
            conn.commit()
            self.close_connection(conn)
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False
        finally:
            self.close_connection(conn)

    def insert_programme(self, programme_code, programme_name, school_name, director_name):
        conn = self.create_connection()
        cursor = conn.cursor()
        try:
            # Get director id
            if director_name != 'None':
                cursor.execute(f"""SELECT staff_id FROM staff WHERE name = '{director_name}'""")
                director_id = cursor.fetchone()[0]
            else:
                director_id = 'NULL'

            # Get school code
            if school_name != 'None':
                cursor.execute(f"""SELECT school_code FROM school WHERE school_name = '{school_name}'""")
                school_code = cursor.fetchone()[0]
            else:
                school_code = 'NULL'

            # Insert details
            cursor.execute(
                f"""INSERT INTO programme VALUES ('{programme_code}', '{programme_name}', '{school_code}', 
                {director_id})""")

            # Commit changes
            conn.commit()
            self.close_connection(conn)
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False
        finally:
            self.close_connection(conn)

    def insert_school(self, school_code, school_name, faculty_name):
        conn = self.create_connection()
        cursor = conn.cursor()
        try:
            # Get faculty code
            if faculty_name != 'None':
                cursor.execute(f"""SELECT faculty_code FROM faculty WHERE faculty_name = '{faculty_name}'""")
                faculty_code = cursor.fetchone()[0]
            else:
                faculty_code = 'NULL'

            # Insert details
            cursor.execute(
                f"""INSERT INTO school VALUES ('{school_code}', '{school_name}', '{faculty_code}')""")

            # Commit changes
            conn.commit()
            self.close_connection(conn)
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False
        finally:
            self.close_connection(conn)

    def update_record(self, data, table_name):
        conn = self.create_connection()
        cursor = conn.cursor()
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

                    cursor.execute(
                        f"""UPDATE student_master SET name='{data[1]}', email='{data[2]}', school_code='{school[0]}', 
                    programme_code='{programme[0]}', advisor_id={advisor} WHERE id={data[0]}""")
                case "module":
                    cursor.execute(f"""UPDATE module_master SET name='{data[1]}', credits={data[2]} 
                    WHERE code='{data[0]}'""")
                case "details":
                    # Get module code
                    cursor.execute(f"""SELECT * FROM module_master WHERE name = '{data[1]}'""")
                    module_code = cursor.fetchone()[0]

                    cursor.execute(f"""UPDATE module_details SET grade_points={data[2]}, 
                    semester={data[3]}, year='{data[4]}'
                    WHERE student_id={data[0]} AND module_code='{module_code}'""")
                case "staff":
                    cursor.execute(f"""UPDATE staff SET name='{data[1]}', email='{data[2]}', position='{data[3]}' 
                    WHERE staff_id={data[0]}""")

                    if data[3] == 'Administrator':
                        if cursor.execute(f"""SELECT * FROM credentials WHERE user_id = {data[0]}""").fetchone():
                            # Update credentials
                            cursor.execute(f"""UPDATE credentials SET username='{data[4]}', password='{data[5]}' 
                            WHERE user_id={data[0]}""")
                        else:
                            # Insert credentials
                            cursor.execute(f"""INSERT INTO credentials VALUES 
                            ({data[0]}, '{data[4]}', '{data[5]}')""")
                case "faculty":
                    # Get admin id
                    if data[2] != 'None':
                        cursor.execute(f"""SELECT * FROM staff WHERE name = '{data[2]}'""")
                        admin_id = cursor.fetchone()[0]
                    else:
                        admin_id = 'NULL'

                    cursor.execute(f"""UPDATE faculty SET admin_id={admin_id}, faculty_name='{data[1]}' 
                    WHERE faculty_code='{data[0]}'""")
                case "school":
                    # Get faculty code
                    if data[2] != 'None':
                        cursor.execute(f"""SELECT * FROM faculty WHERE faculty_name = '{data[2]}'""")
                        faculty_code = cursor.fetchone()[0]
                    else:
                        faculty_code = 'NULL'

                    cursor.execute(f"""UPDATE school SET faculty_code='{faculty_code}', school_name='{data[1]}' 
                    WHERE school_code='{data[0]}'""")
                case "programme":
                    # Get director id
                    if data[3] != 'None':
                        cursor.execute(f"""SELECT * FROM staff WHERE name = '{data[3]}'""")
                        director_id = cursor.fetchone()[0]
                    else:
                        director_id = 'NULL'

                    # Get school code
                    if data[2] != 'None':
                        cursor.execute(f"""SELECT * FROM school WHERE school_name = '{data[2]}'""")
                        school_code = cursor.fetchone()[0]
                    else:
                        school_code = 'NULL'

                    cursor.execute(
                        f"""UPDATE programme SET director_id={director_id},  programme_name='{data[1]}', 
                        school_code='{school_code}' WHERE programme_code='{data[0]}'""")
                case _:
                    print("Record could not be updated.")

            # Commit changes
            conn.commit()
            self.close_connection(conn)
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False
        finally:
            self.close_connection(conn)

    def delete_student(self, student_id):
        conn = self.create_connection()
        cursor = conn.cursor()
        try:
            # Check if the student exists
            cursor.execute(f"""SELECT * FROM student_master WHERE id = {student_id}""")
            if cursor.fetchone() is None:
                self.close_connection(conn)
                logging.error(f"Student with id [{student_id}] doesn't exist.")
                return False

            # Delete record
            cursor.execute(f"""DELETE FROM student_master WHERE id = {student_id}""")
            cursor.execute(f"""DELETE FROM module_details WHERE student_id = '{student_id}'""")

            # Commit changes
            conn.commit()
            self.close_connection(conn)
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False
        finally:
            self.close_connection(conn)

    def delete_module(self, module):
        conn = self.create_connection()
        cursor = conn.cursor()
        try:
            # Get module code
            module_code = self.get_module_code(module)
            if module_code is None:
                self.close_connection(conn)
                logging.error(f"Module [{module}] doesn't exist.")
                return False

            # Check if the module exists
            cursor.execute(f"""SELECT * FROM module_master WHERE code = '{module_code}'""")
            if cursor.fetchone() is None:
                self.close_connection(conn)
                logging.error(f"Module with code [{module_code}] doesn't exist.")
                return False

            # Delete record
            cursor.execute(f"""DELETE FROM module_master WHERE code = '{module_code}'""")
            cursor.execute(f"""DELETE FROM module_details WHERE module_code = '{module_code}'""")

            # Commit changes
            conn.commit()
            self.close_connection(conn)
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False
        finally:
            self.close_connection(conn)

    def delete_details(self, student_id, module_name, semester, year):
        conn = self.create_connection()
        cursor = conn.cursor()
        try:
            # Get module code
            cursor.execute(f"""SELECT code FROM module_master WHERE name = '{module_name}'""")
            module_code = cursor.fetchone()[0]

            # Check if the module exists
            cursor.execute(f"""SELECT * FROM module_details WHERE student_id = {student_id} 
                            AND module_code = '{module_code}' AND semester = {semester} AND year = '{year}'""")
            if cursor.fetchone() is None:
                self.close_connection(conn)
                logging.error(
                    f"Record with student id [{student_id}], module code [{module_code}] "
                    f"and semester [{semester}] doesn't exist.")
                return False

            # Delete record
            cursor.execute(f"""DELETE FROM module_details WHERE student_id = {student_id} 
                            AND module_code = '{module_code}' AND semester = {semester} AND year = '{year}'""")

            # Commit changes
            conn.commit()
            self.close_connection(conn)
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False
        finally:
            self.close_connection(conn)

    def delete_staff(self, staff_id):
        conn = self.create_connection()
        cursor = conn.cursor()
        try:
            # Check if the staff exists
            cursor.execute(f"""SELECT * FROM staff WHERE staff_id = {staff_id}""")
            if cursor.fetchone() is None:
                self.close_connection(conn)
                logging.error(f"Staff with id [{staff_id}] doesn't exist.")
                return False

            # Delete record
            cursor.execute(f"""DELETE FROM staff WHERE staff_id = {staff_id}""")
            cursor.execute(f"""UPDATE student_master SET advisor_id = 'None' WHERE advisor_id = {staff_id}""")
            cursor.execute(f"""UPDATE programme SET director_id = 'None' WHERE director_id = {staff_id}""")
            cursor.execute(f"""UPDATE faculty SET admin_id = 'None' WHERE admin_id = {staff_id}""")

            # Delete credentials
            if cursor.execute(f"""SELECT * FROM credentials WHERE user_id = {staff_id}""").fetchone():
                cursor.execute(f"""DELETE FROM credentials WHERE user_id = {staff_id}""")
            # Commit changes
            conn.commit()
            self.close_connection(conn)
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False
        finally:
            self.close_connection(conn)

    def delete_faculty(self, faculty):
        conn = self.create_connection()
        cursor = conn.cursor()
        try:
            # Get faculty code
            faculty_code = self.get_faculty_code(faculty)
            if faculty_code is None:
                self.close_connection(conn)
                logging.error(f"Faculty [{faculty}] doesn't exist.")
                return False

            # Check if the faculty exists
            cursor.execute(f"""SELECT * FROM faculty WHERE faculty_code = '{faculty_code}'""")
            if cursor.fetchone() is None:
                self.close_connection(conn)
                logging.error(f"Faculty with code [{faculty_code}] doesn't exist.")
                return False

            # Delete record
            cursor.execute(f"""DELETE FROM faculty WHERE faculty_code = '{faculty_code}'""")
            cursor.execute(f"""UPDATE school SET faculty_code = 'None' WHERE faculty_code = '{faculty_code}'""")

            # Commit changes
            conn.commit()
            self.close_connection(conn)
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False
        finally:
            self.close_connection(conn)

    def delete_school(self, school):
        conn = self.create_connection()
        cursor = conn.cursor()
        try:
            # Get school code
            school_code = self.get_school_code(school)
            if school_code is None:
                self.close_connection(conn)
                logging.error(f"School [{school}] doesn't exist.")
                return False

            # Check if the school exists
            cursor.execute(f"""SELECT * FROM school WHERE school_code = '{school_code}'""")
            if cursor.fetchone() is None:
                self.close_connection(conn)
                logging.error(f"School with code [{school_code}] doesn't exist.")
                return False

            # Delete record
            cursor.execute(f"""DELETE FROM school WHERE school_code = '{school_code}'""")
            cursor.execute(f"""UPDATE programme SET school_code = 'None' WHERE school_code = '{school_code}'""")
            cursor.execute(f"""UPDATE student_master SET school_code = 'None' 
            WHERE school_code = '{school_code}'""")

            # Commit changes
            conn.commit()
            self.close_connection(conn)
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False
        finally:
            self.close_connection(conn)

    def delete_programme(self, programme):
        conn = self.create_connection()
        cursor = conn.cursor()
        try:
            # Get programme code
            programme_code = self.get_programme_code(programme)
            if programme_code is None:
                self.close_connection(conn)
                logging.error(f"Programme [{programme}] doesn't exist.")
                return False

            # Check if the programme exists
            cursor.execute(f"""SELECT * FROM programme WHERE programme_code = '{programme_code}'""")
            if cursor.fetchone() is None:
                self.close_connection(conn)
                logging.error(f"Programme with code [{programme_code}] doesn't exist.")
                return False

            # Delete record
            cursor.execute(f"""DELETE FROM programme WHERE programme_code = '{programme_code}'""")
            cursor.execute(
                f"""UPDATE student_master SET programme_code = 'None' WHERE programme_code = '{programme_code}'""")

            # Commit changes
            conn.commit()
            self.close_connection(conn)
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False
        finally:
            self.close_connection(conn)
