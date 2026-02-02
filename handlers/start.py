from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database import get_session, User, Sponsor
from datetime import datetime

router = Router()

# ===============================
# Main Menu Keyboard
# ===============================
def main_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🎯 Tasks", callback_data="menu_tasks"),
        InlineKeyboardButton("👥 Refer", callback_data="menu_refer"),
        InlineKeyboardButton("🎁 Daily", callback_data="menu_daily"),
        InlineKeyboardButton("💰 Wallet", callback_data="menu_wallet"),
        InlineKeyboardButton("🏆 Levels", callback_data="menu_levels"),
        InlineKeyboardButton("📊 Stats", callback_data="menu_stats"),
    )
    return keyboard

# ===============================
# /start Handler
# ===============================
@router.message(F.text == "/start")
async def start_command(message: Message):
    telegram_id = message.from_user.id
    username = message.from_user.username

    session = get_session()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()

    if not user:
        # New user
        user = User(
            telegram_id=telegram_id,
            username=username,
            registered_at=datetime.utcnow()
        )
        session.add(user)
        session.commit()

    # Check sponsor channels (force join)
    active_sponsors = session.query(Sponsor).filter_by(active=True).all()
    session.close()

    if active_sponsors:
        sponsor_list = "\n".join([f"- {s.channel}" for s in active_sponsors])
        await message.answer(
            f"Welcome {message.from_user.full_name}!\n\n"
            "Before you can access the main menu, please join the following sponsor channels:\n\n"
            f"{sponsor_list}\n\n"
            "After joining, click any button below to continue.",
            reply_markup=main_menu()
        )
    else:
        await message.answer(
            f"Welcome {message.from_user.full_name}!\n\n"
            "Your main menu is ready:",
            reply_markup=main_menu()
        )
