import sys
import os

if len(sys.argv) < 2:
    exit()


def seed_database():
    from passlib.hash import bcrypt
    from db.database import Session
    import db.tables
    from core.division.model import Division
    from core.grade.model import Grade
    from core.schedule.model import Schedule
    from core.grade.type import GradeLevel, Vocational
    from core.user.model import User, UserPending
    from core.user.type import Role
    from core.attendance.model import Attendance
    from core.attendance.type import State

    db = Session()

    grade = Grade(
        grade=GradeLevel.XII,
        vocational=Vocational.TKI,
        name="XII PPLG 1"
    )

    division = Division(
        name="Game Development",
        wa_group_link="https://whatsapp.com",
    )

    schedule = Schedule(
        note="This is schedule note",
        location="D2.4",
        token="TOKEN123",
        attendance_is_open=False,
        division_id=1
    )

    user_pending = UserPending(
        name="John Doe",
        email="johndoe@gmail.com",
        motivation="Here is my motivation",
        division_id=1,
        grade_id=1,
    )

    user = User(
        name="User",
        email="user@gmail.com",
        password=bcrypt.hash("password"),
        role=Role.user,
        refresh_token="123",
        phone_number="08123456789",
        division_id=1,
        grade_id=1,
    )

    admin = User(
        name="Admin",
        email="admin@gmail.com",
        password=bcrypt.hash("password"),
        role=Role.admin,
        refresh_token="1234",
        phone_number="08123456789",
        division_id=1,
        grade_id=1,
    )

    superadmin = User(
        name="SuperAdmin",
        email="superadmin@gmail.com",
        password=bcrypt.hash("password"),
        role=Role.superadmin,
        refresh_token="12345",
        phone_number="08123456789",
        division_id=1,
        grade_id=1,
    )

    attendance = Attendance(
        status=State.HADIR,
        rating=5,
        feedback="Good",
        suggestion="Talking too fast",
    )

    db.add(grade)
    db.add(division)
    db.add(schedule)
    db.add(user_pending)
    db.add(user)
    db.add(admin)
    db.add(superadmin)
    db.commit()

    attendance.schedule_id = schedule.id
    attendance.user_id = user.id
    db.add(attendance)
    db.commit()


if __name__ == "__main__":

    sys.path.insert(0, os.path.abspath(
       os.path.join(os.path.dirname(__file__), "src")
    ))

    if sys.argv[1] == "seed":
        seed_database()
    elif sys.argv[1] == "drop-all":
        from db import tables

        tables.drop_all()
