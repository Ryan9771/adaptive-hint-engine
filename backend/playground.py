from setup_db import engine, Base, db_session, add_exercise, add_feature_attempt

if __name__ == "__main__":
    # Initialise db
    # Create the database
    Base.metadata.create_all(bind=engine)

    