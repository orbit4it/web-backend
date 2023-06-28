import sys

if len(sys.argv) < 2:
    exit()

def seed_database():
    from src.db import Session, tables
    from src.core.user.model import User, UserPending, Role
    from src.core.grade.model import Grade, GradeLevel, Vocational
    from src.core.division.model import Division

    db = Session()

    grade = Grade(
        grade=GradeLevel.XII,
        vocational=Vocational.TKI,
        name="XII PPLG 1"
    )

    division = Division(
        name="Game Development",
        wa_group_links="https://whatsapp.com",
    )

    user_pending = UserPending(
        name="John Doe",
        email="johndoe@gmail.com",
        motivation="Here is my motivation",

        division_id=1,
        grade_id=1,
    )

    user = User(
        name = "John Doe",
        email = "johndoe@gmail.com",
        password = "password",
        role = Role.user,
        refresh_token = "123456789",
        phone_number = "08123456789",

        division_id = 1,
        grade_id = 1,
    )

    db.add(grade)
    db.add(division)
    db.add(user_pending)
    db.add(user)
    db.commit()

if __name__ == '__main__':

    if sys.argv[1] == "seed":
        seed_database()
    elif sys.argv[1] == "drop-all":
        from src.db import tables
        tables.drop_all()

