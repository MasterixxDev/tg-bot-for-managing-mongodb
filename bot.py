import telebot
from pymongo import MongoClient

API_TOKEN = 'you can get the token in BotFather ;)'

client = MongoClient('localhost')
db = client['db']
accounts = db['acc']
linked_accounts = db['linked']

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "To manage the bot and database, use the /Gems and /vip commands")

@bot.message_handler(commands=['Gems'])
def give_gems(message):
    try:
        args = message.text.split()

        if len(args) != 3:
            bot.reply_to(message, "Please use the format: /Gems <LowID> <amount>")
            return
        
        low_id = int(args[1])  # ID
        gems_to_add = int(args[2]) #Gems added

        user = accounts.find_one({'lowID': low_id})

        if user:
        
            new_gems = user.get('gems', 0) + gems_to_add
            accounts.update_one({'lowID': low_id}, {'$set': {'gems': new_gems}})
            bot.reply_to(message, f'User with LowID {low_id} has {gems_to_add} Gems added! Now he has {new_gems} Gems.')
        else:
            #i don't know, trash code :)
            accounts.insert_one({'lowID': low_id, 'gems': gems_to_add})
            bot.reply_to(message, f'user with LowID {low_id} received {gems_to_add}')

    except ValueError:
        bot.reply_to(message, "Please make sure LowID and Gems count are integers.")

@bot.message_handler(commands=['vip'])
def set_vip(message):
    try:
        
        args = message.text.split()

        if len(args) != 2:
            bot.reply_to(message, "Please use the format: /vip <LowID>")
            return
        
        low_id = int(args[1])

        user = accounts.find_one({'lowID': low_id})

        if user:

            accounts.update_one({'lowID': low_id}, {'$set': {'vip': 1}})
            bot.reply_to(message, f'user with LowID {low_id} Now VIP!')
        else:
            bot.reply_to(message, f'user with LowID {low_id} not found.')

    except ValueError:
        bot.reply_to(message, "Please make sure LowID is an integer.")


if __name__ == '__main__':
    bot.polling(none_stop=True)
