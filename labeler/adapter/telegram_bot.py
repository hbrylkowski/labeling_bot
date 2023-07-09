import os

from telegram.ext import CommandHandler, ApplicationBuilder

from labeler.app.labeler import Application
from labeler.infra.e550w_printer.printer import E550W
from labeler.infra.renderer import PILRenderer


class LabelingBot:
    def __init__(self, app):
        self.app = app

    async def media_info(self, update, context):
        media = self.app.get_installed_media()
        await update.message.reply_text(f"Installed media: {media.description}")


if __name__ == "__main__":
    application = Application(PILRenderer(), E550W(os.environ.get("PRINTER_IP")))
    bot = LabelingBot(application)

    app = ApplicationBuilder().token(os.environ["TELEGRAM_TOKEN"]).build()
    app.add_handler(CommandHandler("media_info", bot.media_info))

    app.run_polling()
