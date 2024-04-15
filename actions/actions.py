import time

from telebot import types
from config import TARGET_CHANNEL_ID, ADMIN_CHAT_ID, BOT_USERNAME
from string import Template
from config import POST_SAMPLE
from datetime import datetime


post_template = Template(POST_SAMPLE)

messages = {}

def send_approved_message(bot, message, author_chat_id, message_id_in_author_chat):
    if message.text:
        bot.send_message(TARGET_CHANNEL_ID, message.text)
    elif message.photo:
        bot.send_photo(TARGET_CHANNEL_ID, message.photo[-1].file_id, caption=message.caption)
    elif message.video:
        bot.send_video(TARGET_CHANNEL_ID, message.video.file_id, caption=message.caption)

    bot.send_message(author_chat_id, "🔥🔥Ваш пост был одобрен. Скоро он будет опубликован!", reply_to_message_id= message_id_in_author_chat)
    bot.send_message(message.chat.id, "Отправлено в канал", reply_to_message_id= message.id)
    print(f'Message with id {message.id} has sent to channel.')

def send_declined_message(bot, message, author_chat_id, message_id_in_author_chat):
    if message:
        bot.send_message(author_chat_id, "❌Ваш пост был отклонён.", reply_to_message_id=message_id_in_author_chat)

    bot.send_message(message.chat.id, "Отклонено", reply_to_message_id= message.id)
    print(f'Message with id {message.id} has been declined by admin.')

def send_delayed_message(bot, message, author_chat_id):
    bot.send_message(ADMIN_CHAT_ID, "Введите время отправки в формате дд.мм.гггг чч:мм:")
    bot.send_message(author_chat_id, "🔥🔥Ваш пост был одобрен. Скоро он будет опубликован!")
    target_message = message
    print(f'Message with id {message.id} was delayed. Ready to set the time')
    bot.register_next_step_handler(message, set_time, bot, target_message)

def set_time(message, bot, target_message):
    try:
        send_time = datetime.strptime(message.text, '%d.%m.%Y %H:%M')
        messages[message.id] = {'type': target_message.content_type, 'message': target_message, 'time': send_time}
        bot.send_message(ADMIN_CHAT_ID, f"Сообщение будет отправлено в {send_time}", reply_to_message_id=target_message.id)
        print(f'Message with id {target_message.id} was delayed until {send_time}')
    except ValueError:
        bot.send_message(ADMIN_CHAT_ID, "Некорректный формат даты. Попробуйте снова.")
        bot.register_next_step_handler(message, set_time, bot, target_message)

def approved_from_user_message(bot, message, message_id_in_author_chat):
    confirmation_markup = types.InlineKeyboardMarkup()
    approve_button = types.InlineKeyboardButton("✅Подтвердить", callback_data=f"admin_post_approve:{message.chat.id}:{message_id_in_author_chat}")
    decline_button = types.InlineKeyboardButton("❌Отклонить", callback_data=f"admin_post_decline:{message.chat.id}:{message_id_in_author_chat}")
    delay_button = types.InlineKeyboardButton("⏰Отложить", callback_data=f"admin_post_delay:{message.chat.id}:{message_id_in_author_chat}")
    confirmation_markup.add(approve_button, decline_button)
    confirmation_markup.add(delay_button)

    if message.text:
        text = f"{message.text}\n\n" + post_template.substitute(post_author=message.chat.username,
                                                                bot_username=BOT_USERNAME)
        bot.send_message(ADMIN_CHAT_ID, text, reply_markup=confirmation_markup)
        bot.send_message(message.chat.id, "Ваш пост успешно отправлен на рассмотрение!👍")
        print(f"Text message {message.text} from {message.chat.username} sent to admin-panel")
    elif message.photo:
        photo_file_id = message.photo[-1].file_id
        message.caption = message.caption if message.caption else ''
        caption = f"{message.caption}\n\n" + post_template.substitute(post_author=message.chat.username, bot_username=BOT_USERNAME)
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
    delay_button = types.InlineKeyboardButton("⏰Отложить", callback_data=f"admin_post_delay:{message.chat.id}:{message_id_in_author_chat}")
    confirmation_markup.add(approve_button, decline_button)
    confirmation_markup.add(delay_button)

    if message.text:
        text = f"{message.text}\n\n" + post_template.substitute(post_author="Аноним",
                                                                bot_username=BOT_USERNAME)
        bot.send_message(ADMIN_CHAT_ID, text, reply_markup=confirmation_markup)
        bot.send_message(message.chat.id, "Ваш пост успешно отправлен на рассмотрение!👍")
        print(f"Text message {message.text} from {message.from_user.username} sent to admin-panel anonymously")
    elif message.photo:
        photo_file_id = message.photo[-1].file_id
        message.caption = message.caption if message.caption else ''
        caption = f"{message.caption}\n\n" + post_template.substitute(post_author="Аноним",
                                                                      bot_username=BOT_USERNAME)
        bot.send_photo(ADMIN_CHAT_ID, photo_file_id, caption=caption, reply_markup=confirmation_markup)
        bot.send_message(message.chat.id, "Ваш пост успешно отправлен на рассмотрение!👍")
        print(f"Photo message {message.caption} from {message.from_user.username} sent to admin-panel anonymously")
    elif message.video:
        video_file_id = message.video.file_id
        message.caption = message.caption if message.caption else ''
        caption = f"{message.caption}\n\n" + post_template.substitute(post_author="Аноним",
                                                                      bot_username=BOT_USERNAME)
        bot.send_video(ADMIN_CHAT_ID, video_file_id, caption=caption, reply_markup=confirmation_markup)
        bot.send_message(message.chat.id, "Ваш пост успешно отправлен на рассмотрение!👍")
        print(f"Video message {message.caption} from {message.from_user.username} sent to admin-panel anonymously")


def declined_from_user_message(bot, author_chat_id):
    bot.send_message(author_chat_id, "Сообщение отменено. Жду новый вариант!")


def poll_delayed_messages(bot):
    print("Started polling delayed messages at ", time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime()))
    current_time = datetime.now()
    for item_id, data in messages.items():
        if data['time'] is not None and data['time'] <= current_time:
            print(f"Detected a message with id {item_id} that should be posted at {data['time']}")
            match data['type']:
                case 'text':
                    bot.send_message(TARGET_CHANNEL_ID, data['message'].text)
                case 'photo':
                    bot.send_photo(TARGET_CHANNEL_ID, data['message'].photo[-1].file_id, caption=data['message'].caption)
                case 'video':
                    bot.send_video(TARGET_CHANNEL_ID, data['message'].video.file_id, caption=data['message'].caption)
            print(f'Message with id {item_id} has sent to channel.')
            messages.pop(item_id)
            print(f'Message with id {item_id} deleted from the delay queue.')
            break
    print(f"Ended polling messages. {len(messages)} are in the queue now.")