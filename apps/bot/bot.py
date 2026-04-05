"""
Telegram bot setup and initialization.
"""
import logging
from telegram.ext import Application, CommandHandler
from django.conf import settings
from .handlers import (
    start_command,
    help_command,
    predict_command,
    compare_command,
    condensed_command,
    formula_command,
    sports_command,
    patterns_command,
    accuracy_command,
    status_command,
    history_command,
    error_handler,
)

logger = logging.getLogger(__name__)


def create_bot_application() -> Application:
    """
    Create and configure the Telegram bot application.
    
    Returns:
        Configured Application instance
    """
    if not settings.TELEGRAM_BOT_TOKEN:
        logger.warning("TELEGRAM_BOT_TOKEN not configured")
        return None
    
    # Create application
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    
    # Register command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("predict", predict_command))
    application.add_handler(CommandHandler("compare", compare_command))
    application.add_handler(CommandHandler("condensed", condensed_command))
    application.add_handler(CommandHandler("formula", formula_command))
    application.add_handler(CommandHandler("sports", sports_command))
    application.add_handler(CommandHandler("patterns", patterns_command))
    application.add_handler(CommandHandler("accuracy", accuracy_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("history", history_command))
    
    # Register error handler
    application.add_error_handler(error_handler)
    
    logger.info("Telegram bot application created")
    return application


def start_bot():
    """
    Start the Telegram bot.
    Should be called from a management command.
    """
    if not settings.TELEGRAM_ENABLED:
        logger.warning("Telegram bot is disabled in settings")
        return
    
    application = create_bot_application()
    
    if application is None:
        logger.error("Failed to create bot application")
        return
    
    logger.info("Starting Telegram bot...")
    application.run_polling(allowed_updates=True)
