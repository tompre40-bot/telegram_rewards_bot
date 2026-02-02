from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from database import get_session, User, Referral, UserTask
from urllib.parse import quote, unquote
from datetime import datetime

router = Router()

# ===============================
# Generate Referral Link
# ===============================
def generate_referral_link(telegram_id: int):
    base_link = "https://t.me/YourBotUsername?start="
    ref_code = str(telegram_id)
    return base_link + ref_code

# ===============================
# /start with Referral Code
# ===============================
@router.message(F.text.startswith("/start"))
async def start_with_referral(message: Message):
    args = message.text.split()
    session = get_session()
    telegram_id = message.from_user.id
    username = message.from_user.username

    # Get or create user
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    if not user:
        user = User(
            telegram_id=telegram_id,
            username=username,
            registered_at=datetime.utcnow()
        )
        session.add(user)
        session.commit()

    # Handle referral code if exists
    if len(args) > 1:
        ref_code = args[1]
        if ref_code.isdigit():
            referrer_id = int(ref_code)
            if referrer_id != telegram_id:
                # Check if referral already exists
                existing_ref = session.query(Referral).filter_by(referred_id=user.id).first()
                if not existing_ref:
                    referral = Referral(referrer_id=referrer_id, referred_id=user.id, task_completed=False)
                    session.add(referral)
                    session.commit()
    session.close()

# ===============================
# Menu Refer Callback
# ===============================
@router.callback_query(F.data == "menu_refer")
async def show_referral(call: CallbackQuery):
    telegram_id = call.from_user.id
    session = get_session()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    if not user:
        await call.answer("❌ User not found.", show_alert=True)
        session.close()
        return

    # Count referrals who completed first task
    completed_refs = session.query(Referral).filter_by(referrer_id=user.id, task_completed=True).count()

    # Generate referral link
    ref_link = generate_referral_link(telegram_id)

    # Build reply
    text = (
        f"👥 Your Referral Link:\n{ref_link}\n\n"
        f"✅ Referrals Completed: {completed_refs}\n"
        f"🎁 Points & Wallet bonuses will be awarded after their first task or daily check-in."
    )

    # Button to copy link
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🔗 Copy Referral Link", url=ref_link))

    session.close()
    await call.message.answer(text, reply_markup=keyboard)
    await call.answer()

# ===============================
# Mark Referral as Completed
# Call this when user completes first task/check-in
# ===============================
def complete_referral(user_id: int):
    """
    Call this function after user completes first task/check-in
    """
    session = get_session()
    referral = session.query(Referral).filter_by(referred_id=user_id, task_completed=False).first()
    if referral:
        # Mark as completed
        referral.task_completed = True

        # Award referrer: e.g., 50 points + 1 wallet unit
        referrer = session.query(User).filter_by(id=referral.referrer_id).first()
        if referrer:
            referrer.points += 50  # Example points
            referrer.wallet_balance += 1  # Example wallet bonus
        session.commit()
    session.close()
