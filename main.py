import telebot
from telebot import types
from string import Template
from config import BOT_TOKEN, ADMIN_CHAT_ID, POST_SAMPLE, BOT_USERNAME, TARGET_CHANNEL_ID

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Welcome to bot! Send message!")

@bot.message_handler(content_types=["photo", "text"])
def handle_message(message):
    # Copy message content and send to admin with inline keyboard
    markup = types.InlineKeyboardMarkup()
    approve_button = types.InlineKeyboardButton("Approve", callback_data=f"approve:{message.message_id}")
    decline_button = types.InlineKeyboardButton("Decline", callback_data=f"decline:{message.message_id}")
    markup.add(approve_button, decline_button)

    if message.text:
        bot.send_message(ADMIN_CHAT_ID, message.text, reply_markup=markup)
    elif message.photo:
        # Handle photo message
        photo_file_id = message.photo[-1].file_id
        bot.send_photo(ADMIN_CHAT_ID, photo_file_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    # Extract message ID and action from callback data
    action, message_id = call.data.split(":")
    message = call.message  # Extract the message object

    if action == "approve":
        # Check if the message object exists
        if message:
            # Send approved message to channel
            bot.send_message(TARGET_CHANNEL_ID, message.text)
            # Notify user
            bot.send_message(message.chat.id, "Your message has been approved and sent to the channel.")
        else:
            bot.send_message(ADMIN_CHAT_ID, "Error: Message object is missing.")
    elif action == "decline":
        # Check if the message object exists
        if message:
            # Notify user
            bot.send_message(message.chat.id, "Your message has been declined.")
        else:
            bot.send_message(ADMIN_CHAT_ID, "Error: Message object is missing.")

# Enable bot to receive callback queries
bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

bot.polling()
