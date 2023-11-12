import logging
import os

from pyswip import Prolog

# pip install git+https://github.com/yuce/pyswip@master
# python.exe -m pip install --upgrade pip

# Create the logs and data directories if they do not exist
if not os.path.exists("../../logs"):
    os.makedirs("../../logs")
if not os.path.exists("../../data"):
    os.makedirs("../../data")

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
    def assert_student(student):
        try:
            if not list(prolog.query(f"student({student[0]}, Name, Email, School, Programme)")):
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
    def assert_module(module):
        try:
            if not list(prolog.query(f"module('{module[0]}', Name, Credits)")):
                prolog.assertz(f"module('{module[0]}', '{module[1]}', {module[2]})")
                check = list(prolog.query(f"module('{module[0]}', Name, Credits)"))
                if not check:
                    logging.error("Failed to add module information.")
                    return None
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None

    @staticmethod
    def assert_details(detail):
        try:
            if not list(prolog.query(f"module_details({detail[0]}, '{detail[1]}', "
                                     f"{detail[2]}, {detail[3]}, Year)")):
                prolog.assertz(
                    f"module_details({detail[0]}, '{detail[1]}', "
                    f"{detail[2]}, {detail[3]}, {detail[4]})"
                )
                check = list(prolog.query(f"module_details({detail[0]}, '{detail[1]}', "
                                          f"{detail[2]}, {detail[3]}, Year)"))
                if not check:
                    logging.error("Failed to add detail information.")
                    return None
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None

    @staticmethod
    def calculate_cumulative_gpa():
        try:
            result = list(prolog.query(f"cumulative_gpa_all_students(Results)"))
            if result is None:
                return None
            else:
                logging.info(result)
                return result
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None
