import telebot

def send_msg(msg):
    
    bot = telebot.TeleBot('Your_bot_api_token')
    chat_id = 'Your_chat_id_token'
    bot.send_message(chat_id, "使用者您好\n"+msg)

