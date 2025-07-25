
import telebot
import random
import json
import os

BOT_TOKEN = "ISI_TOKEN_BOTMU_DI_SINI"
bot = telebot.TeleBot(BOT_TOKEN)

DATA_FILE = "user_data.json"

# Inisialisasi file jika belum ada
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

# Fungsi untuk load dan save data
def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_or_create_user(user_id, username):
    data = load_data()
    if str(user_id) not in data:
        data[str(user_id)] = {
            "username": username,
            "wallet": None,
            "balance": 0
        }
        save_data(data)
    return data[str(user_id)]

def update_user(user_id, field, value):
    data = load_data()
    data[str(user_id)][field] = value
    save_data(data)

@bot.message_handler(commands=['start'])
def handle_start(message):
    user = get_or_create_user(message.from_user.id, message.from_user.username)
    bot.send_message(message.chat.id, f"👋 Welcome {message.from_user.first_name}!

Use the menu below to start mining 🛠️", reply_markup=main_menu())

@bot.message_handler(func=lambda msg: msg.text == "🎯 Start Mining")
def handle_mining(message):
    user = get_or_create_user(message.from_user.id, message.from_user.username)

    ball_types = [
        ("💎 Diamond Ball", 4),
        ("🥇 Gold Ball", 3),
        ("🥈 Silver Ball", 2),
        ("💚 Emerald Ball", 1),
    ]
    ball = random.choice(ball_types)
    user["balance"] += ball[1]
    update_user(message.from_user.id, "balance", user["balance"])

    wallet_display = user["wallet"] or "Not set"
    bot.send_message(message.chat.id,
        f"👤 User ID: {message.from_user.id}
"
        f"💼 TON Wallet: {wallet_display}
"
        f"🎯 Mining session started...

"
        f"🎉 You caught a {ball[0]}!
"
        f"🪙 +{ball[1]} BEX added to your balance.

"
        f"💰 Current Balance: {user['balance']} BEX"
    )

@bot.message_handler(func=lambda msg: msg.text == "💰 My Balance")
def handle_balance(message):
    user = get_or_create_user(message.from_user.id, message.from_user.username)
    wallet_display = user["wallet"] or "Not set"
    bot.send_message(message.chat.id,
        f"👤 User ID: {message.from_user.id}
"
        f"💼 TON Wallet: {wallet_display}
"
        f"💰 Current Balance: {user['balance']} BEX"
    )

@bot.message_handler(func=lambda msg: msg.text == "🔗 Set Wallet")
def ask_wallet(message):
    msg = bot.send_message(message.chat.id, "🔐 Please send your TON wallet address:")
    bot.register_next_step_handler(msg, save_wallet)

def save_wallet(message):
    wallet = message.text.strip()
    update_user(message.from_user.id, "wallet", wallet)
    bot.send_message(message.chat.id, f"✅ Wallet saved: {wallet}")

@bot.message_handler(func=lambda msg: msg.text == "🚀 Join Presale")
def join_presale(message):
    bot.send_message(message.chat.id,
        "🚀 Join our presale now!

Visit: https://bex-presale.example.com

🔗 Make sure your wallet is connected."
    )

@bot.message_handler(func=lambda msg: msg.text == "🏆 Leaderboard")
def show_leaderboard(message):
    data = load_data()
    sorted_users = sorted(data.items(), key=lambda x: x[1]["balance"], reverse=True)[:10]
    leaderboard = "🏆 Top Miners:
"
    for i, (uid, info) in enumerate(sorted_users, 1):
        leaderboard += f"{i}. @{info['username'] or 'Unknown'} - {info['balance']} BEX
"
    bot.send_message(message.chat.id, leaderboard)

def main_menu():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🎯 Start Mining", "💰 My Balance")
    markup.row("🔗 Set Wallet", "🚀 Join Presale")
    markup.row("🏆 Leaderboard")
    return markup

print("Bot is running...")
bot.infinity_polling()
