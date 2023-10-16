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

# Inserting data into 
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
(2, 'CE101', 4.00, 1, 2018),
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
(4, 'FA101', 3.13, 2, 2021),
(4, 'ME101', 2.63, 2, 2021),
(4, 'BI101', 1.90, 2, 2021),
(4, 'IS101', 3.10, 2, 2021),
(4, 'AC101', 4.20, 2, 2021),
(4, 'PH101', 3.67, 1, 2023),
(4, 'BI101', 3.00, 1, 2023),
(4, 'MAT101', 3.33, 1, 2023),
(4, 'CE101', 4.00, 1, 2023);"""
