from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database import get_session, User, Checkin
from datetime import datetime, timedelta
from handlers.referrals import complete_referral

router = Router()

# ===============================
# Daily Check-in Callback
# ===============================
@router.callback_query(F.data == "menu_daily")
async def daily_checkin(call: CallbackQuery):
    telegram_id = call.from_user.id
    session = get_session()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    if not user:
        await call.answer("❌ User not found.", show_alert=True)
        session.close()
        return

    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)

    # Fetch last check-in
    last_checkin = session.query(Checkin).filter_by(user_id=user.id).order_by(Checkin.date.desc()).first()

    if last_checkin and last_checkin.date == today:
        await call.answer("✅ You already checked in today!", show_alert=True)
        session.close()
        return

    # Check streak
    if last_checkin and last_checkin.date == yesterday:
        user.checkin_streak += 1
    else:
        user.checkin_streak = 1

    # Award points based on streak
    base_points = 10  # Base points for daily check-in
    bonus_points = 0

    # Streak bonuses
    if user.checkin_streak == 5:
        bonus_points = 20
    elif user.checkin_streak == 10:
        bonus_points = 50

    total_points = base_points + bonus_points
    user.points += total_points
    user.last_checkin = datetime.utcnow()

    # Log check-in
    new_checkin = Checkin(
        user_id=user.id,
        date=today,
        streak=user.checkin_streak
    )
    session.add(new_checkin)

    session.commit()
    session.close()

    # Check referral completion (first check-in)
    complete_referral(user.id)

    # Build response
    streak_text = f"🔥 Current Streak: {user.checkin_streak} days"
    bonus_text = f"💰 Bonus Points: {bonus_points}" if bonus_points else ""
    await call.message.answer(
        f"🎁 Daily Check-in Complete!\n"
        f"Points Earned: {total_points}\n"
        f"{streak_text}\n"
        f"{bonus_text}"
    )
    await call.answer()
