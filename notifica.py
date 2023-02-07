import telebot
from decouple import config

token = config('TOKEN_BOT')

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    print(message)
    markup = telebot.types.InlineKeyboardMarkup()
    button_1 = telebot.types.InlineKeyboardButton("Comprar (testar bot)", callback_data="option_1")
    
    markup.add(button_1)
    bot.send_message(
        chat_id=message.chat.id,
        text="Olá, bem-vindo ao meu bot! Escolha uma opção:",
        reply_markup=markup
    )


    
bot.polling()