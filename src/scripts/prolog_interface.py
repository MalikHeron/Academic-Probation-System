import logging

from swiplserver import PrologMQI, create_posix_path

# pip install git+https://github.com/yuce/pyswip@master
# python.exe -m pip install --upgrade pip

# Configure the logging module
logging.basicConfig(filename='../../logs/app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
# Path to prolog file
path = create_posix_path("../prolog/knowledge_base.pl")


class PrologQueryHandler:

    @staticmethod
    def update_gpa(gpa):
        try:
            with PrologMQI() as mqi:
                with mqi.create_thread() as prolog_thread:
                    prolog_thread.query(f'consult("{path}").')
                    prolog_thread.query_async(f"update_default_gpa({gpa})", find_all=False)
                    while True:
                        result = prolog_thread.query_async_result()
                        if result is None:
                            break
                        else:
                            logging.info(result)
                            return result
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None

    @staticmethod
    def get_default_gpa():
        try:
            with PrologMQI() as mqi:
                with mqi.create_thread() as prolog_thread:
                    prolog_thread.query(f'consult("{path}").')
                    prolog_thread.query_async(f"default_gpa(GPA)", find_all=False)
                    while True:
                        result = prolog_thread.query_async_result()
                        if result is None:
                            break
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
            with PrologMQI() as mqi:
                with mqi.create_thread() as prolog_thread:
                    prolog_thread.query(f'consult("{path}").')
                    # TODO
                    prolog_thread.query_async(f"", find_all=False)
                    while True:
                        result = prolog_thread.query_async_result()
                        if result is None:
                            break
                        else:
                            logging.info(result)
                            return result
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None
