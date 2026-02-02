from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from database import get_session, User, Withdrawal, UserTask, Referral, Checkin, Setting
from datetime import datetime

router = Router()

# ===============================
# Helper: Get points to wallet conversion
# ===============================
def get_conversion_rate():
    session = get_session()
    setting = session.query(Setting).filter_by(key="points_to_wallet").first()
    session.close()
    if setting:
        try:
            return float(setting.value)
        except:
            return 100  # Default: 100 points = ₹1
    return 100

# ===============================
# Menu Wallet Callback
# ===============================
@router.callback_query(F.data == "menu_wallet")
async def show_wallet(call: CallbackQuery):
    telegram_id = call.from_user.id
    session = get_session()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    if not user:
        await call.answer("❌ User not found.", show_alert=True)
        session.close()
        return

    conversion = get_conversion_rate()
    wallet_value = round(user.points / conversion, 2)

    # Build wallet menu
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("💸 Redeem", callback_data="wallet_redeem"))

    session.close()
    await call.message.answer(
        f"💰 Wallet Balance:\n"
        f"Points: {user.points}\n"
        f"Redeemable: ₹{wallet_value}",
        reply_markup=keyboard
    )
    await call.answer()

# ===============================
# Redeem Callback
# ===============================
@router.callback_query(F.data == "wallet_redeem")
async def redeem_points(call: CallbackQuery):
    telegram_id = call.from_user.id
    session = get_session()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    if not user:
        await call.answer("❌ User not found.", show_alert=True)
        session.close()
        return

    # Check activity requirements
    tasks_done = session.query(UserTask).filter_by(user_id=user.id, completed=True).count()
    referrals_done = session.query(Referral).filter_by(referrer_id=user.id, task_completed=True).count()
    checkins_done = session.query(Checkin).filter_by(user_id=user.id).count()

    if tasks_done < 5 or referrals_done < 3 or checkins_done < 3:
        await call.answer(
            "❌ You must complete 5 tasks, 3 referrals, and 3 daily check-ins to withdraw.",
            show_alert=True
        )
        session.close()
        return

    conversion = get_conversion_rate()
    withdraw_amount = round(user.points / conversion, 2)

    if withdraw_amount < 1:  # Minimum redeem threshold
        await call.answer("❌ Minimum redeem amount is ₹1.", show_alert=True)
        session.close()
        return

    # Ask user for UPI ID
    await call.message.answer("💳 Please reply with your UPI ID to request withdrawal:")
    
    # Store user in state for next message
    from aiogram.fsm.context import FSMContext
    from aiogram.fsm.storage.memory import MemoryStorage
    storage = MemoryStorage()
    state = FSMContext(storage, call.from_user.id)
    await state.set_data({"redeem_amount": withdraw_amount})
    await call.answer()

# ===============================
# Capture UPI ID Response
# ===============================
@router.message(F.text)
async def process_upi(message: Message):
    # We assume the last FSM context is for redeem
    from aiogram.fsm.context import FSMContext
    from aiogram.fsm.storage.memory import MemoryStorage
    storage = MemoryStorage()
    state = FSMContext(storage, message.from_user.id)
    data = await state.get_data()
    if not data or "redeem_amount" not in data:
        return  # Not a redeem flow

    upi_id = message.text.strip()
    withdraw_amount = data["redeem_amount"]

    session = get_session()
    user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    if not user:
        await message.answer("❌ User not found.")
        session.close()
        return

    # Deduct points
    points_to_deduct = int(withdraw_amount * get_conversion_rate())
    if user.points < points_to_deduct:
        await message.answer("❌ Not enough points for withdrawal.")
        session.close()
        return

    user.points -= points_to_deduct

    # Create withdrawal request
    withdrawal = Withdrawal(
        user_id=user.id,
        amount=withdraw_amount,
        upi_id=upi_id,
        status="pending",
        timestamp=datetime.utcnow()
    )
    session.add(withdrawal)
    session.commit()
    session.close()

    await message.answer(
        f"✅ Withdrawal request submitted!\n"
        f"Amount: ₹{withdraw_amount}\n"
        f"UPI: {upi_id}\n"
        f"Status: Pending approval by admin."
    )

    await state.clear()
