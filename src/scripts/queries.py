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
(10, 'Thomas Moore', 'thomasmoore@gmail.com', 'School of Science', 'Physics'),
(11, 'Alice Johnson', 'alice.johnson@yahoo.com', 'School of Computing', 'Computer Science'),
(12, 'Bob Smith', 'bob.smith@yahoo.com', 'School of Physics', 'Physics'),
(13, 'Charlie Brown', 'charlie.brown@yahoo.com', 'School of Mathematics', 'Mathematics'),
(14, 'David Williams', 'david.williams@yahoo.com', 'School of Chemistry', 'Chemistry'),
(15, 'Eva Davis', 'eva.davis@yahoo.com', 'School of Biology', 'Biology'),
(16, 'Frank Miller', 'frank.miller@yahoo.com', 'School of Economics', 'Economics'),
(17, 'Grace Wilson', 'grace.wilson@yahoo.com', 'School of History', 'History'),
(18, 'Harry Moore', 'harry.moore@yahoo.com', 'School of Philosophy', 'Philosophy'),
(19, 'Ivy Taylor', 'ivy.taylor@yahoo.com', 'School of Sociology', 'Sociology'),
(20, 'Jack Anderson', 'jack.anderson@yahoo.com', 'School of Political Science', 'Political Science'),
(21, 'Kathy Thomas', 'kathy.thomas@hotmail.com', 'School of English Literature', 'English Literature'),
(22, 'Larry Jackson', 'larry.jackson@hotmail.com', 'School of Psychology', 'Psychology'),
(23, 'Mia White', 'mia.white@hotmail.com', 'School of Anthropology', 'Anthropology'),
(24, 'Nick Harris', 'nick.harris@hotmail.com', 'School of Astronomy', 'Astronomy'),
(25, 'Olivia Martin', 'olivia.martin@hotmail.com', 'School of Geography', 'Geography'),
(26, 'Peter Thompson', 'peter.thompson@hotmail.com', 'School of Archaeology', 'Archaeology'),
(27, 'Quincy Allen', 'quincy.allen@hotmail.com', 'School of Music', 'Music'),
(28, 'Rita Clark', 'rita.clark@hotmail.com', 'School of Drama', 'Drama'),
(29, 'Sam King', 'sam.king@hotmail.com', 'School of Art History', 'Art History'),
(30, 'Tina Wright', 'tina.wright@hotmail.com', 'School of Modern Languages', 'Modern Languages');"""

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
('MAT101', 4),
('COM101', 3),
('PHY101', 4),
('CHE101', 1),
('BIO101', 4),
('ECO101', 3),
('HIS101', 2),
('PHI101', 1),
('SOC101', 4),
('POL101', 3),
('ENG101', 2),
('PSY101', 1),
('ANT101', 4),
('AST101', 3),
('GEO101', 2),
('ARC101', 1),
('MUS101', 4),
('DRA101', 3),
('ART101', 2),
('LAN101', 1);"""

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
(1, 'MU101', 4.30, 2, 2021),
(1, 'PH101', 3.67, 2, 2021),
(1, 'BI101', 3.00, 2, 2021),
(1, 'MAT101', 3.33, 2, 2021),
(1, 'CE101', 4.00, 2, 2021),
(2, 'CS101', 3.27, 1, 2018),
(2, 'BA101', 2.10, 1, 2018),
(2, 'FA101', 1.33, 1, 2018),
(2, 'ME101', 3.33, 1, 2018),
(2, 'BI101', 3.30, 2, 2018),
(2, 'IS101', 2.00, 2, 2018),
(2, 'AC101', 3.00, 2, 2018),
(3, 'MU101', 4.10, 1, 2017),
(3, 'PH101', 3.57, 1, 2017),
(3, 'BI101', 3.50, 1, 2017),
(3, 'MAT101', 3.13, 1, 2017),
(3, 'CE101', 2.00, 2, 2017),
(3, 'CS101', 1.67, 2, 2017),
(3, 'BA101', 1.90, 2, 2017),
(4, 'FA101', 3.13, 1, 2021),
(4, 'ME101', 2.63, 1, 2021),
(4, 'BI101', 1.90, 1, 2021),
(4, 'IS101', 3.10, 1, 2021),
(4, 'AC101', 3.20, 2, 2021),
(4, 'PH101', 2.67, 2, 2021),
(4, 'BI101', 2.00, 2, 2021),
(4, 'MAT101', 2.33, 2, 2021),
(4, 'CE101', 3.00, 2, 2021),
(5, 'CS101', 3.21, 1, 2017),
(5, 'BA101', 1.89, 1, 2017),
(5, 'FA101', 2.76, 1, 2017),
(5, 'ME101', 3.56, 1, 2017),
(5, 'BI101', 0.45, 1, 2017),
(5, 'IS101', 3.89, 1, 2017),
(5, 'AC101', 3.67, 1, 2017),
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
(6, 'IS101', 2.45, 2, 2016),
(6, 'AC101', 2.89, 2, 2016),
(6, 'MU101', 2.56, 2, 2016),
(6, 'PH101', 1.23, 2, 2016),
(6, 'BI101', 2.34, 2, 2016),
(6, 'MAT101', 2.56, 2, 2016),
(6, 'CE101', 2.78, 2, 2016),
(7, 'CS101', 1.67, 1, 2018),
(7, 'BA101', 1.90, 1, 2018),
(7, 'FA101', 1.33, 1, 2018),
(7, 'ME101', 1.56, 1, 2018),
(7, 'BI101', 0.78, 1, 2018),
(7, 'IS101', 2.45, 2, 2018),
(7, 'AC101', 2.89, 2, 2018),
(7, 'MU101', 2.56, 2, 2018),
(7, 'PH101', 1.23, 2, 2018),
(7, 'BI101', 2.34, 2, 2018),
(7, 'MAT101', 2.56, 2, 2018),
(7, 'CE101', 2.78, 2, 2018),
(8, 'CS101', 3.67, 1, 2021),
(8, 'BA101', 2.90, 1, 2021),
(8, 'FA101', 2.33, 1, 2021),
(8, 'ME101', 1.76, 1, 2021),
(8, 'BI101', 0.78, 1, 2021),
(8, 'IS101', 0.45, 2, 2021),
(8, 'AC101', 0.89, 2, 2021),
(8, 'MU101', 1.56, 2, 2021),
(8, 'PH101', 0.23, 2, 2021),
(8, 'BI101', 0.34, 2, 2021),
(8, 'MAT101', 1.56, 2, 2021),
(8, 'CE101', 1.18, 2, 2021),
(9, 'CS101', 1.27, 1, 2020),
(9, 'BA101', 1.50, 1, 2020),
(9, 'FA101', 2.33, 1, 2020),
(9, 'ME101', 2.56, 1, 2020),
(9, 'BI101', 0.78, 1, 2020),
(9, 'IS101', 0.45, 2, 2020),
(9, 'AC101', 0.89, 2, 2020),
(9, 'MU101', 0.56, 2, 2020),
(9, 'PH101', 0.23, 2, 2020),
(9, 'BI101', 1.34, 2, 2020),
(9, 'MAT101', 3.56, 2, 2020),
(9, 'CE101', 1.78, 2, 2020),
(10, 'CS101', 3.45, 1, 2020),
(10, 'BA101', 1.67, 1, 2020),
(10, 'FA101', 2.89, 1, 2020),
(10, 'ME101', 3.12, 1, 2020),
(10, 'BI101', 0.78, 1, 2020),
(10, 'IS101', 3.45, 2, 2020),
(10, 'AC101', 3.89, 2, 2020),
(10, 'MU101', 3.56, 2, 2020),
(10, 'PH101', 1.23, 2, 2020),
(10, 'BI101', 2.34, 2, 2020),
(10, 'MAT101', 3.56, 2, 2020),
(10, 'CE101', 3.78, 2, 2020),
(11, 'COM101', 3.15, 1, 2020),
(11, 'PHY101', 1.47, 1, 2020),
(11, 'CHE101', 2.29, 1, 2020),
(11, 'BIO101', 3.62, 1, 2020),
(11, 'ECO101', 0.48, 1, 2020),
(11, 'HIS101', 3.65, 2, 2020),
(11, 'PHI101', 3.19, 2, 2020),
(11, 'SOC101', 3.06, 2, 2020),
(11, 'POL101', 1.03, 2, 2020),
(11, 'ENG101', 2.24, 2, 2020),
(11, 'PSY101', 3.06, 2, 2020),
(11, 'ANT101', 3.18, 2, 2020),
(12, 'COM101', 2.15, 1, 2020),
(12, 'PHY101', 2.47, 1, 2020),
(12, 'CHE101', 1.29, 1, 2020),
(12, 'BIO101', 1.62, 1, 2020),
(12, 'ECO101', 1.48, 1, 2020),
(12, 'HIS101', 1.65, 2, 2020),
(12, 'PHI101', 2.19, 2, 2020),
(12, 'SOC101', 2.06, 2, 2020),
(12, 'POL101', 1.03, 2, 2020),
(12, 'ENG101', 2.24, 2, 2020),
(12, 'PSY101', 2.06, 2, 2020),
(12, 'ANT101', 2.18, 2, 2020),
(13, 'COM101', 2.15, 1, 2019),
(13, 'PHY101', 1.47, 1, 2019),
(13, 'CHE101', 2.29, 1, 2019),
(13, 'BIO101', 1.62, 1, 2019),
(13, 'ECO101', 0.48, 1, 2019),
(13, 'HIS101', 2.65, 2, 2019),
(13, 'PHI101', 2.09, 2, 2019),
(13, 'SOC101', 2.06, 2, 2019),
(13, 'POL101', 1.03, 2, 2019),
(13, 'ENG101', 2.04, 2, 2019),
(13, 'PSY101', 3.06, 2, 2019),
(13, 'ANT101', 3.08, 2, 2019),
(14, 'COM101', 1.15, 1, 2020),
(14, 'PHY101', 3.47, 1, 2020),
(14, 'CHE101', 3.29, 1, 2020),
(14, 'BIO101', 2.62, 1, 2020),
(14, 'ECO101', 1.48, 1, 2020),
(15, 'HIS101', 3.65, 1, 2021),
(15, 'PHI101', 3.19, 1, 2021),
(15, 'SOC101', 3.06, 1, 2021),
(15, 'POL101', 1.03, 1, 2021),
(15, 'ENG101', 2.24, 1, 2021),
(15, 'PSY101', 3.06, 1, 2021),
(15, 'ANT101', 3.18, 1, 2021),
(16, 'HIS101', 3.15, 1, 2021),
(16, 'PHI101', 3.59, 1, 2021),
(16, 'SOC101', 3.06, 1, 2021),
(16, 'POL101', 1.03, 1, 2021),
(16, 'ENG101', 2.24, 1, 2021),
(16, 'PSY101', 2.06, 1, 2021),
(16, 'ANT101', 3.08, 1, 2021),
(17, 'HIS101', 2.65, 1, 2022),
(17, 'PHI101', 3.19, 1, 2022),
(17, 'SOC101', 3.46, 1, 2022),
(17, 'POL101', 1.53, 1, 2022),
(17, 'ENG101', 2.24, 1, 2022),
(17, 'PSY101', 1.06, 1, 2022),
(17, 'ANT101', 2.18, 1, 2022),
(18, 'HIS101', 1.65, 1, 2016),
(18, 'PHI101', 2.19, 1, 2016),
(18, 'SOC101', 4.06, 1, 2016),
(18, 'POL101', 2.03, 1, 2016),
(18, 'ENG101', 1.24, 1, 2016),
(18, 'PSY101', 2.06, 1, 2016),
(18, 'ANT101', 1.18, 1, 2016),
(19, 'CS101', 1.67, 1, 2017),
(19, 'BA101', 2.90, 1, 2017),
(19, 'FA101', 1.33, 1, 2017),
(19, 'ME101', 2.56, 1, 2017),
(19, 'BI101', 2.78, 1, 2017),
(20, 'CS101', 3.67, 1, 2018),
(20, 'BA101', 2.90, 1, 2018),
(20, 'FA101', 1.33, 1, 2018),
(20, 'ME101', 1.96, 1, 2018),
(20, 'BI101', 0.98, 1, 2018),
(21, 'COM101', 2.15, 1, 2016),
(21, 'PHY101', 1.27, 1, 2016),
(21, 'CHE101', 0.29, 1, 2016),
(21, 'BIO101', 0.62, 1, 2016),
(21, 'ECO101', 0.98, 1, 2016),
(21, 'HIS101', 2.35, 2, 2016),
(21, 'PHI101', 1.09, 2, 2016),
(21, 'SOC101', 2.06, 2, 2016),
(21, 'POL101', 1.03, 2, 2016),
(21, 'ENG101', 3.04, 2, 2016),
(21, 'PSY101', 3.16, 2, 2016),
(21, 'ANT101', 2.08, 2, 2016),
(22, 'AST101', 2.15, 1, 2016),
(22, 'GEO101', 1.27, 1, 2016),
(22, 'ARC101', 1.29, 1, 2016),
(22, 'DRA101', 1.62, 1, 2016),
(22, 'ART101', 0.98, 1, 2016),
(22, 'LAN101', 0.98, 1, 2016),
(23, 'AST101', 2.15, 1, 2016),
(23, 'GEO101', 1.27, 1, 2016),
(23, 'ARC101', 1.29, 1, 2016),
(23, 'DRA101', 1.62, 1, 2016),
(23, 'ART101', 0.98, 1, 2016),
(23, 'LAN101', 0.98, 1, 2016),
(23, 'HIS101', 2.35, 2, 2016),
(23, 'PHI101', 1.09, 2, 2016),
(23, 'SOC101', 2.06, 2, 2016),
(23, 'POL101', 1.03, 2, 2016),
(23, 'ENG101', 3.04, 2, 2016),
(24, 'AST101', 1.15, 1, 2016),
(24, 'GEO101', 2.27, 1, 2016),
(24, 'ARC101', 3.29, 1, 2016),
(24, 'DRA101', 2.62, 1, 2016),
(24, 'ART101', 1.98, 1, 2016),
(24, 'LAN101', 1.98, 1, 2016),
(24, 'HIS101', 3.35, 2, 2016),
(24, 'PHI101', 3.09, 2, 2016),
(24, 'SOC101', 2.06, 2, 2016),
(24, 'POL101', 2.03, 2, 2016),
(24, 'ENG101', 1.04, 2, 2016),
(25, 'AST101', 1.45, 1, 2017),
(25, 'GEO101', 2.27, 1, 2017),
(25, 'ARC101', 3.19, 1, 2017),
(25, 'DRA101', 2.82, 1, 2017),
(25, 'SOC101', 2.26, 2, 2017),
(25, 'POL101', 2.53, 2, 2017),
(25, 'ENG101', 1.24, 2, 2017),
(26, 'AST101', 1.15, 1, 2018),
(26, 'GEO101', 1.27, 1, 2018),
(26, 'ARC101', 0.29, 1, 2018),
(26, 'DRA101', 1.62, 1, 2018),
(26, 'ART101', 2.98, 1, 2018),
(26, 'PHI101', 3.09, 2, 2018),
(26, 'SOC101', 4.06, 2, 2018),
(26, 'POL101', 1.03, 2, 2018),
(26, 'ENG101', 3.04, 2, 2018),
(27, 'CS101', 1.27, 1, 2022),
(27, 'BA101', 1.50, 1, 2022),
(27, 'FA101', 2.33, 1, 2022),
(27, 'ME101', 2.56, 1, 2022),
(27, 'MU101', 0.56, 2, 2022),
(27, 'PH101', 0.23, 2, 2022),
(27, 'BI101', 1.34, 2, 2022),
(28, 'CS101', 1.27, 1, 2021),
(28, 'BA101', 2.50, 1, 2021),
(28, 'FA101', 3.33, 1, 2021),
(28, 'ME101', 0.56, 1, 2021),
(28, 'MU101', 1.56, 2, 2021),
(28, 'PH101', 1.23, 2, 2021),
(28, 'BI101', 2.34, 2, 2021),
(29, 'CS101', 1.27, 1, 2022),
(29, 'BA101', 0.50, 1, 2022),
(29, 'FA101', 0.33, 1, 2022),
(29, 'ME101', 3.56, 1, 2022),
(29, 'MU101', 3.56, 2, 2022),
(29, 'PH101', 3.23, 2, 2022),
(29, 'BI101', 2.34, 2, 2022),
(30, 'CS101', 3.27, 1, 2021),
(30, 'BA101', 3.50, 1, 2021),
(30, 'FA101', 0.33, 1, 2021),
(30, 'ME101', 0.56, 1, 2021),
(30, 'MU101', 1.56, 2, 2021),
(30, 'PH101', 1.23, 2, 2021),
(30, 'BI101', 2.34, 2, 2021);"""
