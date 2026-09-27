from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.database import (
    delete_user,
    get_all_plans,
    get_all_users,
    get_original_plan,
    get_user,
    save_plan,
    save_user,
    update_plan,
)

from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.gemini_generator import generate_workout_gemini
from app.schemas import FeedbackRequest, UserAPIResponse, UserInput
from app.updated_plan import update_workout_plan


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "error": None
        }
    )


@router.post("/generate-workout")
async def generate_workout(
    request: Request,
    name: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):
    try:
        user_data = UserInput(
            name=name,
            user_id=user_id,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity
        )

        workout_plan = generate_workout_gemini(
            name=user_data.name,
            age=user_data.age,
            weight=user_data.weight,
            goal=user_data.goal,
            intensity=user_data.intensity
        )

        nutrition_tip = generate_nutrition_tip_with_flash(
            goal=user_data.goal,
            weight=user_data.weight
        )

        save_user(
            user_id=user_data.user_id,
            name=user_data.name,
            age=user_data.age,
            weight=user_data.weight,
            goal=user_data.goal,
            intensity=user_data.intensity
        )

        save_plan(
            user_id=user_data.user_id,
            original_plan=workout_plan,
            nutrition_tip=nutrition_tip
        )

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": user_data,
                "workout_plan": workout_plan,
                "nutrition_tip": nutrition_tip,
                "error": None
            }
        )

    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "error": str(e)
            }
        )


@router.post("/submit-feedback")
async def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...)
):
    try:
        user = get_user(user_id)
        plan = get_original_plan(user_id)

        if not user or not plan:
            return templates.TemplateResponse(
                request=request,
                name="index.html",
                context={
                    "error": "User or workout plan not found."
                }
            )

        revised_plan = update_workout_plan(
            original_plan=plan.original_plan,
            feedback=feedback,
            goal=user.goal,
            intensity=user.intensity
        )

        update_plan(
            plan_id=plan.id,
            updated_plan=revised_plan,
            feedback=feedback
        )

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": user,
                "workout_plan": revised_plan,
                "nutrition_tip": plan.nutrition_tip,
                "error": None
            }
        )

    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "error": str(e)
            }
        )


@router.get("/view-all-users")
async def view_all_users(request: Request):
    users = get_all_users()
    plans = get_all_plans()

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "users": users,
            "plans": plans
        }
    )


@router.post("/delete-user/{user_id}")
async def remove_user(user_id: str):
    delete_user(user_id)

    return RedirectResponse(
        url="/view-all-users",
        status_code=303
    )


@router.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "message": "FitBuddy AI is running"
    }


@router.post(
    "/api/generate-workout",
    response_model=UserAPIResponse
)
async def api_generate_workout(data: UserInput):

    workout_plan = generate_workout_gemini(
        name=data.name,
        age=data.age,
        weight=data.weight,
        goal=data.goal,
        intensity=data.intensity
    )

    nutrition_tip = generate_nutrition_tip_with_flash(
        goal=data.goal,
        weight=data.weight
    )

    save_user(
        user_id=data.user_id,
        name=data.name,
        age=data.age,
        weight=data.weight,
        goal=data.goal,
        intensity=data.intensity
    )

    save_plan(
        user_id=data.user_id,
        original_plan=workout_plan,
        nutrition_tip=nutrition_tip
    )

    return UserAPIResponse(
        user_id=data.user_id,
        name=data.name,
        workout_plan=workout_plan,
        nutrition_tip=nutrition_tip
    )


@router.post("/api/submit-feedback")
async def api_submit_feedback(data: FeedbackRequest):

    user = get_user(data.user_id)
    plan = get_original_plan(data.user_id)

    if not user or not plan:
        return {
            "success": False,
            "message": "User or workout plan not found."
        }

    revised_plan = update_workout_plan(
        original_plan=plan.original_plan,
        feedback=data.feedback,
        goal=user.goal,
        intensity=user.intensity
    )

    update_plan(
        plan_id=plan.id,
        updated_plan=revised_plan,
        feedback=data.feedback
    )

    return {
        "success": True,
        "user_id": data.user_id,
        "updated_plan": revised_plan
    }