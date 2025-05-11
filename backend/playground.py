from setup_db import add_exercise, required_concepts_exists, set_required_concepts, get_required_concepts, get_past_concept_scores, update_student_profile, initialise_student_profile, engine, Base
from example_exercises.python.exercise_1 import exercise_1

if __name__ == "__main__":
    # Initialise db
    # Create the database
    Base.metadata.create_all(bind=engine)
    exercise_key = exercise_1["exercise_key"]

    past_scores_1 = get_past_concept_scores(exercise_key=exercise_key)
    print(f"Past scores: {past_scores_1}")

    implemented_concepts = {'loops': 4, 'range_function': 4, 'modulo_operator': 4,
                            'conditional_statements': 2, 'print_statements': 2, 'comparison_operations': 4, 'boolean_logic': 4}

    update_student_profile(
        exercise_key=exercise_key,
        updated_scores=implemented_concepts
    )

    past_scores_2 = get_past_concept_scores(exercise_key=exercise_key)
    print(f"Past scores: {past_scores_2}")
