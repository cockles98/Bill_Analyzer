from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler

# Replace 'YOUR_BOT_TOKEN' with the token you obtained from BotFather
TOKEN = 'YOUR_BOT_TOKEN'

# States for the conversation
CHOOSING, TYPING_REPLY = range(2)

# Dictionary to store user data
user_data = {}

def start(update, context):
    update.message.reply_text("Hello! I'm your Options Bot. Send /options to get started.")
    return CHOOSING

def options(update, context):
    reply_keyboard = [['Option 1', 'Option 2', 'Option 3']]
    update.message.reply_text(
        "Choose an option:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )
    return TYPING_REPLY

def received_options(update, context):
    text = update.message.text
    user_data['choice'] = text
    update.message.reply_text(f"You chose: {text}. Now, what's your next move?")
    return CHOOSING

def cancel(update, context):
    user_data.clear()
    update.message.reply_text("Cancelled. Send /start to begin again.")
    return ConversationHandler.END

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [MessageHandler(Filters.regex('^(Option 1|Option 2|Option 3)$'), received_options)],
            TYPING_REPLY: [MessageHandler(Filters.text & ~Filters.command, received_options)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
