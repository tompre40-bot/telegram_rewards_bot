🎯 Telegram Rewards Points & Referral Bot
A powerful Telegram Rewards Platform where users earn Points by completing tasks, daily check-ins, and inviting friends.
Points are converted into Wallet Balance which can be redeemed via UPI after meeting activity requirements.
❗ This is NOT an “earn money” bot.
It is a Rewards, Tasks & Engagement Platform.
🚀 Features
👤 User Features
✅ Sponsor Channel Force Join (rotating every 24h)
🎯 Tasks System (join, visit, shortlink, app install)
🎁 Daily Check-in with streak bonuses
👥 Referral System with milestones
🏆 Levels & rewards
💰 Wallet & Withdraw (UPI)
📊 Personal statistics
🔔 Live rewards activity feed
🛡 Anti-fraud protection
🛠 Admin Panel
Button-based admin controls:
View total users
Ban / unban users
Add / remove points
Manage wallet balance
Add / remove tasks & premium tasks
Manage sponsor channels
Broadcast messages
Change points → wallet conversion rate
Approve / reject withdrawals
🧠 Core Concept
Two separate economies:
System
Purpose
Points
Engagement, tasks, streaks, referrals
Wallet
Real redeemable value (admin controlled)
Admin can change conversion anytime:
Copy code

1000 Points = ₹10
🗂 Project Structure
Copy code

bot/
│
├── start.py
├── config.py
├── database.py
├── requirements.txt
│
├── handlers/
│   ├── tasks.py
│   ├── referrals.py
│   ├── checkin.py
│   ├── wallet.py
│   ├── sponsors.py
│   ├── stats.py
│   └── admin_panel.py
│
├── keyboards/
│   ├── main_menu.py
│   └── admin_menu.py
│
└── utils/
    ├── helpers.py
    ├── anti_fraud.py
    └── shortlink.py
⚙️ Installation (Local / VPS)
1️⃣ Clone repo
Copy code
Bash
git clone https://github.com/yourusername/rewards-bot.git
cd rewards-bot
2️⃣ Create virtual environment
Copy code
Bash
python -m venv venv
source venv/bin/activate
3️⃣ Install requirements
Copy code
Bash
pip install -r requirements.txt
4️⃣ Create .env file
Copy code

BOT_TOKEN=YOUR_BOT_TOKEN
ADMIN_IDS=123456789
DB_URL=sqlite:///rewards.db
For PostgreSQL (VPS):
Copy code

DB_URL=postgresql://user:pass@localhost/dbname
5️⃣ Run bot
Copy code
Bash
python start.py
🗄 Database
Supports:
SQLite (testing)
PostgreSQL (production)
Tables:
users
referrals
tasks
premium_tasks
sponsors
withdrawals
checkins
user_tasks
settings
💸 Monetization Model
This bot earns from:
Sponsor channels
Shortlinks
App install offers
Promotional tasks
Users stay engaged daily through:
Streaks
Levels
Referrals
Rewards feed
🛡 Anti-Fraud Protection
Self-referral blocked
Multiple account detection
Task farming detection
Referral farming detection
Suspicious user auto-ban
🔑 Important Wording Used in Bot
Allowed words:
Points, Rewards, Bonus, Redeem
Avoided words:
Earn money, Free money
📌 Deployment Tips
Use SQLite for testing
Use PostgreSQL on VPS
Run with screen or pm2 for 24/7 uptime
Integrate real shortlink API in utils/shortlink.py
👨‍💻 Built With
Python
Aiogram
SQLAlchemy
Telegram Bot API
📜 License
Free to use and modify for your own project.
