import time
import schedule
import telebot

from schedule import every, repeat
from threading import Thread
from telebot import types

from config import BOT_TOKEN, ADMIN_CHAT_ID

from actions.actions import poll_delayed_messages, send_approved_message, send_declined_message, send_delayed_message, approved_from_user_message, declined_from_user_message, anonymous_from_user_message

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Приветствую! Пришлите фото или видео с сообщением или без.")
    print(f"Registered start message from user {message.from_user.username} in chat {message.chat.id}")

@bot.message_handler(content_types=["photo", "text", "video"])
def handle_message(message):
    # Copy message content and send to admin with inline keyboard
    confirmation_markup = types.InlineKeyboardMarkup()
    approve_button = types.InlineKeyboardButton("✅Подтвердить", callback_data=f"user_post_approve:{message.chat.id}:{message.id}")
    decline_button = types.InlineKeyboardButton("❌Отклонить", callback_data=f"user_post_decline:{message.chat.id}:{message.id}")
    anonymous_button = types.InlineKeyboardButton("🙈Отправить анонимно", callback_data=f"user_post_anonymous:{message.chat.id}:{message.id}")
    confirmation_markup.add(approve_button, decline_button)
    confirmation_markup.add(anonymous_button)

    if message.text:
        bot.send_message(message.chat.id, message.text, reply_markup=confirmation_markup)
    elif message.photo:
        photo_file_id = message.photo[-1].file_id
        message.caption = message.caption if message.caption else ''
        bot.send_photo(message.chat.id, photo_file_id, caption=message.caption, reply_markup=confirmation_markup)
    elif message.video:
        video_file_id = message.video.file_id
        message.caption = message.caption if message.caption else ''
        bot.send_video(message.chat.id, video_file_id, caption=message.caption, reply_markup=confirmation_markup)

#For admin approvement
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    # Extract message ID and action from callback data
    action, author_chat_id, message_id_in_author_chat = call.data.split(":")
    message = call.message  # Extract the message object
    if message:
        match action:
            case "user_post_approve":
                approved_from_user_message(bot, message, message_id_in_author_chat)
            case "user_post_decline":
                declined_from_user_message(bot, author_chat_id)
            case "user_post_anonymous":
                anonymous_from_user_message(bot, message, message_id_in_author_chat)
            case "admin_post_approve":
                send_approved_message(bot, message, author_chat_id, message_id_in_author_chat)
            case "admin_post_decline":
                send_declined_message(bot, message, author_chat_id, message_id_in_author_chat)
            case "admin_post_delay":
                send_delayed_message(bot, message, author_chat_id, message_id_in_author_chat)
        bot.edit_message_reply_markup(ADMIN_CHAT_ID, call.message.id, reply_markup=None)

# Enable bot to receive callback queries
bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

def delay_start():
    while True:
        schedule.run_pending()
        time.sleep(1)
@repeat(every(5).minutes)
def delay():
    poll_delayed_messages(bot)

Thread(target=delay_start).start()

bot.infinity_polling(timeout=10, long_polling_timeout = 5)