import telebot
from telebot import types
from string import Template
from config import BOT_TOKEN, ADMIN_CHAT_ID, POST_SAMPLE, BOT_USERNAME, TARGET_CHANNEL_ID

bot = telebot.TeleBot(BOT_TOKEN)

post_template = Template(POST_SAMPLE)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Welcome to bot! Send message!")

@bot.message_handler(content_types=["photo", "text", "video"])
def handle_message(message):
    # Copy message content and send to admin with inline keyboard
    markup = types.InlineKeyboardMarkup()
    approve_button = types.InlineKeyboardButton("Approve", callback_data=f"approve:{message.message_id}:{message.chat.id}")
    decline_button = types.InlineKeyboardButton("Decline", callback_data=f"decline:{message.message_id}:{message.chat.id}")
    markup.add(approve_button, decline_button)

    if message.text:
        text = f"{message.text}\n\n" + post_template.substitute(post_author=message.from_user.username, bot_username = BOT_USERNAME)
        bot.send_message(ADMIN_CHAT_ID, text, reply_markup=markup)
        bot.send_message(message.chat.id, "Ваш пост успешно отправлен на рассмотрение!")
    elif message.photo:
        photo_file_id = message.photo[-1].file_id
        caption = f"{message.caption}\n\n" + post_template.substitute(post_author = message.from_user.username, bot_username = BOT_USERNAME)
        bot.send_photo(ADMIN_CHAT_ID, photo_file_id, caption=caption, reply_markup=markup)
        bot.send_message(message.chat.id, "Ваш пост успешно отправлен на рассмотрение!")
    elif message.video:
        video_file_id = message.video.file_id
        caption = f"{message.caption}\n\n" + post_template.substitute(post_author=message.from_user.username, bot_username=BOT_USERNAME)
        bot.send_video(ADMIN_CHAT_ID, video_file_id, caption=caption, reply_markup=markup)
        bot.send_message(message.chat.id, "Ваш пост успешно отправлен на рассмотрение!")

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    # Extract message ID and action from callback data
    action, message_id, author_chat_id = call.data.split(":")
    message = call.message  # Extract the message object

    if action == "approve":
        # Check if the message object exists
        if message.text:
            # Send approved message to channel
            bot.send_message(TARGET_CHANNEL_ID, message.text)
        elif message.photo:
            bot.send_photo(TARGET_CHANNEL_ID, message.photo[-1].file_id, caption=message.caption)
        elif message.video:
            bot.send_video(ADMIN_CHAT_ID, message.video_file_id, caption=message.caption)
        else:
            bot.send_message(ADMIN_CHAT_ID, "Error: Message object is missing.")
        bot.edit_message_reply_markup(ADMIN_CHAT_ID, call.message.id, reply_markup=None)
        bot.send_message(author_chat_id, "Your message has been approved and sent to the channel.")

    elif action == "decline":
        # Check if the message object exists
        if message:
            # Notify user
            bot.send_message(author_chat_id, "Your message has been declined.")
        else:
            bot.send_message(ADMIN_CHAT_ID, "Error: Message object is missing.")

        bot.edit_message_reply_markup(ADMIN_CHAT_ID, call.message.id, reply_markup=None)

# Enable bot to receive callback queries
bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

bot.polling()
