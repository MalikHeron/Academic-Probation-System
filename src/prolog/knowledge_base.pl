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

% Calculate grade points earned for a module
grade_points_earned(StudentID, Semester, Year, GradePointsEarned) :-
    % Retrieve the details of each module taken by the student in the given semester
    module_details(StudentID, Module, GradePoint, Semester, Year),
    % Retrieve the credits for each module
    module(Module, Credits),
    % Calculate the grade points earned for each module (credits * grade point)
    GradePointsEarned is Credits * GradePoint.

% Retrieve credits for a module
module_credits(StudentID, Semester, Year, Credits) :-
    % Retrieve the details of each module taken by the student in the given semester
    module_details(StudentID, Module, _, Semester, Year),
    % Retrieve the credits for each module
    module(Module, Credits).

% Calculates the GPA for a given student ID and semester
gpa(StudentID, Name, Semester, Year, GPA) :-
    % Retrieve the student's details
    student(StudentID, Name, _, _, _),
    % Find all grade points earned by the student in the given semester
    findall(
        GradePointsEarned,
        grade_points_earned(StudentID, Semester, Year, GradePointsEarned),
        GradePointsEarnedList
    ),
    % Calculate the total grade points earned by summing up the list
    sum_list(GradePointsEarnedList, TotalGradePoints),
    % Find all credits for modules taken by the student in the given semester
    findall(Credits, module_credits(StudentID, Semester, Year, Credits), CreditsList),
    % Calculate the total credits by summing up the list
    sum_list(CreditsList, TotalCredits),
    % Ensure that total credits is not zero to avoid division by zero error
    TotalCredits \= 0,
    % Calculate GPA (total grade points / total credits), rounded to 2 decimal places
    GPA is round((TotalGradePoints / TotalCredits) * 100) / 100.

% Calculates the Cumulative GPA for a given student ID
cumulative_gpa(StudentID, Name, GPA1, GPA2, Year, CumulativeGPA) :-
    % If the student has GPAs for both semesters
    (   gpa(StudentID, Name, 1, Year, GPA1), gpa(StudentID, Name, 2, Year, GPA2) ->
        % Find all total grade points earned by the student in all semesters
        findall(
            TotalGradePoints,
            (   % Retrieve the GPA for each semester
                gpa(StudentID, Name, Semester, Year, _),
                % Find all grade points earned by the student in each semester
                findall(
                    GradePointsEarned,
                    grade_points_earned(StudentID, Semester, Year, GradePointsEarned),
                    GradePointsEarnedList
                ),
                % Calculate the total grade points earned by summing up the list
                sum_list(GradePointsEarnedList, TotalGradePoints)
            ),
            TotalGradePointsList
        ),
        % Calculate the total of all grade points by summing up the list
        sum_list(TotalGradePointsList, AllTotalGradePoints),
        % Find all total credits for modules taken by the student in all semesters
        findall(
            TotalCredits,
            (   % Retrieve the GPA for each semester
                gpa(StudentID, Name, Semester, Year, _),
                % Find all credits for modules taken by the student in each semester
                findall(Credits, module_credits(StudentID, Semester, Year, Credits), CreditsList),
                % Calculate the total credits by summing up the list
                sum_list(CreditsList, TotalCredits)
            ),
            TotalCreditsList
        ),
        % Calculate the total of all credits by summing up the list
        sum_list(TotalCreditsList, AllTotalCredits),
        % Calculate Cumulative GPA (total of all grade points / total of all credits), rounded to 2 decimal places
        CumulativeGPA is round((AllTotalGradePoints / AllTotalCredits) * 100) / 100
    ;   % If the student only has a GPA for semester 1
        gpa(StudentID, Name, 1, Year, GPA1) ->
        % The Cumulative GPA is just GPA1 rounded to 2 decimal places
        CumulativeGPA is round(GPA1 * 100) / 100
    ).

% Calculates the Cumulative GPA for all students and stores the results in a list
cumulative_gpa_all_students(Year, Results) :-
    % find all solutions to a goal and returns them in a list
    findall(
        % The list of variables we are interested in
        [StudentID, Name, Email, School, Programme, GPA1, GPA2, CumulativeGPA],
        % The goal we want to find all solutions for
        (
            % Retrieve the student's details
            student(StudentID, Name, Email, School, Programme),
            % If cumulative_gpa/5 succeeds then format and print the student's name and cumulative GPA
            (   cumulative_gpa(StudentID, Name, GPA1, GPA2, Year, CumulativeGPA) ->
                format('Student: ~w, Cumulative GPA: ~2f~n', [Name, CumulativeGPA])
            % If cumulative_gpa/5 fails then print that no GPA was calculated for this student
            ;   CumulativeGPA = 'No GPA calculated',
                format('Student: ~w, No GPA calculated~n', [Name])
            )
        ),
        % The variable that will hold the results
        Results
    ).

% Updates the default GPA
update_default_gpa(NewGPA) :-
    % If retract/1 is able to remove the old GPA, it does nothing
    % If retract/1 is not able to remove the old GPA, it sets OldGPA to 'No old GPA'
    (   retract(default_gpa(OldGPA)) ->
        true
    ;   OldGPA = 'No old GPA'
    ),
    % Add the new GPA to the database
    assert(default_gpa(NewGPA)),
    write('Old GPA: '), write(OldGPA), nl,
    write('New GPA: '), write(NewGPA), nl.