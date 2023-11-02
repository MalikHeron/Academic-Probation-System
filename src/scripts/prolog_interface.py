import logging

from pyswip import Prolog

# pip install git+https://github.com/yuce/pyswip@master
# python.exe -m pip install --upgrade pip

# Configure the logging module
logging.basicConfig(filename='../../logs/app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.getLogger().setLevel(logging.INFO)  # Set logger's level to INFO

# Connects the application to the prolog knowledge base
prolog = Prolog()
prolog.consult("../prolog/knowledge_base.pl")


class PrologQueryHandler:

    @staticmethod
    def update_gpa(gpa):
        try:
            result = list(prolog.query(f"update_default_gpa({gpa})"))
            if result is None:
                return None
            else:
                logging.info(result)
                return result
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        return None

    @staticmethod
    def get_default_gpa():
        try:
            result = list(prolog.query(f"default_gpa(GPA)"))
            if result is None:
                return None
            else:
                logging.info(result)
                return result[0]['GPA']
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None

    @staticmethod
    def add_student(student):
        try:
            prolog.assertz(
                f"student({student[0]}, '{student[1]}', "
                f"'{student[2]}', '{student[3]}', '{student[4]}')"
            )
            check = list(prolog.query(f"student({student[0]}, Name, Email, School, Programme)"))
            if not check:
                logging.error("Failed to add student information.")
                return None
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None

    @staticmethod
    def add_module(module):
        try:
            prolog.assertz(f"module('{module[0]}', '{module[1]}', {module[2]})")
            check = list(prolog.query(f"module('{module[0]}', Name, Credits)"))
            if not check:
                logging.error("Failed to add module information.")
                return None
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None

    @staticmethod
    def add_details(detail):
        try:
            prolog.assertz(
                f"module_details({detail[0]}, '{detail[1]}', "
                f"{detail[2]}, {detail[3]}, {detail[4]})"
            )
            check = list(prolog.query(f"module_details({detail[0]}, Module, GradePoint, Semester, Year)"))
            if not check:
                logging.error("Failed to add detail information.")
                return None
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None

    @staticmethod
    def get_student_list():
        try:
            result = list(prolog.query("student(Id, Name, Email, School, Programme)"))
            if result is None:
                return None
            else:
                logging.info(result)
                return result
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None

    @staticmethod
    def get_module_list():
        try:
            result = list(prolog.query("module(Code, Name, Credits)"))
            if result is None:
                return None
            else:
                logging.info(result)
                return result
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None

    @staticmethod
    def get_details_list():
        try:
            result = list(prolog.query("module_details(Id, Code, Grade_Points, Semester, Year)"))
            if result is None:
                return None
            else:
                logging.info(result)
                return result
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None

    @staticmethod
    def remove_student(student_id):
        try:
            list(prolog.query(f"remove_student({student_id})"))
            check = list(prolog.query(f"student({student_id}, _, _, _, _)"))
            if not check:
                logging.error("Failed to remove student information.")
                return None
            else:
                logging.info("Student Removed.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None

    @staticmethod
    def remove_module(module_code):
        try:
            list(prolog.query(f"remove_module({module_code})"))
            check = list(prolog.query(f"module({module_code}, _, _)"))
            if not check:
                logging.error("Failed to remove module information.")
                return None
            else:
                logging.info("Module Removed.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None

    @staticmethod
    def remove_details(student_id, module_code, semester):
        try:
            list(prolog.query(f"remove_module_details({student_id}, {module_code}, {semester})"))
            check = list(prolog.query(f"module_details({student_id}, {module_code}, _, {semester}, _)"))
            if not check:
                logging.error("Failed to remove details information.")
                return None
            else:
                logging.info("Details Removed.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None

    @staticmethod
    def calculate_cumulative_gpa(year):
        try:
            result = list(prolog.query(f"cumulative_gpa_all_students({year}, Results)"))
            if result is None:
                return None
            else:
                logging.info(result)
                return result
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None
