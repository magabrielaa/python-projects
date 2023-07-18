
def gen_class_rosters(students, instructor_assignments):

    d_roster = {}

    for i, (course, instructor) in enumerate(instructor_assignments):
        if course not in d_roster:
            d_roster[course] = {}
        for student in students:
            student_dict = dict(student)
            del student_dict["Courses"]
            d_roster[course]["Instructor"] = instructor
            d_roster[course]["Students"] = student_dict
        
    return d_roster


