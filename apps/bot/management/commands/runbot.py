"""
Django management command to run the Telegram bot.
"""
import logging
from django.core.management.base import BaseCommand
from apps.bot.bot import create_bot_application

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Run the Telegram Sports Prediction Bot'

    def handle(self, *args, **options):
        """Execute the command."""
        self.stdout.write(self.style.SUCCESS('Starting Telegram Bot...'))
        
        try:
            # Create bot application
            application = create_bot_application()
            
            if application is None:
                self.stdout.write(
                    self.style.ERROR(
                        'Failed to create bot application. '
                        'Check that TELEGRAM_BOT_TOKEN is set in .env'
                    )
                )
                return
            
            # Log bot info
            self.stdout.write(
                self.style.SUCCESS(
                    f'Bot started successfully!\n'
                    f'Commands available:\n'
                    f'  /start - Welcome message\n'
                    f'  /help - Show help\n'
                    f'  /predict L=<value> day=<day> sport=<sport>\n'
                    f'  /compare prediction=<value> vegas=<line>\n'
                    f'  /condensed <day>\n'
                    f'  /formula - Show formula explanation\n'
                    f'  /sports - Show sport multipliers\n'
                )
            )
            
            # Run bot (blocking)
            application.run_polling()
            
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\nBot stopped by user'))
        except Exception as e:
            logger.error(f"Error running bot: {e}", exc_info=True)
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
