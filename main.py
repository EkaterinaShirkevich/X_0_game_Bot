import random
from telegram import ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)

fld = list(range(1, 10))
x = chr(10060)
o = chr(11093)
count = 5
player = x
bot = o
CHOICE = 0


def show_field(field):
    txt = ''
    for i in range(len(field)):
        if not i % 3:
            txt += f'\n{"-" * 25}\n'
        txt += f'{field[i]:^8}'
    txt += f"\n{'-' * 25}"
    return txt


def check_win(field):
    win_coord = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
    n = [field[x[0]] for x in win_coord if field[x[0]] == field[x[1]] == field[x[2]]]
    return n[0] if n else n


def start(update, _):
    global fld, player, count
    fld = list(range(1, 10))
    count = 9
    player = x
    update.message.reply_text("Hi, let's play tic-tac-toe")
    update.message.reply_text(show_field(fld))
    update.message.reply_text(f'Go first {chr(10060)}')
    return CHOICE


def choice(update, _):
    global player, count, bot, fld
    move = update.message.text
    if not move.isdigit():
         update.message.reply_text(f"Incorrect input{chr(9940)}\nTry again")
    else:
        move = int(move)
        if move not in fld:
            update.message.reply_text(f"Incorrect input{chr(9940)}\nTry again")
        else:
            fld.insert(fld.index(move), player)
            fld.remove(move)
            update.message.reply_text(show_field(fld))
            if check_win(fld):
                update.message.reply_text(f"You're{player} - CHAMPION{chr(127942)}{chr(127881)}")
                return ConversationHandler.END
            count -= 1

            botmove = random.randint(1,9)
            while botmove not in fld:
                botmove = random.randint(1,9)
            update.message.reply_text(f'Ok... My choice is {botmove} ->')
            fld.insert(fld.index(botmove), bot)
            fld.remove(botmove)
            update.message.reply_text(f'{show_field(fld)}\n\n Your choice again')
            if check_win(fld):
                update.message.reply_text(f"I'm{bot} - CHAMPION{chr(127942)}{chr(127881)}")
                return ConversationHandler.END
            count -=1 

    if count == 0:
        update.message.reply_text(f"Draw {chr(129309)}")
        return ConversationHandler.END
    


def cancel(update, _):
    update.message.reply_text('Bye', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


if __name__ == '__main__':
    updater = Updater('HERE IS TOKEN')
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOICE: [MessageHandler(Filters.text, choice)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conv_handler)

    print('server start')

    updater.start_polling()
    updater.idle()