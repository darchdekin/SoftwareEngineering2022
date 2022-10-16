import pytest
import System

ta_u = "cmhbf5"
ta_p = "bestTA"

cc_prof_u = "calyam"
cc_prof_p = "#yeet"

cs_prof_u = "saab"
cs_prof_p = "boomr345"

s_u = "akend3"
s_p = "123454321"

s_u2 = 'hdjsr7'
s_p2 = 'pass1234'

def test_login(grading_system):
    grading_system.login(ta_u,ta_p)
    assert type(grading_system.usr).__name__ == "TA"
    assert grading_system.usr.name == ta_u
    assert grading_system.usr.users == grading_system.users
    assert grading_system.usr.password == ta_p
    assert grading_system.usr.courses == grading_system.users[ta_u]["courses"]

def test_check_password(grading_system):
    test = grading_system.check_password(ta_u,ta_p)
    test2 = grading_system.check_password(ta_u, 'bestTA')
    test3 = grading_system.check_password(ta_u,'BESTTA')
    if test == test3 or test2 == test3:
        assert False
    if test != test2:
        assert False

def test_change_grade(grading_system):
    grading_system.login(ta_u,ta_p)
    grading_system.usr.change_grade("yted91", "cloud_computing", "assignment1", 4)

    db = grading_system.load_user_db()
    assert db["yted91"]["courses"]["cloud_computing"]["assignment1"]["grade"] == 4

def test_create_assignment(grading_system):
    grading_system.login(ta_u,ta_p)
    grading_system.usr.create_assignment("test_asgn", "2/2/22", "comp_sci")

    c = grading_system.load_course_db()

    assert c["comp_sci"]["assignments"]["test_asgn"]["due_date"] == "2/2/22"

def test_add_student(grading_system):
    grading_system.login(cc_prof_u, cc_prof_p)
    grading_system.usr.add_student("akend3", "cloud_computing")

    db = grading_system.load_user_db()
    assert db["akend3"]["courses"]["cloud_computing"]["assignment1"]["grade"] == "N/A"

def test_drop_student(grading_system):
    grading_system.login(cc_prof_u, cc_prof_p)
    grading_system.usr.drop_student("hdjsr7", "cloud_computing")

    db = grading_system.load_user_db()
    assert "cloud_computing" not in db["hdjsr7"]["courses"]

def test_submit_assignment(grading_system):
    grading_system.login(s_u, s_p)
    grading_system.usr.submit_assignment("databases", "assignment1", "lorem ipsum", "1/5/20")

    db = grading_system.load_user_db()
    assert db["akend3"]["courses"]["databases"]["assignment1"]["submission"] == "lorem ipsum"
    assert db["akend3"]["courses"]["databases"]["assignment1"]["submission_date"] == "1/5/20"

def test_check_ontime(grading_system):
    grading_system.login(s_u, s_p)
    test1 = grading_system.usr.check_ontime("1/1/20", "1/2/20")
    test2 = grading_system.usr.check_ontime("1/9/20", "1/8/20")
    assert test1
    assert not test2

def test_check_grades(grading_system):
    grading_system.login(s_u2, s_p2)
    grades1 = grading_system.usr.check_grades("cloud_computing")
    grades2 = grading_system.load_user_db()[s_u2]["courses"]["cloud_computing"]

    for grade_entry in grades1:
        assignment_name = grade_entry[0]
        grade = grade_entry[1]
        assert grades2[assignment_name]["grade"] == grade

#The function view_assignments only works with the course comp_sci
def test_view_assignments(grading_system):
    grading_system.login(s_u, s_p)
    result = grading_system.usr.view_assignments("databases")

    course = grading_system.load_course_db()["databases"]["assignments"]
    assignments = []
    for key in course:
        assignments.append([key,course[key]['due_date']])

    assert assignments == result

@pytest.fixture
def grading_system():
    gradingSystem = System.System()
    gradingSystem.load_data()
    return gradingSystem
