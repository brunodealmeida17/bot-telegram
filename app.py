from flask import Flask
import telebot, csv
from decouple import config
from telebot.types import LabeledPrice
import os

app = Flask(__name__)

token = config('TOKEN_BOT')
token_provider = config('TOKEN_PROVIDER_TEST')

bot = telebot.TeleBot(token)

precos = [    
    LabeledPrice(label="Curriculo para analise", amount=600),
    
    
]


def salvarid(id_telegram):
    with open('ids_telegram.csv', 'a') as ids:
        e = csv.writer(ids)
        e.writerow([id_telegram])

@bot.message_handler(commands=['start'])
def start_message(message):
    salvarid(message.from_user.id)
    
    markup = telebot.types.InlineKeyboardMarkup()
    button_1 = telebot.types.InlineKeyboardButton("Comprar (testar bot)", callback_data="option_1")
    
    markup.add(button_1)
    bot.send_message(
        chat_id=message.chat.id,
        text="Olá, bem-vindo ao meu bot! Escolha uma opção:",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):    
    if call.data == "option_1":
        bot.answer_callback_query(
            callback_query_id=call.id,
        )
        bot.send_message(
            chat_id=call.message.chat.id,
            text="Opção comprar  escolhida. Algumas informações",
        )
        bot.send_invoice(
            chat_id=call.message.chat.id,
            title='Robo de vendas no telegram',
            description='criação de um bot de vendas no telegram',
            provider_token=token_provider,
            currency='BRL',
            is_flexible=False,
            prices=precos,
            invoice_payload='PAYLOAD'

        )
        

@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(
        pre_checkout_query.id, ok=True, error_message="Falha em processar o pagamento, tente em instantes"
    )

@bot.message_handler(content_types=['successful_payment'])
def documento(message):
    markup = telebot.types.InlineKeyboardMarkup()
    button_1 = telebot.types.InlineKeyboardButton("baixar documento", callback_data="option_2")
    
    markup.add(button_1)
    bot.send_message(
        chat_id=message.chat.id,
        text="Oba, agradeço o interesse ate aqui, baixe seu documento na opção abaixo:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    doc = open('Bruno_de Almeida Miranda.pdf', "rb")
    if call.data == "option_2":
        bot.answer_callback_query(
            callback_query_id=call.id,
        )        
       
        bot.send_document(chat_id=call.message.chat.id, document=doc)

    
bot.polling(none_stop=True, interval=0)

@app.route("/")
def hello():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True)
