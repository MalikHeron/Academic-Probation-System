import logging

from pyswip import Prolog

# pip install git+https://github.com/yuce/pyswip@master
# python.exe -m pip install --upgrade pip

# Configure the logging module
logging.basicConfig(filename='../../logs/app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

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
    def get_student_list():
        try:
            result = list(prolog.query("student_master(Id, Name, Email, School, Programme)"))
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
            result = list(prolog.query("module_master(Code, Name, Credits)"))
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
    def calculate_cumulative_gpa():
        try:
            result = list(prolog.query("cumulative_gpa(StudentId, Name, GPA1, GPA2, CumulativeGPA)"))
            if result is None:
                return None
            else:
                logging.info(result)
                print(result)
                return result
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None


PrologQueryHandler.calculate_cumulative_gpa()
