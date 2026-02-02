from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database import get_session, Task, UserTask, User
from datetime import datetime
import asyncio

router = Router()

# ===============================
# Task List Keyboard
# ===============================
def task_buttons(tasks):
    """
    Generates inline buttons for tasks
    """
    keyboard = InlineKeyboardMarkup(row_width=1)
    for task in tasks:
        status = "✅ Completed" if task.completed else "▶️ Start"
        keyboard.add(
            InlineKeyboardButton(f"{task.title} - {task.points} Points", callback_data=f"task_{task.id}")
        )
    return keyboard

# ===============================
# Menu Tasks Callback
# ===============================
@router.callback_query(F.data == "menu_tasks")
async def show_tasks(call: CallbackQuery):
    telegram_id = call.from_user.id
    session = get_session()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()

    # Fetch active tasks
    tasks = session.query(Task).filter_by(active=True).all()

    # Prepare keyboard
    keyboard = InlineKeyboardMarkup(row_width=1)
    for task in tasks:
        # Check if user completed
        completed = session.query(UserTask).filter_by(user_id=user.id, task_id=task.id, completed=True).first()
        status = "✅ Completed" if completed else "▶️ Start"
        keyboard.add(
            InlineKeyboardButton(f"{task.title} - {task.points} Points", callback_data=f"task_{task.id}")
        )
    session.close()

    await call.message.answer("🎯 Here are your tasks:", reply_markup=keyboard)
    await call.answer()

# ===============================
# Task Verification Callback
# ===============================
@router.callback_query(F.data.startswith("task_"))
async def task_verify(call: CallbackQuery):
    task_id = int(call.data.split("_")[1])
    telegram_id = call.from_user.id
    session = get_session()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    task = session.query(Task).filter_by(id=task_id, active=True).first()

    if not task:
        await call.answer("❌ Task not found or inactive.", show_alert=True)
        session.close()
        return

    # Check if already completed
    completed = session.query(UserTask).filter_by(user_id=user.id, task_id=task.id, completed=True).first()
    if completed:
        await call.answer("✅ You already completed this task!", show_alert=True)
        session.close()
        return

    # Send verification message with 10s delay
    msg = await call.message.answer(f"🔔 Verifying task '{task.title}'...\nPlease wait 10 seconds...")
    await asyncio.sleep(10)  # 10-second delay

    # Add points to user
    user.points += task.points
    # Log user task completion
    user_task = UserTask(user_id=user.id, task_id=task.id, completed=True, timestamp=datetime.utcnow())
    session.add(user_task)
    session.commit()
    session.close()

    await msg.edit_text(f"✅ Task '{task.title}' completed!\nYou earned {task.points} Points.")
    await call.answer("Task verified and points added!")
