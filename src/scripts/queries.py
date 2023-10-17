# SQL for creating tables
sql_create_students_table = """CREATE TABLE IF NOT EXISTS student_master (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    email text NOT NULL,
                                    school text NOT NULL,
                                    programme text NOT NULL
                                );"""

sql_create_modules_table = """CREATE TABLE IF NOT EXISTS module_master (
                                    code text PRIMARY KEY,
                                    credits integer NOT NULL
                                );"""

sql_create_details_table = """CREATE TABLE IF NOT EXISTS module_details (
                                student_id integer NOT NULL,
                                module_code text NOT NULL,
                                grade_points integer NOT NULL,
                                semester integer NOT NULL,
                                year integer NOT NULL,
                                FOREIGN KEY (student_id) REFERENCES student_master (id),
                                FOREIGN KEY (module_code) REFERENCES module_master (code)
                            );"""

sql_create_unique_index = """CREATE UNIQUE INDEX idx_module_details_unique ON 
                        module_details(student_id, module_code, semester, year
                        );"""

# SQL for retrieving data
sql_get_students = """SELECT * FROM student_master"""
sql_get_modules = """SELECT * FROM module_master"""
sql_get_details = """SELECT * FROM module_details"""

# Inserting data into student_master
sql_insert_students = """INSERT OR IGNORE INTO student_master (id, name, email, school, programme) VALUES
(1, 'John Doe', 'johndoe@gmail.com', 'School of Computing', 'Computer Science'),
(2, 'Jane Smith', 'janesmith@gmail.com', 'School of Business', 'Business Administration'),
(3, 'Robert Johnson', 'robertjohnson@gmail.com', 'School of Arts', 'Fine Arts'),
(4, 'Michael Williams', 'michaelwilliams@gmail.com', 'School of Engineering', 'Mechanical Engineering'),
(5, 'Sarah Brown', 'sarahbrown@gmail.com', 'School of Science', 'Biology'),
(6, 'David Jones', 'davidjones@gmail.com', 'School of Computing', 'Information Systems'),
(7, 'Emily Davis', 'emilydavis@gmail.com', 'School of Business', 'Accounting'),
(8, 'James Miller', 'jamesmiller@gmail.com', 'School of Arts', 'Music'),
(9, 'Jessica Wilson', 'jessicawilson@gmail.com', 'School of Engineering', 'Civil Engineering'),
(10, 'Thomas Moore', 'thomasmoore@gmail.com', 'School of Science', 'Physics');"""

# Inserting data into module_master
sql_insert_modules = """INSERT OR IGNORE INTO module_master(code, credits) VALUES
('CS101', 3),
('BA101', 3),
('FA101', 4),
('ME101', 4),
('BI101', 3),
('IS101', 2),
('AC101', 1),
('MU101', 1),
('CE101', 2),
('PH101', 4),
('MAT101', 4);"""

# Inserting data into module_details
sql_insert_details = """INSERT OR IGNORE INTO module_details(student_id, module_code, grade_points, semester, year) 
VALUES
(1, 'CS101', 3.67, 1, 2021),
(1, 'BA101', 2.00, 1, 2021),
(1, 'FA101', 3.33, 1, 2021),
(1, 'ME101', 2.33, 1, 2021),
(1, 'BI101', 1.30, 1, 2021),
(1, 'IS101', 3.00, 1, 2021),
(1, 'AC101', 4.00, 1, 2021),
(1, 'MU101', 4.30, 2, 2022),
(1, 'PH101', 3.67, 2, 2022),
(1, 'BI101', 3.00, 2, 2022),
(1, 'MAT101', 3.33, 2, 2022),
(1, 'CE101', 4.00, 2, 2022),
(2, 'CS101', 3.27, 1, 2018),
(2, 'BA101', 2.10, 1, 2018),
(2, 'FA101', 1.33, 1, 2018),
(2, 'ME101', 3.33, 1, 2018),
(2, 'BI101', 3.30, 2, 2019),
(2, 'IS101', 2.00, 2, 2019),
(2, 'AC101', 3.00, 2, 2019),
(3, 'MU101', 4.10, 1, 2017),
(3, 'PH101', 3.57, 1, 2017),
(3, 'BI101', 3.50, 1, 2017),
(3, 'MAT101', 3.13, 1, 2017),
(3, 'CE101', 2.00, 2, 2018),
(3, 'CS101', 1.67, 2, 2018),
(3, 'BA101', 1.90, 2, 2018),
(4, 'FA101', 3.13, 1, 2022),
(4, 'ME101', 2.63, 1, 2022),
(4, 'BI101', 1.90, 1, 2022),
(4, 'IS101', 3.10, 1, 2022),
(4, 'AC101', 3.20, 2, 2023),
(4, 'PH101', 2.67, 2, 2023),
(4, 'BI101', 2.00, 2, 2023),
(4, 'MAT101', 2.33, 2, 2023),
(4, 'CE101', 3.00, 2, 2023),
(5, 'CS101', 3.21, 1, 2016),
(5, 'BA101', 1.89, 1, 2016),
(5, 'FA101', 2.76, 1, 2016),
(5, 'ME101', 3.56, 1, 2016),
(5, 'BI101', 0.45, 1, 2016),
(5, 'IS101', 3.89, 1, 2016),
(5, 'AC101', 3.67, 1, 2016),
(5, 'MU101', 3.98, 2, 2017),
(5, 'PH101', 1.23, 2, 2017),
(5, 'BI101', 2.34, 2, 2017),
(5, 'MAT101', 3.56, 2, 2017),
(5, 'CE101', 3.78, 2, 2017),
(6, 'CS101', 1.67, 1, 2016),
(6, 'BA101', 1.90, 1, 2016),
(6, 'FA101', 1.33, 1, 2016),
(6, 'ME101', 1.56, 1, 2016),
(6, 'BI101', 0.78, 1, 2016),
(6, 'IS101', 2.45, 2, 2017),
(6, 'AC101', 2.89, 2, 2017),
(6, 'MU101', 2.56, 2, 2017),
(6, 'PH101', 1.23, 2, 2017),
(6, 'BI101', 2.34, 2, 2017),
(6, 'MAT101', 2.56, 2, 2017),
(6, 'CE101', 2.78, 2, 2017),
(7, 'CS101', 1.67, 1, 2018),
(7, 'BA101', 1.90, 1, 2018),
(7, 'FA101', 1.33, 1, 2018),
(7, 'ME101', 1.56, 1, 2018),
(7, 'BI101', 0.78, 1, 2018),
(7, 'IS101', 2.45, 2, 2019),
(7, 'AC101', 2.89, 2, 2019),
(7, 'MU101', 2.56, 2, 2019),
(7, 'PH101', 1.23, 2, 2019),
(7, 'BI101', 2.34, 2, 2019),
(7, 'MAT101', 2.56, 2, 2019),
(7, 'CE101', 2.78, 2, 2019),
(8, 'CS101', 3.67, 1, 2020),
(8, 'BA101', 2.90, 1, 2020),
(8, 'FA101', 2.33, 1, 2020),
(8, 'ME101', 1.76, 1, 2020),
(8, 'BI101', 0.78, 1, 2020),
(8, 'IS101', 0.45, 2, 2021),
(8, 'AC101', 0.89, 2, 2021),
(8, 'MU101', 1.56, 2, 2021),
(8, 'PH101', 0.23, 2, 2021),
(8, 'BI101', 0.34, 2, 2021),
(8, 'MAT101', 1.56, 2, 2021),
(8, 'CE101', 1.18, 2, 2021),
(9, 'CS101', 1.27, 1, 2022),
(9, 'BA101', 1.50, 1, 2022),
(9, 'FA101', 2.33, 1, 2022),
(9, 'ME101', 2.56, 1, 2022),
(9, 'BI101', 0.78, 1, 2022),
(9, 'IS101', 0.45, 2, 2022),
(9, 'AC101', 0.89, 2, 2022),
(9, 'MU101', 0.56, 2, 2023),
(9, 'PH101', 0.23, 2, 2023),
(9, 'BI101', 1.34, 2, 2023),
(9, 'MAT101', 3.56, 2, 2023),
(9, 'CE101', 1.78, 2, 2023),
(10, 'CS101', 3.45, 1, 2023 ),
(10, 'BA101', 1.67, 1, 2023 ),
(10, 'FA101', 2.89, 1, 2023 ),
(10, 'ME101', 3.12, 1, 2023 ),
(10, 'BI101', 0.78, 1, 2023 ),
(10, 'IS101', 3.45, 2, 2023 ),
(10, 'AC101', 3.89, 2, 2023 ),
(10, 'MU101', 3.56, 2, 2024 ),
(10, 'PH101', 1.23, 2, 2024 ),
(10, 'BI101', 2.34, 2, 2024 ),
(10, 'MAT101', 3.56, 2, 2024 ),
(10, 'CE101', 3.78, 2, 2024 );"""