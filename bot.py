"""
Bot functionality.

@Developer: Stan Ermokhin
@Version: 0.0.1
"""

import json
import sys
from typing import Any

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

import credentials
import database_control
import datamodel
import processing

START_MESSAGE_BEGINNING: str = "Hi "
HELP_MESSAGE: str = "This is a help message."
UNKNOWN_INPUT_RESPONSE: str = """Невалидный запос. Пример запроса:\n
{"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}"""
MAIN_HANDLE_FILTER: filters.MessageFilter | filters.BaseFilter = datamodel.MessageFilterJSON()
PROCESSING_APP: processing.MainApp = processing.MainApp()
DATABASE_APP: database_control.DatabaseControl = database_control.DatabaseControl()


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    chat_id: int = update.effective_chat.id
    user_name: str = f"{update.effective_user.first_name} {update.effective_user.last_name}"
    return await context.bot.send_message(chat_id=chat_id,
                                          text=f"{START_MESSAGE_BEGINNING}{user_name}!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    chat_id: int = update.effective_chat.id
    return await context.bot.send_message(chat_id=chat_id, text=HELP_MESSAGE)


async def main_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:

    _model_dict: dict[str, Any] = PROCESSING_APP.convert_request_json_to_valid_dict(
        update.message.text
    )

    values: dict[str, Any] = {"dt_from": None, "dt_upto": None, "group_type": None}
    for key in _model_dict:
        values[key] = PROCESSING_APP.unpack_value(_model_dict, key)

    result: str = json.dumps(DATABASE_APP.get_result(**values))

    chat_id: int = update.effective_chat.id
    return await context.bot.send_message(chat_id=chat_id, text=result)


async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    chat_id: int = update.effective_chat.id
    return await context.bot.send_message(chat_id=chat_id, text=UNKNOWN_INPUT_RESPONSE)


def main():
    # set Telegram bot
    application = ApplicationBuilder().token(credentials.TELEGRAM_API_TOKEN).build()

    # default commands
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))

    # main handler
    application.add_handler(MessageHandler(MAIN_HANDLE_FILTER, main_handler))

    # message handler to handle unknown commands or messages
    application.add_handler(MessageHandler(filters.ALL, unknown_message))

    # start the Telegram bot
    application.run_polling(poll_interval=3, timeout=30, connect_timeout=30)


if __name__ == "__main__":
    print("[START] Starting bot ...")
    main()
    print("[END] Stopping bot ...")
    sys.exit()
