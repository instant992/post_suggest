from telebot import types
from config import TARGET_CHANNEL_ID, ADMIN_CHAT_ID, BOT_USERNAME
from string import Template
from config import POST_SAMPLE

post_template = Template(POST_SAMPLE)

def send_approved_message(bot, message, author_chat_id, message_id_in_author_chat):
    if message.text:
        bot.send_message(TARGET_CHANNEL_ID, message.text)
    elif message.photo:
        bot.send_photo(TARGET_CHANNEL_ID, message.photo[-1].file_id, caption=message.caption)
    elif message.video:
        bot.send_video(TARGET_CHANNEL_ID, message.video.file_id, caption=message.caption)
    else:
        bot.send_message(ADMIN_CHAT_ID, "Error: Message object is missing.")

    bot.send_message(author_chat_id, "🔥🔥Ваш пост был одобрен и отправлен в канал! ", reply_to_message_id= message_id_in_author_chat)

def send_declined_message(bot, message, author_chat_id, message_id_in_author_chat):
    if message:
        bot.send_message(author_chat_id, "❌Ваш пост был отклонён.", reply_to_message_id=message_id_in_author_chat)
    else:
        bot.send_message(ADMIN_CHAT_ID, "Error: Message object is missing.")

def approved_from_user_message(bot, message, message_id_in_author_chat):
    confirmation_markup = types.InlineKeyboardMarkup()
    approve_button = types.InlineKeyboardButton("✅Подтвердить", callback_data=f"admin_post_approve:{message.chat.id}:{message_id_in_author_chat}")
    decline_button = types.InlineKeyboardButton("❌Отклонить", callback_data=f"admin_post_decline:{message.chat.id}:{message_id_in_author_chat}")
    confirmation_markup.add(approve_button, decline_button)

    if message.text:
        text = f"{message.text}\n\n" + post_template.substitute(post_author=message.chat.username,
                                                                bot_username=BOT_USERNAME)
        bot.send_message(ADMIN_CHAT_ID, text, reply_markup=confirmation_markup)
        bot.send_message(message.chat.id, "Ваш пост успешно отправлен на рассмотрение!👍")
        print(f"Text message {message.text} from {message.chat.username} sent to admin-panel")
    elif message.photo:
        photo_file_id = message.photo[-1].file_id
        message.caption = message.caption if message.caption else ''
        caption = f"{message.caption}\n\n" + post_template.substitute(post_author = message.chat.username, bot_username = BOT_USERNAME)
        bot.send_photo(ADMIN_CHAT_ID, photo_file_id, caption=caption, reply_markup=confirmation_markup)
        bot.send_message(message.chat.id, "Ваш пост успешно отправлен на рассмотрение!👍")
        print(f"Photo-message with caption {message.caption} from {message.chat.username} ")
    elif message.video:
        video_file_id = message.video.file_id
        message.caption = message.caption if message.caption else ''
        caption = f"{message.caption}\n\n" + post_template.substitute(post_author=message.chat.username,
                                                                      bot_username=BOT_USERNAME)
        bot.send_video(ADMIN_CHAT_ID, video_file_id, caption=caption, reply_markup=confirmation_markup)
        bot.send_message(message.chat.id, "Ваш пост успешно отправлен на рассмотрение!👍")
        print(f"Video-message with caption {message.caption} from {message.chat.username} ")


def anonymous_from_user_message(bot, message, message_id_in_author_chat):
    confirmation_markup = types.InlineKeyboardMarkup()
    approve_button = types.InlineKeyboardButton("✅Подтвердить", callback_data=f"admin_post_approve:{message.chat.id}:{message_id_in_author_chat}")
    decline_button = types.InlineKeyboardButton("❌Отклонить", callback_data=f"admin_post_decline:{message.chat.id}:{message_id_in_author_chat}")
    confirmation_markup.add(approve_button, decline_button)

    if message.text:
        text = f"{message.text}\n\n" + post_template.substitute(post_author="Аноним",
                                                                bot_username=BOT_USERNAME)
        bot.send_message(ADMIN_CHAT_ID, text, reply_markup=confirmation_markup)
        bot.send_message(message.chat.id, "Ваш пост успешно отправлен на рассмотрение!👍")
        print(f"Text message {message.text} from {message.from_user.username} sent to admin-panel")
    elif message.photo:
        photo_file_id = message.photo[-1].file_id
        message.caption = message.caption if message.caption else ''
        caption = f"{message.caption}\n\n" + post_template.substitute(post_author="Аноним",
                                                                      bot_username=BOT_USERNAME)
        bot.send_photo(ADMIN_CHAT_ID, photo_file_id, caption=caption, reply_markup=confirmation_markup)
        bot.send_message(message.chat.id, "Ваш пост успешно отправлен на рассмотрение!👍")
        print(f"Photo-message with caption {message.caption} ")
    elif message.video:
        video_file_id = message.video.file_id
        message.caption = message.caption if message.caption else ''
        caption = f"{message.caption}\n\n" + post_template.substitute(post_author="Аноним",
                                                                      bot_username=BOT_USERNAME)
        bot.send_video(ADMIN_CHAT_ID, video_file_id, caption=caption, reply_markup=confirmation_markup)
        bot.send_message(message.chat.id, "Ваш пост успешно отправлен на рассмотрение!👍")


def declined_from_user_message(bot, author_chat_id):
    bot.send_message(author_chat_id, "Сообщение отменено. Жду новый вариант!")

