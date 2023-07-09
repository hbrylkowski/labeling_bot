import os

from telegram import Update
from telegram.ext import (
    CommandHandler,
    ApplicationBuilder,
    ConversationHandler,
    CallbackContext,
    filters,
    MessageHandler,
)

from labeler.app.labeler import Application
from labeler.infra.e550w_printer.printer import E550W
from labeler.infra.renderer import PILRenderer


class LabelingBot:
    def __init__(self, app: Application):
        self.app = app

    async def media_info(self, update, context):
        media = self.app.get_installed_media()
        await update.message.reply_text(f"Installed media: {media.description}")

    async def label_length(self, update, context):
        await update.message.reply_text(
            "Hello! Please tell me the length of the label, enter 0 for auto:"
        )
        return LABEL_LENGTH

    async def label_text(self, update: Update, context: CallbackContext) -> int:
        user_input = update.message.text
        context.user_data["length"] = int(user_input)
        await update.message.reply_text("Now, please tell me the text of the label:")
        return LABEL_TEXT

    async def simple_label(self, update: Update, context: CallbackContext) -> int:
        user_input = update.message.text
        context.user_data["label"] = user_input
        try:
            label = self.app.print_label(
                text=context.user_data["label"], length=context.user_data["length"]
            )
        except Exception as e:
            await update.message.reply_text(f"There was an exception: {e}")
            return ConversationHandler.END

        await update.message.reply_photo(
            label.bytes, f'Your label is: {context.user_data["label"]}'
        )
        return ConversationHandler.END

    async def cancel(self, update: Update, context: CallbackContext) -> int:
        await update.message.reply_text("Cancelled.")
        return ConversationHandler.END


if __name__ == "__main__":
    application = Application(PILRenderer(), E550W(os.environ.get("PRINTER_IP")))
    bot = LabelingBot(application)

    LABEL_LENGTH, LABEL_TEXT = range(2)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("simple_label", bot.label_length)],
        states={
            LABEL_LENGTH: [
                MessageHandler(filters.Text() & ~filters.Command(), bot.label_text)
            ],
            LABEL_TEXT: [
                MessageHandler(filters.Text() & ~filters.Command(), bot.simple_label)
            ],
        },
        fallbacks=[CommandHandler("cancel", bot.cancel)],
    )

    app = ApplicationBuilder().token(os.environ["TELEGRAM_TOKEN"]).build()
    app.add_handler(CommandHandler("media_info", bot.media_info))
    app.add_handler(conv_handler)

    app.run_polling()
