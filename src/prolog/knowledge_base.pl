% dynamic predicates
:- dynamic(default_gpa/1).
:- dynamic(student/5).
:- dynamic(module/2).
:- dynamic(module_details/5).

% The default GPA
default_gpa(2.2).

% Facts for student
% student(Id, Name, Email, School, Programme).

% Facts for module
% module(Module, Credits).

% Facts for module_details
% module_details(Id, Module, GradePoint, Semester, Year).

% A predicate that calculates the GPA for a given student ID and semester
gpa(StudentID, Name, Semester, GPA) :-
    student(StudentID, Name, _, _, _),
    findall(
        GradePointsEarned,
        (   module_details(StudentID, Module, GradePoint, Semester, _),
            module(Module, Credits),
            GradePointsEarned is Credits * GradePoint
        ),
        GradePointsEarnedList
    ),
    sum_list(GradePointsEarnedList, TotalGradePoints),
    findall(
        Credits,
        (   module_details(StudentID, Module, _, Semester, _),
            module(Module, Credits)
        ),
        CreditsList
    ),
    sum_list(CreditsList, TotalCredits),
    TotalCredits \= 0,
    GPA is round((TotalGradePoints / TotalCredits) * 100) / 100.

% A predicate that calculates the Cumulative GPA for a given student ID
cumulative_gpa(StudentID, Name, GPA1, GPA2, CumulativeGPA) :-
    (   gpa(StudentID, Name, 1, GPA1), gpa(StudentID, Name, 2, GPA2) ->
        findall(
            TotalGradePoints,
            (   gpa(StudentID, Name, Semester, _),
                findall(
                    GradePointsEarned,
                    (   module_details(StudentID, Module, GradePoint, Semester, _),
                        module(Module, Credits),
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
                        module(Module, Credits)
                    ),
                    CreditsList
                ),
                sum_list(CreditsList, TotalCredits)
            ),
            TotalCreditsList
        ),
        sum_list(TotalCreditsList, AllTotalCredits),
        CumulativeGPA is round((AllTotalGradePoints / AllTotalCredits) * 100) / 100
    ;   gpa(StudentID, Name, 1, GPA1) ->
        CumulativeGPA is round(GPA1 * 100) / 100
    ).

% A predicate that calculates the Cumulative GPA for all students and stores the results in a list
cumulative_gpa_all_students(Results) :-
    findall(
        [StudentID, Name, GPA1, GPA2, CumulativeGPA],
        (   student(StudentID, Name, _, _, _),
            gpa(StudentID, Name, 1, GPA1),
            gpa(StudentID, Name, 2, GPA2),
            (   cumulative_gpa(StudentID, Name, GPA1, GPA2, CumulativeGPA) ->
                format('Student: ~w, Cumulative GPA: ~2f~n', [Name, CumulativeGPA])
            ;   CumulativeGPA = 'No GPA calculated',
                format('Student: ~w, No GPA calculated~n', [Name])
            )
        ),
        Results
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
