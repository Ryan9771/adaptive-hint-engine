from setup_db import engine, Base, add_exercise, list_all_exercises

"""
Exercise Detail Format:

exercise_title - Title
exercise_background - Text before instructions
exercise_text - Exercise Instructions
skel_code - Default code

"""


if __name__ == "__main__":
    # Create the database
    Base.metadata.create_all(bind=engine)

    print(f"\n== All Exercises: ==\n{list_all_exercises()}")

    # Create the exercises
