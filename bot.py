import os
from dotenv import load_dotenv
import logging
from telegram import Update,  ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, ConversationHandler
import pandas as pd

##### config
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

##### For logging how the bot it's doing
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
