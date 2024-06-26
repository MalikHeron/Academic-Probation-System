# SQL for creating tables
sql_create_students_table = """CREATE TABLE IF NOT EXISTS student_master (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    email text NOT NULL,
                                    school_code text,
                                    programme_code text,
                                    advisor_id integer,
                                    FOREIGN KEY (school_code) REFERENCES school (school_code),
                                    FOREIGN KEY (programme_code) REFERENCES programme (programme_code),
                                    FOREIGN KEY (advisor_id) REFERENCES staff (staff_id)
                                );"""

sql_create_modules_table = """CREATE TABLE IF NOT EXISTS module_master (
                                    code text PRIMARY KEY,
                                    name text NOT NULL,
                                    credits integer NOT NULL
                                );"""

sql_create_details_table = """CREATE TABLE IF NOT EXISTS module_details (
                                student_id integer NOT NULL,
                                module_code text NOT NULL,
                                grade_points integer NOT NULL,
                                semester integer NOT NULL,
                                year text NOT NULL,
                                FOREIGN KEY (student_id) REFERENCES student_master (id),
                                FOREIGN KEY (module_code) REFERENCES module_master (code)
                            );"""

sql_create_programmes_table = """CREATE TABLE IF NOT EXISTS programme (
                                programme_code text PRIMARY KEY,
                                programme_name text NOT NULL,
                                school_code text,
                                director_id integer,
                                FOREIGN KEY (school_code) REFERENCES school (school_code),
                                FOREIGN KEY (director_id) REFERENCES staff (staff_id)
                            );"""

sql_create_school_table = """CREATE TABLE IF NOT EXISTS school (
                                school_code text PRIMARY KEY,
                                school_name text NOT NULL,
                                faculty_code text,
                                FOREIGN KEY (faculty_code) REFERENCES faculty (faculty_code)
                            );"""

sql_create_faculty_table = """CREATE TABLE IF NOT EXISTS faculty (
                                faculty_code text PRIMARY KEY,
                                faculty_name text NOT NULL,
                                admin_id integer
                            );"""

sql_create_staff_table = """CREATE TABLE IF NOT EXISTS staff (
                                staff_id integer PRIMARY KEY,
                                name text NOT NULL,
                                email text NOT NULL,
                                position text NOT NULL
                            );"""

sql_create_credentials_table = """CREATE TABLE IF NOT EXISTS credentials (
                                user_id integer PRIMARY KEY,
                                username text NOT NULL,
                                password text NOT NULL,
                                FOREIGN KEY (user_id) REFERENCES staff (staff_id)
                            );"""

sql_create_unique_index = """CREATE UNIQUE INDEX idx_module_details_unique ON 
                        module_details(student_id, module_code, semester, year
                        );"""

# Inserting data into faculty
sql_insert_faculty = """INSERT OR IGNORE INTO faculty (faculty_code, faculty_name, admin_id) VALUES
('FENC', 'Faculty of Engineering and Computing', 18),
('FELS', 'Faculty of Education and Liberal Studies', 19),
('COBAM', 'College of Business Administration and Management', 20),
('FOSS', 'Faculty of Science and Sport', 21),
('COHS', 'College of Heath Sciences', 22);"""

# Inserting data into school
sql_insert_schools = """INSERT OR IGNORE INTO school (school_code, school_name, faculty_code) VALUES
('SCIT', 'School of Computing and Information Technology', 'FENC'),
('SOE', 'School of Engineering', 'FENC'),
('SOBA', 'School of Business and Management', 'COBAM'),
('CSN', 'Caribbean School of Nursing', 'COHS'),
('SOMAS', 'School of Mathematics & Statistics', 'FOSS'),
('SONAS', 'School of Natural & Applied Sciences', 'FOSS'),
('CSSS', 'Caribbean School of Sport Sciences', 'FOSS');"""

# Inserting data into programmes
sql_insert_programmes = """INSERT OR IGNORE INTO programme (programme_code, programme_name, school_code, director_id) 
VALUES
('CS', 'Computing',  'SCIT', 1),
('CNS', 'Computer Network and Security', 'SCIT', 2),
('CIS', 'Computer Information Systems', 'SCIT', 3),
('APD', 'Animation Production and Development', 'SCIT', 4),
('CE', 'Civil Engineering',  'SOE', 5),
('ME', 'Mechanical Engineering', 'SOE', 6),
('CHE', 'Chemical Engineering', 'SOE', 7),
('NS', 'Nursing', 'CSN', 8),
('MW', 'Midwifery', 'CSN', 9),
('AS', 'Actuarial Science', 'SOMAS', 10),
('ES', 'Environmental Science', 'SONAS', 11),
('FC', 'Forensic Chemistry', 'SONAS', 12),
('SM', 'Sport Management', 'CSSS', 13),
('ASC', 'Art and Science of Coaching', 'CSSS', 14),
('HRM', 'Human Resource Management', 'SOBA', 15),
('ACC', 'Accounting', 'SOBA', 16);"""

# Inserting data into staff
sql_insert_staff = """INSERT OR IGNORE INTO staff (staff_id, name, email, position) VALUES
(1, 'Alex Doe', 'alexdoe@gmail.com', 'Director'),
(2, 'John Smith', 'johnsmith@gmail.com', 'Director'),
(3, 'Robert Johnson', 'robertjohnson@gmail.com', 'Director'),
(4, 'Emily Davis', 'emilydavis@gmail.com', 'Director'),
(5, 'Daniel Miller', 'danielmiller@gmail.com', 'Director'),
(6, 'Jessica Taylor', 'jessicataylor@gmail.com', 'Director'),
(7, 'Michael Brown', 'michaelbrown@gmail.com', 'Director'),
(8, 'Sarah White', 'sarahwhite@gmail.com', 'Director'),
(9, 'David Anderson', 'davidanderson@gmail.com', 'Director'),
(10, 'Emma Thomas', 'emmathomas@gmail.com', 'Director'),
(11, 'William Jackson', 'williamjackson@hotmail.com', 'Director'),
(12, 'Olivia Martin', 'oliviamartin@yahoo.com', 'Director'),
(13, 'James Thompson', 'jamesthompson@yahoo.com', 'Director'),
(14, 'Sophia Garcia', 'sophiagarcia@yahoo.com', 'Director'),
(15, 'Benjamin Martinez', 'benjaminmartinez@yahoo.com', 'Director'),
(16, 'Isabella Robinson', 'isabellarobinson@yahoo.com', 'Director'),
(17, 'John Bartley', 'johnbartley@gmail.com', 'Director'),
(18, 'Jane White', 'janeswhite@gmail.com', 'Administrator'),
(19, 'Robert McCarthy', 'robertmccarthy@gmail.com', 'Administrator'),
(20, 'Emily Williams', 'emilywilliams@gmail.com', 'Administrator'),
(21, 'Daniel Grant', 'danielgrant@gmail.com', 'Administrator'),
(22, 'Jessica Gilpin', 'jessicgilpin@hotmail.com', 'Administrator'),
(23, 'Michael Horne', 'michaelhorne@hotmail.com', 'Advisor'),
(24, 'Sarah Heron', 'sarahheron@hotmail.com', 'Advisor'),
(25, 'David Thomas', 'davidthomas@hotmail.com', 'Advisor'),
(26, 'Emma Pitterson', 'emmapitterson@hotmail.com', 'Advisor');"""

# Inserting data into credentials
sql_insert_credentials = """INSERT OR IGNORE INTO credentials (user_id, username, password) VALUES
(18, 'JaneWhite5', 'janeswhite'),
(19, 'RobertMc4', 'robertmccarthy'),
(20, 'EmilyWilliams3', 'emilywilliams'),
(21, 'DanielGrant6', 'danielgrant'),
(22, 'JessicaGilpin7', 'jessicgilpin');"""

# Inserting data into student_master
sql_insert_students = """INSERT OR IGNORE INTO student_master (id, name, email, school_code, programme_code, advisor_id)
VALUES
(1, 'John Doe', 'johndoe@gmail.com', 'SCIT', 'CS', 23),
(2, 'Jane Smith', 'janesmith@gmail.com', 'SCIT', 'CNS', 24),
(3, 'Robert Johnson', 'robertjohnson@gmail.com', 'SCIT', 'CIS', 25),
(4, 'Michael Williams', 'michaelwilliams@gmail.com', 'SCIT', 'APD', 26),
(5, 'Sarah Brown', 'sarahbrown@gmail.com', 'SOE', 'CE', 23),
(6, 'David Jones', 'davidjones@gmail.com', 'SOE', 'ME', 24),
(7, 'Emily Davis', 'emilydavis@gmail.com', 'SOE', 'CHE', 25),
(8, 'James Miller', 'jamesmiller@gmail.com', 'CSN', 'NS', 26),
(9, 'Jessica Wilson', 'jessicawilson@gmail.com', 'CSN', 'MW', 23),
(10, 'Thomas Moore', 'thomasmoore@gmail.com', 'SOMAS', 'AS', 24),
(11, 'Alice Johnson', 'alice.johnson@yahoo.com', 'SONAS', 'ES', 25),
(12, 'Bob Smith', 'bob.smith@yahoo.com', 'SONAS', 'FC', 26),
(13, 'Charlie Brown', 'charlie.brown@yahoo.com', 'CSSS', 'SM', 23),
(14, 'David Williams', 'david.williams@yahoo.com', 'CSSS', 'ASC', 24),
(15, 'Eva Davis', 'eva.davis@yahoo.com', 'SOBA', 'HRM', 25),
(16, 'Frank Miller', 'frank.miller@yahoo.com', 'SOBA', 'ACC', 26),
(17, 'Grace Wilson', 'grace.wilson@yahoo.com', 'SOMAS', 'AS', 23),
(18, 'Harry Moore', 'harry.moore@yahoo.com', 'SOBA', 'HRM', 24),
(19, 'Ivy Taylor', 'ivy.taylor@yahoo.com', 'SOMAS', 'AS', 25),
(20, 'Jack Anderson', 'jack.anderson@yahoo.com', 'CSN', 'MW', 26),
(21, 'Kathy Thomas', 'kathy.thomas@hotmail.com', 'SOE', 'ME', 23),
(22, 'Larry Jackson', 'larry.jackson@hotmail.com', 'SOMAS', 'AS', 24),
(23, 'Mia White', 'mia.white@hotmail.com', 'SOE', 'CE', 25),
(24, 'Nick Harris', 'nick.harris@hotmail.com', 'SCIT', 'CS', 26),
(25, 'Olivia Martin', 'olivia.martin@hotmail.com', 'SCIT', 'CS', 23),
(26, 'Peter Thompson', 'peter.thompson@hotmail.com', 'SONAS', 'FC', 24),
(27, 'Quincy Allen', 'quincy.allen@hotmail.com', 'CSN', 'NS', 25),
(28, 'Rita Clark', 'rita.clark@hotmail.com', 'SOE', 'CHE', 26),
(29, 'Sam King', 'sam.king@hotmail.com', 'SCIT', 'CIS', 23),
(30, 'Tina Wright', 'tina.wright@hotmail.com', 'SCIT', 'APD', 24);"""

# Inserting data into module_master
sql_insert_modules = """INSERT OR IGNORE INTO module_master(code, name, credits) VALUES
('CS101', 'Computer Security', 3),
('BA101', 'Business Administration', 3),
('FA101', 'Fine Arts', 4),
('ME101', 'Mechanical Engineering', 4),
('BI101', 'Biology', 3),
('IS101', 'Information Systems', 2),
('AC101', 'Accounting', 1),
('MU101', 'Music', 1),
('CE101', 'Civil Engineering', 2),
('PH101', 'Philosophy', 4),
('MAT101', 'Mathematics', 4),
('COM101', 'Communications', 3),
('PHY101', 'Physics', 4),
('CHE101', 'Chemistry', 1),
('BIO101', 'Biotechnology', 4),
('ECO101', 'Economics', 3),
('HIS101', 'History', 2),
('PHI101', 'Philosophy', 1),
('SOC101', 'Sociology', 4),
('POL101', 'Political Science', 3),
('ENG101', 'English Literature', 2),
('PSY101', 'Psychology', 1),
('ANT101', 'Anthropology', 4),
('AST101', 'Astronomy', 3),
('GEO101', 'Geography Studies', 2), 
('ARC101', 'Architecture Studies', 1), 
('MUS101', 'Music Studies', 4), 
('DRA101', 'Drama Studies', 3), 
('ART101', 'Art History', 2), 
('LAN101', 'Languages and Literature Studies', 1);"""

# Inserting data into module_details
sql_insert_details = """INSERT OR IGNORE INTO module_details(student_id, module_code, grade_points, semester, year) 
VALUES
(1, 'CS101', 3.67, 1, '2021'),
(1, 'BA101', 2.00, 1, '2021'),
(1, 'FA101', 3.33, 1, '2021'),
(1, 'ME101', 2.33, 1, '2021'),
(1, 'BI101', 1.30, 1, '2021'),
(1, 'IS101', 3.00, 1, '2021'),
(1, 'AC101', 4.00, 1, '2021'),
(1, 'MU101', 4.30, 2, '2021'),
(1, 'PH101', 3.67, 2, '2021'),
(1, 'BI101', 3.00, 2, '2021'),
(1, 'MAT101', 3.33, 2, '2021'),
(1, 'CE101', 4.00, 2, '2021'),
(2, 'CS101', 3.27, 1, '2018'),
(2, 'BA101', 2.10, 1, '2018'),
(2, 'FA101', 1.33, 1, '2018'),
(2, 'ME101', 3.33, 1, '2018'),
(2, 'BI101', 3.30, 2, '2018'),
(2, 'IS101', 2.00, 2, '2018'),
(2, 'AC101', 3.00, 2, '2018'),
(3, 'MU101', 4.10, 1, '2017'),
(3, 'PH101', 3.57, 1, '2017'),
(3, 'BI101', 3.50, 1, '2017'),
(3, 'MAT101', 3.13, 1, '2017'),
(3, 'CE101', 2.00, 2, '2017'),
(3, 'CS101', 1.67, 2, '2017'),
(3, 'BA101', 1.90, 2, '2017'),
(4, 'FA101', 3.13, 1, '2021'),
(4, 'ME101', 2.63, 1, '2021'),
(4, 'BI101', 1.90, 1, '2021'),
(4, 'IS101', 3.10, 1, '2021'),
(4, 'AC101', 3.20, 2, '2021'),
(4, 'PH101', 2.67, 2, '2021'),
(4, 'BI101', 2.00, 2, '2021'),
(4, 'MAT101', 2.33, 2, '2021'),
(4, 'CE101', 3.00, 2, '2021'),
(5, 'CS101', 3.21, 1, '2017'),
(5, 'BA101', 1.89, 1, '2017'),
(5, 'FA101', 2.76, 1, '2017'),
(5, 'ME101', 3.56, 1, '2017'),
(5, 'BI101', 0.45, 1, '2017'),
(5, 'IS101', 3.89, 1, '2017'),
(5, 'AC101', 3.67, 1, '2017'),
(5, 'MU101', 3.98, 2, '2017'),
(5, 'PH101', 1.23, 2, '2017'),
(5, 'BI101', 2.34, 2, '2017'),
(5, 'MAT101', 3.56, 2, '2017'),
(5, 'CE101', 3.78, 2, '2017'),
(6, 'CS101', 1.67, 1, '2016'),
(6, 'BA101', 1.90, 1, '2016'),
(6, 'FA101', 1.33, 1, '2016'),
(6, 'ME101', 1.56, 1, '2016'),
(6, 'BI101', 0.78, 1, '2016'),
(6, 'IS101', 2.45, 2, '2016'),
(6, 'AC101', 2.89, 2, '2016'),
(6, 'MU101', 2.56, 2, '2016'),
(6, 'PH101', 1.23, 2, '2016'),
(6, 'BI101', 2.34, 2, '2016'),
(6, 'MAT101', 2.56, 2, '2016'),
(6, 'CE101', 2.78, 2, '2016'),
(7, 'CS101', 1.67, 1, '2018'),
(7, 'BA101', 1.90, 1, '2018'),
(7, 'FA101', 1.33, 1, '2018'),
(7, 'ME101', 1.56, 1, '2018'),
(7, 'BI101', 0.78, 1, '2018'),
(7, 'IS101', 2.45, 2, '2018'),
(7, 'AC101', 2.89, 2, '2018'),
(7, 'MU101', 2.56, 2, '2018'),
(7, 'PH101', 1.23, 2, '2018'),
(7, 'BI101', 2.34, 2, '2018'),
(7, 'MAT101', 2.56, 2, '2018'),
(7, 'CE101', 2.78, 2, '2018'),
(8, 'CS101', 3.67, 1, '2021'),
(8, 'BA101', 2.90, 1, '2021'),
(8, 'FA101', 2.33, 1, '2021'),
(8, 'ME101', 1.76, 1, '2021'),
(8, 'BI101', 0.78, 1, '2021'),
(8, 'IS101', 0.45, 2, '2021'),
(8, 'AC101', 0.89, 2, '2021'),
(8, 'MU101', 1.56, 2, '2021'),
(8, 'PH101', 0.23, 2, '2021'),
(8, 'BI101', 0.34, 2, '2021'),
(8, 'MAT101', 1.56, 2, '2021'),
(8, 'CE101', 1.18, 2, '2021'),
(9, 'CS101', 1.27, 1, '2020'),
(9, 'BA101', 1.50, 1, '2020'),
(9, 'FA101', 2.33, 1, '2020'),
(9, 'ME101', 2.56, 1, '2020'),
(9, 'BI101', 0.78, 1, '2020'),
(9, 'IS101', 0.45, 2, '2020'),
(9, 'AC101', 0.89, 2, '2020'),
(9, 'MU101', 0.56, 2, '2020'),
(9, 'PH101', 0.23, 2, '2020'),
(9, 'BI101', 1.34, 2, '2020'),
(9, 'MAT101', 3.56, 2, '2020'),
(9, 'CE101', 1.78, 2, '2020'),
(10, 'CS101', 3.45, 1, '2020'),
(10, 'BA101', 1.67, 1, '2020'),
(10, 'FA101', 2.89, 1, '2020'),
(10, 'ME101', 3.12, 1, '2020'),
(10, 'BI101', 0.78, 1, '2020'),
(10, 'IS101', 3.45, 2, '2020'),
(10, 'AC101', 3.89, 2, '2020'),
(10, 'MU101', 3.56, 2, '2020'),
(10, 'PH101', 1.23, 2, '2020'),
(10, 'BI101', 2.34, 2, '2020'),
(10, 'MAT101', 3.56, 2, '2020'),
(10, 'CE101', 3.78, 2, '2020'),
(11, 'COM101', 3.15, 1, '2020'),
(11, 'PHY101', 1.47, 1, '2020'),
(11, 'CHE101', 2.29, 1, '2020'),
(11, 'BIO101', 3.62, 1, '2020'),
(11, 'ECO101', 0.48, 1, '2020'),
(11, 'HIS101', 3.65, 2, '2020'),
(11, 'PHI101', 3.19, 2, '2020'),
(11, 'SOC101', 3.06, 2, '2020'),
(11, 'POL101', 1.03, 2, '2020'),
(11, 'ENG101', 2.24, 2, '2020'),
(11, 'PSY101', 3.06, 2, '2020'),
(11, 'ANT101', 3.18, 2, '2020'),
(12, 'COM101', 2.15, 1, '2020'),
(12, 'PHY101', 2.47, 1, '2020'),
(12, 'CHE101', 1.29, 1, '2020'),
(12, 'BIO101', 1.62, 1, '2020'),
(12, 'ECO101', 1.48, 1, '2020'),
(12, 'HIS101', 1.65, 2, '2020'),
(12, 'PHI101', 2.19, 2, '2020'),
(12, 'SOC101', 2.06, 2, '2020'),
(12, 'POL101', 1.03, 2, '2020'),
(12, 'ENG101', 2.24, 2, '2020'),
(12, 'PSY101', 2.06, 2, '2020'),
(12, 'ANT101', 2.18, 2, '2020'),
(13, 'COM101', 2.15, 1, '2019'),
(13, 'PHY101', 1.47, 1, '2019'),
(13, 'CHE101', 2.29, 1, '2019'),
(13, 'BIO101', 1.62, 1, '2019'),
(13, 'ECO101', 0.48, 1, '2019'),
(13, 'HIS101', 2.65, 2, '2019'),
(13, 'PHI101', 2.09, 2, '2019'),
(13, 'SOC101', 2.06, 2, '2019'),
(13, 'POL101', 1.03, 2, '2019'),
(13, 'ENG101', 2.04, 2, '2019'),
(13, 'PSY101', 3.06, 2, '2019'),
(13, 'ANT101', 3.08, 2, '2019'),
(14, 'COM101', 1.15, 1, '2020'),
(14, 'PHY101', 3.47, 1, '2020'),
(14, 'CHE101', 3.29, 1, '2020'),
(14, 'BIO101', 2.62, 1, '2020'),
(14, 'ECO101', 1.48, 1, '2020'),
(15, 'HIS101', 3.65, 1, '2021'),
(15, 'PHI101', 3.19, 1, '2021'),
(15, 'SOC101', 3.06, 1, '2021'),
(15, 'POL101', 1.03, 1, '2021'),
(15, 'ENG101', 2.24, 1, '2021'),
(15, 'PSY101', 3.06, 1, '2021'),
(15, 'ANT101', 3.18, 1, '2021'),
(16, 'HIS101', 3.15, 1, '2021'),
(16, 'PHI101', 3.59, 1, '2021'),
(16, 'SOC101', 3.06, 1, '2021'),
(16, 'POL101', 1.03, 1, '2021'),
(16, 'ENG101', 2.24, 1, '2021'),
(16, 'PSY101', 2.06, 1, '2021'),
(16, 'ANT101', 3.08, 1, '2021'),
(17, 'HIS101', 2.65, 1, '2022'),
(17, 'PHI101', 3.19, 1, '2022'),
(17, 'SOC101', 3.46, 1, '2022'),
(17, 'POL101', 1.53, 1, '2022'),
(17, 'ENG101', 2.24, 1, '2022'),
(17, 'PSY101', 1.06, 1, '2022'),
(17, 'ANT101', 2.18, 1, '2022'),
(18, 'HIS101', 1.65, 1, '2016'),
(18, 'PHI101', 2.19, 1, '2016'),
(18, 'SOC101', 4.06, 1, '2016'),
(18, 'POL101', 2.03, 1, '2016'),
(18, 'ENG101', 1.24, 1, '2016'),
(18, 'PSY101', 2.06, 1, '2016'),
(18, 'ANT101', 1.18, 1, '2016'),
(19, 'CS101', 1.67, 1, '2017'),
(19, 'BA101', 2.90, 1, '2017'),
(19, 'FA101', 1.33, 1, '2017'),
(19, 'ME101', 2.56, 1, '2017'),
(19, 'BI101', 2.78, 1, '2017'),
(20, 'CS101', 3.67, 1, '2018'),
(20, 'BA101', 2.90, 1, '2018'),
(20, 'FA101', 1.33, 1, '2018'),
(20, 'ME101', 1.96, 1, '2018'),
(20, 'BI101', 0.98, 1, '2018'),
(21, 'COM101', 2.15, 1, '2016'),
(21, 'PHY101', 1.27, 1, '2016'),
(21, 'CHE101', 0.29, 1, '2016'),
(21, 'BIO101', 0.62, 1, '2016'),
(21, 'ECO101', 0.98, 1, '2016'),
(21, 'HIS101', 2.35, 2, '2016'),
(21, 'PHI101', 1.09, 2, '2016'),
(21, 'SOC101', 2.06, 2, '2016'),
(21, 'POL101', 1.03, 2, '2016'),
(21, 'ENG101', 3.04, 2, '2016'),
(21, 'PSY101', 3.16, 2, '2016'),
(21, 'ANT101', 2.08, 2, '2016'),
(22, 'AST101', 2.15, 1, '2016'),
(22, 'GEO101', 1.27, 1, '2016'),
(22, 'ARC101', 1.29, 1, '2016'),
(22, 'DRA101', 1.62, 1, '2016'),
(22, 'ART101', 0.98, 1, '2016'),
(22, 'LAN101', 0.98, 1, '2016'),
(23, 'AST101', 2.15, 1, '2016'),
(23, 'GEO101', 1.27, 1, '2016'),
(23, 'ARC101', 1.29, 1, '2016'),
(23, 'DRA101', 1.62, 1, '2016'),
(23, 'ART101', 0.98, 1, '2016'),
(23, 'LAN101', 0.98, 1, '2016'),
(23, 'HIS101', 2.35, 2, '2016'),
(23, 'PHI101', 1.09, 2, '2016'),
(23, 'SOC101', 2.06, 2, '2016'),
(23, 'POL101', 1.03, 2, '2016'),
(23, 'ENG101', 3.04, 2, '2016'),
(24, 'AST101', 1.15, 1, '2016'),
(24, 'GEO101', 2.27, 1, '2016'),
(24, 'ARC101', 3.29, 1, '2016'),
(24, 'DRA101', 2.62, 1, '2016'),
(24, 'ART101', 1.98, 1, '2016'),
(24, 'LAN101', 1.98, 1, '2016'),
(24, 'HIS101', 3.35, 2, '2016'),
(24, 'PHI101', 3.09, 2, '2016'),
(24, 'SOC101', 2.06, 2, '2016'),
(24, 'POL101', 2.03, 2, '2016'),
(24, 'ENG101', 1.04, 2, '2016'),
(25, 'AST101', 1.45, 1, '2017'),
(25, 'GEO101', 2.27, 1, '2017'),
(25, 'ARC101', 3.19, 1, '2017'),
(25, 'DRA101', 2.82, 1, '2017'),
(25, 'SOC101', 2.26, 2, '2017'),
(25, 'POL101', 2.53, 2, '2017'),
(25, 'ENG101', 1.24, 2, '2017'),
(26, 'AST101', 1.15, 1, '2018'),
(26, 'GEO101', 1.27, 1, '2018'),
(26, 'ARC101', 0.29, 1, '2018'),
(26, 'DRA101', 1.62, 1, '2018'),
(26, 'ART101', 2.98, 1, '2018'),
(26, 'PHI101', 3.09, 2, '2018'),
(26, 'SOC101', 4.06, 2, '2018'),
(26, 'POL101', 1.03, 2, '2018'),
(26, 'ENG101', 3.04, 2, '2018'),
(27, 'CS101', 1.27, 1, '2022'),
(27, 'BA101', 1.50, 1, '2022'),
(27, 'FA101', 2.33, 1, '2022'),
(27, 'ME101', 2.56, 1, '2022'),
(27, 'MU101', 0.56, 2, '2022'),
(27, 'PH101', 0.23, 2, '2022'),
(27, 'BI101', 1.34, 2, '2022'),
(28, 'CS101', 1.27, 1, '2021'),
(28, 'BA101', 2.50, 1, '2021'),
(28, 'FA101', 3.33, 1, '2021'),
(28, 'ME101', 0.56, 1, '2021'),
(28, 'MU101', 1.56, 2, '2021'),
(28, 'PH101', 1.23, 2, '2021'),
(28, 'BI101', 2.34, 2, '2021'),
(29, 'CS101', 1.27, 1, '2022'),
(29, 'BA101', 0.50, 1, '2022'),
(29, 'FA101', 0.33, 1, '2022'),
(29, 'ME101', 3.56, 1, '2022'),
(29, 'MU101', 3.56, 2, '2022'),
(29, 'PH101', 3.23, 2, '2022'),
(29, 'BI101', 2.34, 2, '2022'),
(30, 'CS101', 3.27, 1, '2021'),
(30, 'BA101', 3.50, 1, '2021'),
(30, 'FA101', 0.33, 1, '2021'),
(30, 'ME101', 0.56, 1, '2021'),
(30, 'MU101', 1.56, 2, '2021'),
(30, 'PH101', 1.23, 2, '2021'),
(30, 'BI101', 2.34, 2, '2021');"""
