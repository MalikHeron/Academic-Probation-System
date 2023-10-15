% The default GPA
:- dynamic(default_gpa/1).
default_gpa(2.2).

% The grade points and credits of each module
grade_points('CMP4011', 4).

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