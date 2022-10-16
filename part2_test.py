#These are the tests that I chose

import pytest
import System


cc_prof_u = "calyam"
cc_prof_p = "#yeet"

hdjsr7 = 'hdjsr7'
hdjsr7_p = 'pass1234'

akend3 = "akend3"
akend3_p = "123454321"

ta_u = "cmhbf5"
ta_p = "bestTA"

#Check if a professor can add students to a class that they don't teach
def test_add_student_2(grading_system):
    prev_state = grading_system.load_user_db()["akend3"]["courses"]

    grading_system.login(cc_prof_u, cc_prof_p)
    grading_system.usr.add_student("akend3", 'software_engineering')

    curr_state = grading_system.load_user_db()["akend3"]["courses"]
    assert prev_state == curr_state

#Check if professor can drop a student for a class they don't teach
#The try block is included because we want this function to result in an error if the input is invalid
def test_drop_student_2(grading_system):
    prev_state = grading_system.load_user_db()["akend3"]["courses"]

    grading_system.login(cc_prof_u, cc_prof_p)
    try:
        grading_system.usr.drop_student("akend3", 'comp_sci')
    except:
        assert True

    curr_state = grading_system.load_user_db()["akend3"]["courses"]
    assert prev_state == curr_state

#Check if staff can change grades for a class they don't teach
#The try block is included because we want this function to result in an error if the input is invalid
def test_change_grades_2(grading_system):
    grading_system.login(ta_u, ta_p)
    prev_state = grading_system.load_user_db()["hdjsr7"]["courses"]["databases"]["assignment1"]["grade"]
    try:
        grading_system.usr.change_grade("hdjsr7", "databases", "assignment1", 90)
    except:
        assert True
    assert prev_state == grading_system.load_user_db()["hdjsr7"]["courses"]["databases"]["assignment1"]["grade"]

#Check if staff can add assignment for a class they don't teach
#The try block is included because we want this function to result in an error if the input is invalid
def test_create_assignment_2(grading_system):
    grading_system.login(ta_u, ta_p)
    prev_state = grading_system.load_course_db()["databases"]["assignments"]
    try:
        grading_system.usr.create_assignment("test_assignment", "10/16/22", "databases")
    except:
        assert True
    assert prev_state == grading_system.load_course_db()["databases"]["assignments"]


#Check if a student can view assignments for a class they are not enrolled in
#The try block is included because we want this function to result in an error if the input is invalid
def test_view_assignments_unenrolled(grading_system):
    grading_system.login(akend3, akend3_p)
    try:
        result = grading_system.usr.view_assignments("cloud_computing")
    except:
        assert True
    assert len(result) == 0


@pytest.fixture
def grading_system():
    gradingSystem = System.System()
    gradingSystem.load_data()
    return gradingSystem
