import os
from dotenv import load_dotenv
from auxiliar import *
import logging
from telegram import Update,  ReplyKeyboardMarkup, ReplyKeyboardRemove, bot_api_version
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, ConversationHandler
import pandas as pd
import locale

##### config

# Language: spanish (Mexico) "es-MX" 
locale.setlocale(locale.LC_ALL, 'es-MX') 

# formatting the float columns as currency
pd.options.display.float_format = '${:,.2f}'.format

# Load enviromental variables
load_dotenv()

# Save bot token on variable
token = os.environ['BOT_TOKEN']

##### files
# read the csv
transactions = pd.read_csv('db/movimientos.csv', encoding='utf-8')
accounts = pd.read_csv('db/cuentas.csv', encoding='utf-8')

# fix format of "Cantidad" column
transactions['Cantidad'] = transactions['Cantidad'].replace('[^-.0-9]', '', regex=True).astype(float)
# transform column "Fecha" to datetime
transactions["Fecha"]= pd.to_datetime(transactions["Fecha"])

##### For logging how the bot it's doing
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

#############################################
# Bot
#############################################

##### Handler functions

### command: /hello
def hello(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi, I'm your financial bot, I'll help you keep track of your expenses!")

### instruction: last n (ex: last 10)
def last_n(update: Update, context: CallbackContext):
    """Generates an image with the last n transactions"""
    msg = update.message.text
    cols = ["Tipo", "Cuenta", "Fecha", "Cantidad", "Descripción"]

    try:
        n = min(int(msg.split()[1]), transactions.shape[0])
        trans_n = transactions[cols].tail(n)
        trans_n["Fecha"] = trans_n["Fecha"].dt.strftime('%d %B %Y')
        saves_png(trans_n, 'last_n', 'img/')
        update.message.bot.send_photo(chat_id=update.effective_chat.id, photo=open('img/last_n.png', 'rb'))
    except ValueError:
        update.message.reply_text("Sorry, there was a problem with the number of rows. Please, try again!")
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="There was an error, we'll work into it")


##### Bot configuration

### updater
upd = Updater(token=token, use_context=True)

### dispatcher
disp = upd.dispatcher

### add handlers to the dispatcher
disp.add_handler(CommandHandler('hello', hello))
disp.add_handler(MessageHandler(Filters.regex('^(L|l)ast *') & (~Filters.command), last_n))

### start polling
upd.start_polling()

print('Bot running')

upd.idle()

print('End')