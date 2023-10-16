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

'''
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
sql_insert_modules = """INSERT OR IGNORE INTO module_master(code, name, credits) VALUES
('CS101', 'Artificial Intelligence', 4),
('BA101', 'Introduction to Business Administration', 4),
('FA101', 'Introduction to Fine Arts', 3),
('ME101', 'Introduction to Mechanical Engineering', 5),
('BI101', 'Introduction to Biology', 4),
('IS101', 'Introduction to Information Systems', 4),
('AC101', 'Introduction to Accounting', 4),
('MU101', 'Introduction to Music', 3),
('CE101', 'Introduction to Civil Engineering', 5),
('PH101', 'Introduction to Physics', 4);"""

# Inserting data into module_details
sql_insert_details = """INSERT OR IGNORE INTO module_details(student_id, module_code, grade_points, semester, year) 
VALUES
(1, 'CS101', 4, 1, 2023),
(2, 'BA101', 3.5, 1, 2023),
(3, 'FA101', 4.0, 1, 2023),
(4, 'ME101', 3.7, 1, 2023),
(5, 'BI101', 3.8, 1, 2023),
(6, 'IS101', 3.9, 1, 2023),
(7, 'AC101', 4.0, 1, 2023),
(8, 'MU101', 3.6, 1, 2023),
(9, 'CE101', 3.5, 1, 2023),
(10, 'PH101',4.0 ,1 ,2023);"""
'''

# Inserting data into student_master
sql_insert_students = """INSERT OR IGNORE INTO student_master(id, name, email, school, programme) VALUES
(?,?,?,?,?)"""

# Inserting data into module_master
sql_insert_modules = """INSERT OR IGNORE INTO module_master(code, credits) VALUES
(?,?);"""

# Inserting data into module_details
sql_insert_details = """INSERT OR IGNORE INTO module_details(student_id, module_code, grade_points, semester, 
year) VALUES(?,?,?,?,?)"""
