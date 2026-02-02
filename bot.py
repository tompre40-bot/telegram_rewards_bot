from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from config import BOT_TOKEN
from handlers import start, tasks, referrals, checkin, wallet, sponsors, stats, admin_panel

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Register handlers
start.register_handlers(dp)
tasks.register_handlers(dp)
referrals.register_handlers(dp)
checkin.register_handlers(dp)
wallet.register_handlers(dp)
sponsors.register_handlers(dp)
stats.register_handlers(dp)
admin_panel.register_handlers(dp)

# Bot commands
async def set_commands():
    await bot.set_my_commands([
        BotCommand(command="start", description="Start the Rewards Bot"),
    ])

if __name__ == "__main__":
    import asyncio
    asyncio.run(set_commands())
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
