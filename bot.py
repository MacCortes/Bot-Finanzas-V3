import os
from dotenv import load_dotenv
import logging
from telegram import Update,  ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, ConversationHandler
import pandas as pd

# Load enviromental variables
load_dotenv()

# Save bot token on variable
token = os.environ['BOT_TOKEN']
