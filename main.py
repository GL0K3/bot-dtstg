"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os

import httpx
from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(
    update: Update, context: ContextTypes.DEFAULT_TYPE, whitelist: list | None = None
) -> None:
    """Send a message when the command /start is issued."""
    user_id = update.effective_user.id
    match whitelist:
        case None:
            pass
        case filled_list:
            if user_id not in filled_list:
                await update.message.reply_text(
                    "Sorry, you are not authorized to use this bot."
                )
                return
    await update.message.reply_text("Welcome! You are authorized to use this bot.")
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def give_ip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    ans = httpx.get("http://eth0.me")
    await update.message.reply_text("Your specified machine ip {}".format(ans.text))


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


def run(token: str, whitelist: list | None = None) -> None:
    """Start the bot."""

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    async def start_(*args, **kwargs):
        return await start(*args, **kwargs, whitelist=whitelist)

    application.add_handler(CommandHandler("start", start_))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ip", give_ip))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    match os.getenv("WHITELIST"), os.getenv("TOKEN"):
        case str(whitelist), str(token):
            whitelist = list(map(int, whitelist.split(",")))
            print("Using whitelist {}".format(whitelist))
            print("Using token {}...{}".format(token[:5], token[-5:]))
            run(whitelist=whitelist, token=token)
        case None, str(token):
            print("Specify $WHITELIST dummy!")
        case list(whitelist), None:
            print("Specify $TOKEN dummy!")
        case None, None:
            print("Cringe, specify in environment $WHITELIST and $TOKEN")
        case _:
            print("I dont know what you did, but it is not expected!")
