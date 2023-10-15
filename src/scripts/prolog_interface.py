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
                gpa = result[0]['GPA']
                return gpa
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None

    @staticmethod
    def get_student_list():
        try:
            # TODO
            result = list(prolog.query(f""))
            if result is None:
                return None
            else:
                logging.info(result)
                return result
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None
