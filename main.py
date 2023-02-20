from flask import Flask, request
import telebot
import os
import openai


app = Flask(__name__)
TOKEN = os.environ.get("TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
bot = telebot.TeleBot(TOKEN)
openai.api_key = OPENAI_API_KEY

@bot.message_handler(commands=['start'])
def message_start(message):
    bot.send_message(message.chat.id, f'Привіт, {message.from_user.username}!\nПоспілкуємось?')

@bot.message_handler(func=lambda _: True)
def handle_message(message):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message.text,
        temperature=0.5,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
    )
    bot.send_message(chat_id=message.from_user.id, text=response['choices'][0]['text'])


@app.route("/" + TOKEN, methods=["POST"])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "Python Telegram Bot", 200


@app.route("/")
def main():
    bot.remove_webhook()
    bot.set_webhook(url="https://itgen-gpt-bot.herokuapp.com/" + TOKEN)
    return "Python Telegram Bot", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
