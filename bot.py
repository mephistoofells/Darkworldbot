import telebot
from telebot import types
import math

bot = telebot.TeleBot("7867046071:AAFt1NHNUIKXsDV4rq2pHeWOh79Hz_FeeK0")

users = {}
global_users = []
waiting_for_random_chat = None
active_chats = {}
user_diaries = {}

@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.chat.id
    users[user_id] = {}
    bot.send_message(user_id, "🌑 به این دنیای کثیف خوش اومدی...\n\nاسم کوچیکتو بهم بگو، تا بهتر بشناسمت 👁️")
    bot.register_next_step_handler(message, ask_name)

def ask_name(message):
    user_id = message.chat.id
    users[user_id]['name'] = message.text
    rules = (
        "📜 قوانین این دنیا:\n"
        "❌ بی‌احترامی ممنوع\n"
        "🧠 به عقاید هم احترام بگذار\n"
        "🤐 فحش و ناسزا اکیداً ممنوع\n\n"
        "🕳️ تو دنیای واقعی همه چی کثیفه... شاید اینجا بهتر باشه.\n"
        "آیا می‌خوای به این جهان بپیوندی و تعامل بیشتری داشته باشی؟ 🤝"
    )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("✅ بله، می‌پیوندم")
    bot.send_message(user_id, rules, reply_markup=markup)
    bot.register_next_step_handler(message, ask_job)

def ask_job(message):
    if message.text != "✅ بله، می‌پیوندم":
        bot.send_message(message.chat.id, "اگر نمی‌خوای بپیوندی، پس خداحافظ 👋")
        return
    bot.send_message(message.chat.id, "🎭 اهل چه کاری هستی؟ مثلا: آهنگ خوندن، نقاشی، برنامه‌نویسی و ...")
    bot.register_next_step_handler(message, save_job)

def save_job(message):
    user_id = message.chat.id
    users[user_id]['job'] = message.text
    bot.send_message(user_id, "💠 چه نوع اخلاقی داری؟", reply_markup=ethics_buttons())

def ethics_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("😡 عصبانی", "😐 خنثی", "😃 شاد", "😔 غمگین")
    return markup

@bot.message_handler(func=lambda m: m.text in ["😡 عصبانی", "😐 خنثی", "😃 شاد", "😔 غمگین"])
def handle_ethics(message):
    user_id = message.chat.id
    users[user_id]['ethics'] = message.text
    bot.send_message(user_id, "📅 متولد چندی؟ (فقط سال تولد رو بفرست مثلا: 1383)")
    bot.register_next_step_handler(message, get_birth)

def get_birth(message):
    user_id = message.chat.id
    if not message.text.isdigit():
        bot.send_message(user_id, "🔢 فقط سال تولد عددی رو بفرست مثلا 1380")
        bot.register_next_step_handler(message, get_birth)
        return
    users[user_id]['birth_year'] = int(message.text)
    bot.send_message(user_id, "👥 دوست داری با چه جور آدمایی تعامل داشته باشی؟")
    bot.register_next_step_handler(message, get_preference)

def get_preference(message):
    user_id = message.chat.id
    users[user_id]['preference'] = message.text
    bot.send_message(user_id, "📏 قدت چند سانتی‌متره؟ فقط عدد بفرست مثلا 174")
    bot.register_next_step_handler(message, get_height)

def get_height(message):
    user_id = message.chat.id
    try:
        height = int(message.text)
        users[user_id]['height'] = height
        send_location_request(user_id)
    except:
        bot.send_message(user_id, "📏 لطفا فقط عدد بفرست مثلا 174")
        bot.register_next_step_handler(message, get_height)

def send_location_request(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = types.KeyboardButton("📍 ارسال لوکیشن", request_location=True)
    markup.add(button)
    bot.send_message(user_id, "🌐 لطفاً لوکیشن خودتو بفرست تا بتونیم نزدیک‌هات رو نشونت بدیم.", reply_markup=markup)

@bot.message_handler(content_types=['location'])
def handle_location(message):
    user_id = message.chat.id
    users[user_id]['location'] = {
        'lat': message.location.latitude,
        'lon': message.location.longitude
    }
    if user_id not in global_users:
        global_users.append(user_id)
    show_main_menu(user_id)

def show_main_menu(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🌍 ارتباط جهانی", "📡 ارتباط با نزدیکا", "🧠 دفترچه خاطرات من")
    markup.add("🎲 چت تصادفی", "🚪 خداحافظی با این دنیا", "🧨 ارتباط با سازنده")
    bot.send_message(user_id, "🎉 ثبت‌نامت کامل شد. خوش اومدی به جهانی تاریک ولی متفاوت...\n\nانتخاب کن 👇", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🧠 دفترچه خاطرات من")
def diary_handler(message):
    user_id = message.chat.id
    bot.send_message(user_id, "✍️ یک خاطره بنویس و برام بفرست تا ثبتش کنم.")
    bot.register_next_step_handler(message, save_diary)

def save_diary(message):
    user_id = message.chat.id
    user_diaries[user_id] = message.text
    bot.send_message(user_id, "✅ خاطرت ثبت شد! بقیه تو پروفایلت می‌تونن بخوننش.")
    show_main_menu(user_id)

@bot.message_handler(func=lambda m: m.text == "🎲 چت تصادفی")
def random_chat_handler(message):
    global waiting_for_random_chat
    user_id = message.chat.id
    if waiting_for_random_chat is None:
        waiting_for_random_chat = user_id
        bot.send_message(user_id, "⌛ منتظر طرف مقابل هستی...")
    else:
        partner_id = waiting_for_random_chat
        active_chats[user_id] = partner_id
        active_chats[partner_id] = user_id
        waiting_for_random_chat = None

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("❌ قطع ارتباط")

        bot.send_message(user_id, "🎯 شما به چت تصادفی وصل شدید! پیام‌هات مستقیماً برای طرف مقابل فرستاده می‌شن.", reply_markup=markup)
        bot.send_message(partner_id, "🎯 شما به چت تصادفی وصل شدید! پیام‌هات مستقیماً برای طرف مقابل فرستاده می‌شن.", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "❌ قطع ارتباط")
def disconnect_chat(message):
    user_id = message.chat.id
    if user_id in active_chats:
        partner_id = active_chats[user_id]
        del active_chats[user_id]
        del active_chats[partner_id]
        bot.send_message(user_id, "🚫 ارتباط شما قطع شد.")
        bot.send_message(partner_id, "🚫 طرف مقابل ارتباط رو قطع کرد.")
        show_main_menu(user_id)
        show_main_menu(partner_id)
    else:
        bot.send_message(user_id, "❗ شما در چت فعالی نیستی.")

@bot.message_handler(func=lambda m: m.chat.id in active_chats)
def relay_random_message(message):
    sender = message.chat.id
    receiver = active_chats.get(sender)
    if receiver:
        bot.send_message(receiver, f"💬 {message.text}")

bot.polling()
