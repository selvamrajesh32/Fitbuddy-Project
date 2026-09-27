import json
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import DATABASE_URL


connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {
        "check_same_thread": False
    }


engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    name = Column(String, nullable=False)

    age = Column(Integer, nullable=False)

    weight = Column(String, nullable=False)

    goal = Column(String, nullable=False)

    intensity = Column(String, nullable=False)


class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        String,
        index=True,
        nullable=False
    )

    original_plan = Column(
        Text,
        nullable=False
    )

    updated_plan = Column(
        Text,
        nullable=True
    )

    nutrition_tip = Column(
        Text,
        nullable=True
    )

    feedback = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


def init_db():
    Base.metadata.create_all(bind=engine)


def save_user(user_id, name, age, weight, goal, intensity):
    db = SessionLocal()

    try:
        existing_user = (
            db.query(User)
            .filter(User.user_id == user_id)
            .first()
        )

        if existing_user:
            existing_user.name = name
            existing_user.age = age
            existing_user.weight = str(weight)
            existing_user.goal = goal
            existing_user.intensity = intensity

        else:
            user = User(
                user_id=user_id,
                name=name,
                age=age,
                weight=str(weight),
                goal=goal,
                intensity=intensity
            )

            db.add(user)

        db.commit()

    finally:
        db.close()


def get_user(user_id):
    db = SessionLocal()

    try:
        return (
            db.query(User)
            .filter(User.user_id == user_id)
            .first()
        )

    finally:
        db.close()


def save_plan(user_id, original_plan, nutrition_tip):
    db = SessionLocal()

    try:
        original_plan_json = json.dumps(
            original_plan,
            ensure_ascii=False
        )

        plan = WorkoutPlan(
            user_id=user_id,
            original_plan=original_plan_json,
            updated_plan=None,
            nutrition_tip=nutrition_tip,
            feedback=None
        )

        db.add(plan)
        db.commit()
        db.refresh(plan)

        return plan

    finally:
        db.close()


def get_original_plan(user_id):
    db = SessionLocal()

    try:
        plan = (
            db.query(WorkoutPlan)
            .filter(WorkoutPlan.user_id == user_id)
            .order_by(WorkoutPlan.id.desc())
            .first()
        )

        if not plan:
            return None

        return json.loads(plan.original_plan)

    finally:
        db.close()


def update_plan(user_id, updated_plan, feedback):
    db = SessionLocal()

    try:
        plan = (
            db.query(WorkoutPlan)
            .filter(WorkoutPlan.user_id == user_id)
            .order_by(WorkoutPlan.id.desc())
            .first()
        )

        if not plan:
            return None

        plan.updated_plan = json.dumps(
            updated_plan,
            ensure_ascii=False
        )

        plan.feedback = feedback
        plan.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(plan)

        return plan

    finally:
        db.close()


def get_all_users():
    db = SessionLocal()

    try:
        return db.query(User).all()

    finally:
        db.close()


def get_all_plans():
    db = SessionLocal()

    try:
        return db.query(WorkoutPlan).all()

    finally:
        db.close()


def delete_user(user_id):
    db = SessionLocal()

    try:
        db.query(WorkoutPlan).filter(
            WorkoutPlan.user_id == user_id
        ).delete()

        db.query(User).filter(
            User.user_id == user_id
        ).delete()

        db.commit()

    finally:
        db.close()