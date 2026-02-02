from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database import get_session, User, UserTask, Withdrawal, Checkin
from datetime import datetime, timedelta

router = Router()

# ===============================
# Menu Stats Callback
# ===============================
@router.callback_query(F.data == "menu_stats")
async def show_stats(call: CallbackQuery):
    session = get_session()
    
    # Total users
    total_users = session.query(User).count()

    # Total rewards redeemed (sum of approved withdrawals)
    total_redeemed = session.query(Withdrawal).filter_by(status="approved").all()
    total_redeemed_amount = sum([w.amount for w in total_redeemed])

    # Active users today (any activity today)
    today = datetime.utcnow().date()
    active_tasks = session.query(UserTask).filter(UserTask.timestamp >= datetime(today.year, today.month, today.day)).count()
    active_checkins = session.query(Checkin).filter_by(date=today).count()
    active_users_today = active_tasks + active_checkins

    # Live Rewards Feed (last 5 activities)
    recent_tasks = session.query(UserTask).order_by(UserTask.timestamp.desc()).limit(5).all()
    recent_withdrawals = session.query(Withdrawal).order_by(Withdrawal.timestamp.desc()).limit(5).all()
    feed_lines = []

    for task in recent_tasks:
        user = session.query(User).filter_by(id=task.user_id).first()
        if user:
            feed_lines.append(f"🎯 {user.username or 'User'} completed a task (+{task.completed})")

    for wd in recent_withdrawals:
        user = session.query(User).filter_by(id=wd.user_id).first()
        if user and wd.status=="approved":
            feed_lines.append(f"💰 {user.username or 'User'} redeemed ₹{wd.amount}")

    feed_text = "\n".join(feed_lines[:5]) if feed_lines else "No recent activity."

    session.close()

    # Build stats message
    text = (
        f"📊 Bot Statistics:\n"
        f"👥 Total Users: {total_users}\n"
        f"💸 Total Rewards Redeemed: ₹{total_redeemed_amount}\n"
        f"🔥 Active Users Today: {active_users_today}\n\n"
        f"📢 Live Rewards Feed:\n{feed_text}"
    )

    # Back to main menu button
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("⬅️ Back to Menu", callback_data="menu_back"))

    await call.message.answer(text, reply_markup=keyboard)
    await call.answer()
