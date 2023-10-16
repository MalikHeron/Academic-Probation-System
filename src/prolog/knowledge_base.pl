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
module_master('CS101', 'Artificial Intelligence', 3).
module_master('BA101', 'Introduction to Business Administration', 3).
module_master('FA101', 'Introduction to Fine Arts', 4).
module_master('ME101', 'Introduction to Mechanical Engineering', 4).
module_master('BI101', 'Introduction to Biology', 3).
module_master('IS101', 'Introduction to Information Systems', 2).
module_master('AC101', 'Introduction to Accounting', 1).
module_master('MU101', 'Introduction to Music', 1).
module_master('CE101', 'Introduction to Civil Engineering', 2).
module_master('PH101', 'Introduction to Physics', 4).
module_master('MAT101', 'Introduction to Statistics', 4).

% Facts for module_details
module_details(1, 'CS101', 3.67, 1, 2021).
module_details(1, 'BA101', 2.00, 1, 2021).
module_details(1, 'FA101', 3.33, 1, 2021).
module_details(1, 'ME101', 2.33, 1, 2021).
module_details(1, 'BI101', 1.30, 1, 2021).
module_details(1, 'IS101', 3.00, 1, 2021).
module_details(1, 'AC101', 4.00, 1, 2021).
module_details(1, 'MU101', 4.30, 2, 2022).
module_details(1, 'PH101', 3.67, 2, 2022).
module_details(1, 'BI101', 3.00, 2, 2022).
module_details(1, 'MAT101', 3.33, 2, 2022).
module_details(1, 'CE101', 4.00, 2, 2022).

% A predicate that calculates the GPA for a given student ID and semester
gpa(StudentID, Name, Semester, GPA) :-
    student_master(StudentID, Name, _, _, _),
    findall(
        GradePointsEarned,
        (   module_details(StudentID, Module, GradePoint, Semester, _),
            module_master(Module, _, Credits),
            GradePointsEarned is Credits * GradePoint
        ),
        GradePointsEarnedList
    ),
    sum_list(GradePointsEarnedList, TotalGradePoints),
    write('Total Grade Points: '), write(TotalGradePoints), nl,
    findall(
        Credits,
        (   module_details(StudentID, Module, _, Semester, _),
            module_master(Module, _, Credits)
        ),
        CreditsList
    ),
    sum_list(CreditsList, TotalCredits),
    write('Total Credits: '), write(TotalCredits), nl,
    TotalCredits \= 0,
    GPA is round((TotalGradePoints / TotalCredits) * 100) / 100,
    write('GPA is '), write(GPA), nl, nl.

% A predicate that calculates the Cumulative GPA for a given student ID
cumulative_gpa(StudentID, Name, GPA1, GPA2, CumulativeGPA) :-
    (   gpa(StudentID, Name, 1, GPA1), gpa(StudentID, Name, 2, GPA2) ->
        findall(
            TotalGradePoints,
            (   gpa(StudentID, Name, Semester, _),
                findall(
                    GradePointsEarned,
                    (   module_details(StudentID, Module, GradePoint, Semester, _),
                        module_master(Module, _, Credits),
                        GradePointsEarned is Credits * GradePoint
                    ),
                    GradePointsEarnedList
                ),
                sum_list(GradePointsEarnedList, TotalGradePoints)
            ),
            TotalGradePointsList
        ),
        sum_list(TotalGradePointsList, AllTotalGradePoints),
        findall(
            TotalCredits,
            (   gpa(StudentID, Name, Semester, _),
                findall(
                    Credits,
                    (   module_details(StudentID, Module, _, Semester, _),
                        module_master(Module, _, Credits)
                    ),
                    CreditsList
                ),
                sum_list(CreditsList, TotalCredits)
            ),
            TotalCreditsList
        ),
        sum_list(TotalCreditsList, AllTotalCredits),
        CumulativeGPA is AllTotalGradePoints / AllTotalCredits
    ;   gpa(StudentID, Name, 1, GPA1) ->
        CumulativeGPA is GPA1
    ).

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
sum_list([], 0).
sum_list([H|T], Sum) :-
   sum_list(T, Rest),
   Sum is H + Rest.
