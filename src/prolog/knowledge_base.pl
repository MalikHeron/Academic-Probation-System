% The default GPA
:- dynamic(default_gpa/1).
default_gpa(2.2).

% Facts for student_master
student_master(1, 'John Doe', 'johndoe@gmail.com', 'School of Computing', 'Computer Science').
student_master(2, 'Jane Smith', 'janesmith@gmail.com', 'School of Business', 'Business Administration').
student_master(3, 'Robert Johnson', 'robertjohnson@gmail.com', 'School of Arts', 'Fine Arts').
student_master(4, 'Michael Williams', 'michaelwilliams@gmail.com', 'School of Engineering', 'Mechanical Engineering').
student_master(5, 'Sarah Brown', 'sarahbrown@gmail.com', 'School of Science', 'Biology').
student_master(6, 'David Jones', 'davidjones@gmail.com', 'School of Computing', 'Information Systems').
student_master(7, 'Emily Davis', 'emilydavis@gmail.com', 'School of Business', 'Accounting').
student_master(8, 'James Miller', 'jamesmiller@gmail.com', 'School of Arts', 'Music').
student_master(9, 'Jessica Wilson', 'jessicawilson@gmail.com', 'School of Engineering', 'Civil Engineering').
student_master(10, 'Thomas Moore', 'thomasmoore@gmail.com', 'School of Science', 'Physics').

% Facts for module_master
module_master('CS101', 'Artificial Intelligence', 4).
module_master('BA101', 'Introduction to Business Administration', 4).
module_master('FA101', 'Introduction to Fine Arts', 3).
module_master('ME101', 'Introduction to Mechanical Engineering', 4).
module_master('BI101', 'Introduction to Biology', 4).
module_master('IS101', 'Introduction to Information Systems', 4).
module_master('AC101', 'Introduction to Accounting', 4).
module_master('MU101', 'Introduction to Music', 3).
module_master('CE101', 'Introduction to Civil Engineering', 3).
module_master('PH101', 'Introduction to Physics', 4).

% Facts for module_details
module_details(1, 'CS101', 4, 1, 2023).
module_details(2, 'BA101', 3.5, 1, 2023).
module_details(3, 'FA101', 4.0, 1, 2023).
module_details(4, 'ME101', 3.7, 1, 2023).
module_details(5, 'BI101', 3.8, 1, 2023).
module_details(6, 'IS101', 3.9, 1, 2023).
module_details(7, 'AC101', 4.0, 1, 2023).
module_details(8, 'MU101', 3.6, 1, 2023).
module_details(9, 'CE101', 3.5, 1, 2023).
module_details(10, 'PH101',4.0 ,1 ,2023).

% A predicate that calculates the GPA for a given student ID and semester
gpa(StudentID, Semester, GPA) :-
    findall(GradePoint, grade_points(Module, Semester, GradePoint), GradePoints),
    sum(GradePoints, TotalGradePoints),
    length(GradePoints, TotalCredits),
    GPA is TotalGradePoints / TotalCredits.

% A predicate that calculates the cumulative GPA for a given student ID
cumulative_gpa(StudentID, CumulativeGPA) :-
    findall(GPA, gpa(StudentID, Semester, GPA), GPAs),
    sum(GPAs, TotalGPAs),
    length(GPAs, TotalSemesters),
    CumulativeGPA is TotalGPAs / TotalSemesters.

% A predicate that updates the default GPA
update_default_gpa(NewGPA) :-
    (   retract(default_gpa(OldGPA)) ->
        true
    ;   OldGPA = 'No old GPA'
    ),
    assert(default_gpa(NewGPA)),
    write('Old GPA: '), write(OldGPA), nl,
    write('New GPA: '), write(NewGPA), nl.

% A predicate that calculates the sum of a list of numbers
sum(List, Sum) :-
    sum(List, 0, Sum).

sum([], Sum, Sum).
sum([Head|Tail], TempSum, Sum) :-
    NewTempSum is TempSum + Head,
    sum(Tail, NewTempSum, Sum).