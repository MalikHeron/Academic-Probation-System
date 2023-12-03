import logging  # Import the logging module
import os  # Import the os module

from pyswip import Prolog  # Import the Prolog class from the pyswip module

# Create the logs and data directories if they do not exist
if not os.path.exists("logs"):
    os.makedirs("logs")  # Create a logs directory
if not os.path.exists("data"):
    os.makedirs("data")  # Create a data directory
if not os.path.exists("reports"):
    os.makedirs("reports")  # Create a reports directory
if not os.path.exists("config"):
    os.makedirs("config")  # Create a config directory

# Configure the logging module
logging.basicConfig(filename='logs/app.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')  # Set the basic configuration for the logging
logging.getLogger().setLevel(logging.INFO)  # Set logger's level to INFO

# Connects the application to the prolog knowledge base
prolog = Prolog()  # Create a Prolog instance
prolog.consult("prolog/knowledge_base.pl")  # Consult the Prolog knowledge base file


# Define a class to handle Prolog queries
class PrologQueryHandler:

    @staticmethod
    def update_gpa(gpa):  # Method to update the GPA
        try:
            result = list(prolog.query(f"update_default_gpa({gpa})"))  # Query to update the GPA
            if result is None:
                return None
            else:
                return result
        except Exception as e:
            logging.error(f"An error occurred: {e}")  # Log the error
        return None

    @staticmethod
    def get_default_gpa():  # Method to get the default GPA
        try:
            result = list(prolog.query(f"default_gpa(GPA)"))  # Query to get the default GPA
            if result is None:
                return None
            else:
                return result[0]['GPA']
        except Exception as e:
            logging.error(f"An error occurred: {e}")  # Log the error
            return None

    @staticmethod
    def assert_student(student):  # Method to assert a student
        try:
            # Query to check if the student exists
            if not list(prolog.query(
                    f"student({student[0]}, Name, Email, School, Programme)")):
                # Assert the student
                prolog.assertz(
                    f"student({student[0]}, '{student[1]}', "
                    f"'{student[2]}', '{student[3]}', '{student[4]}')"
                )
                # Query to check if the student was asserted
                check = list(prolog.query(
                    f"student({student[0]}, Name, Email, School, Programme)"))
                if not check:
                    logging.error("Failed to add student information.")  # Log the error
                    return None
        except Exception as e:
            logging.error(f"An error occurred: {e}")  # Log the error
            return None

    @staticmethod
    def assert_module(module):  # Method to assert a module
        try:
            # Query to check if the module exists
            if not list(prolog.query(f"module('{module[0]}', Name, Credits)")):
                # Assert the module
                prolog.assertz(f"module('{module[0]}', '{module[1]}', {module[2]})")
                # Query to check if the module was asserted
                check = list(
                    prolog.query(f"module('{module[0]}', Name, Credits)"))
                if not check:
                    logging.error("Failed to add module information.")  # Log the error
                    return None
        except Exception as e:
            logging.error(f"An error occurred: {e}")  # Log the error
            return None

    @staticmethod
    def assert_details(detail):  # Method to assert details
        try:
            # Query to check if the details exist
            if not list(prolog.query(f"module_details({detail[0]}, '{detail[1]}', "
                                     f"{detail[2]}, {detail[3]}, Year)")):
                # Assert the details
                prolog.assertz(
                    f"module_details({detail[0]}, '{detail[1]}', "
                    f"{detail[2]}, {detail[3]}, {detail[4]})"
                )
                # Query to check if the details were asserted
                check = list(prolog.query(f"module_details({detail[0]}, '{detail[1]}', "
                                          f"{detail[2]}, {detail[3]}, Year)"))
                if not check:
                    logging.error("Failed to add detail information.")  # Log the error
                    return None
        except Exception as e:
            logging.error(f"An error occurred: {e}")  # Log the error
            return None

    @staticmethod
    def calculate_cumulative_gpa():  # Method to calculate the cumulative GPA
        try:
            # Query to calculate the cumulative GPA
            result = list(
                prolog.query(f"cumulative_gpa_all_students(Results)"))
            if result is None:
                return None
            else:
                logging.info(result)  # Log the result
                return result
        except Exception as e:
            logging.error(f"An error occurred: {e}")  # Log the error
            return None
