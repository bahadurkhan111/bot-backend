"""
Telegram bot handlers for sports predictions.
"""
import logging
from datetime import datetime, date
from telegram import Update
from telegram.ext import ContextTypes
from apps.predictions.services import PredictionService
from apps.predictions.formula import (
    apply_formula,
    get_pd_value,
    calculate_date_digit_sum,
    SPORT_MULTIPLIERS
)

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    welcome_message = """
🏀 **Sports Prediction Bot** 🏈⚾🏒

Welcome! I use ML models + numerology (gematria) to predict sports outcomes.

**Formula:** T = ((Base_Number + L + Date_Digit_Sum) / 2) x 4

**Commands:**
/predict - Make a prediction
/compare - Compare with Vegas line
/condensed <day> - View Base Number for a day
/formula - View formula explanation
/sports - View sport multipliers
/patterns - View detected patterns
/accuracy - View prediction accuracy
/help - Show this help

**Examples:**
/predict L=6.32 day=14 date=01/14/2026 sport=NBA
/compare prediction=52.64 vegas=219.5
/condensed 14
    """
    await update.message.reply_text(welcome_message, parse_mode='Markdown')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    help_text = """
**Available Commands:**

🎯 /predict L=<val> day=<day> sport=<sport> date=<MM/DD/YYYY>
   Calculate prediction using the formula
   Example: /predict L=6.32 day=14 sport=NBA date=01/14/2026

⚖️ /compare prediction=<val> vegas=<line>
   Compare prediction with Vegas line
   Example: /compare prediction=52.64 vegas=219.5

📅 /condensed <day>
   View Base Number for a specific day (1-31)
   Example: /condensed 14

📐 /formula
   Full formula explanation

🏆 /sports
   View all sport multipliers

📊 /patterns
   View detected prediction patterns

📈 /accuracy
   View prediction accuracy stats

❓ /help
   Show this help

**Discrepancy Classification:**
🟢 NORMAL (<20): Safe to bet
🟡 CAUTION (20-50): Proceed with caution
🔴 EXTREME (>50): DO NOT BET
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def predict_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /predict command with new formula."""
    if not context.args:
        await update.message.reply_text(
            "❌ Please provide parameters:\n"
            "/predict L=<val> day=<day> sport=<sport> date=<MM/DD/YYYY>\n\n"
            "Example: /predict L=6.32 day=14 sport=NBA date=01/14/2026"
        )
        return

    # Parse arguments
    params = {}
    for arg in context.args:
        if '=' in arg:
            key, value = arg.split('=', 1)
            params[key.upper()] = value

    # Validate required parameters
    if 'L' not in params or 'DAY' not in params or 'SPORT' not in params:
        await update.message.reply_text(
            "❌ Missing required parameters:\n"
            "L=<val> day=<day> sport=<sport>\n\n"
            "Example: /predict L=6.32 day=14 sport=NBA date=01/14/2026"
        )
        return

    try:
        L = float(params['L'])
        day = int(params['DAY'])
        sport = params['SPORT'].upper()

        # Validate day range
        if day < 1 or day > 31:
            await update.message.reply_text("❌ Day must be between 1 and 31")
            return

        # Parse optional date
        game_date = None
        if 'DATE' in params:
            try:
                game_date = datetime.strptime(params['DATE'], '%m/%d/%Y').date()
            except ValueError:
                game_date = date.today()
        else:
            game_date = date.today()

        # Get Base Number
        base_number = get_pd_value(day)
        if base_number is None:
            await update.message.reply_text(f"❌ No Base Number available for day {day}")
            return

        # Calculate prediction using new formula
        result_dict = apply_formula(L, day, game_date=game_date, sport=sport)
        result = result_dict['predicted_total']
        date_digit_sum = result_dict['date_digit_sum']

        # Build step breakdown
        step1 = base_number + L + date_digit_sum
        step2 = step1 / 2
        step3 = step2 * 4

        response = f"""
┌─────────────────────────────────────────┐
│   SPORTS PREDICTION CALCULATOR          │
├─────────────────────────────────────────┤
│ Date: {game_date.strftime('%B %d, %Y') if game_date else datetime.now().strftime('%B %d, %Y')}
│ Day of month: {day}
│ Sport: {sport}
│
│ INPUTS:
│ • Linear Regression (L): {L}
│ • Base Number: {base_number}
│ • Date Digit Sum: {date_digit_sum}
│
│ FORMULA: T = ((Base + L + DateSum) / 2) x 4
│
│ CALCULATION:
│ Step 1: {base_number} + {L} + {date_digit_sum} = {step1:.2f}
│ Step 2: {step1:.2f} / 2 = {step2:.2f}
│ Step 3: {step2:.2f} x 4 = {step3:.2f}
│
│ PREDICTION: {result:.2f} points
└─────────────────────────────────────────┘
        """

        await update.message.reply_text(response)

        # Log prediction for pattern tracking
        try:
            from apps.predictions.pattern_recognition import pattern_tracker
            pattern_tracker.log_prediction(
                sport=sport,
                day=day,
                predicted_total=result,
                linear_output=L,
                base_number=base_number,
                date_digit_sum=date_digit_sum,
                game_date=str(game_date) if game_date else None
            )
        except Exception:
            pass  # Pattern tracking is optional

    except ValueError as e:
        await update.message.reply_text(f"❌ Error in values: {str(e)}")
    except Exception as e:
        logger.error(f"Error in predict command: {e}", exc_info=True)
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def compare_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /compare command to compare prediction with Vegas line."""
    if not context.args:
        await update.message.reply_text(
            "❌ Please provide parameters:\n"
            "/compare prediction=<val> vegas=<line>\n\n"
            "Example: /compare prediction=52.64 vegas=219.5"
        )
        return

    params = {}
    for arg in context.args:
        if '=' in arg:
            key, value = arg.split('=', 1)
            params[key.lower()] = value

    if 'prediction' not in params or 'vegas' not in params:
        await update.message.reply_text(
            "❌ Missing required parameters:\n"
            "prediction=<val> vegas=<line>\n\n"
            "Example: /compare prediction=52.64 vegas=219.5"
        )
        return

    try:
        prediction = float(params['prediction'])
        vegas = float(params['vegas'])
        discrepancy = abs(prediction - vegas)

        if discrepancy < 20:
            level, emoji, signal = "NORMAL", "🟢", "SAFE"
            recommendation = "Safe to bet based on analysis"
        elif discrepancy < 50:
            level, emoji = "CAUTION", "🟡"
            signal = "BULLISH" if prediction < vegas else "BEARISH"
            recommendation = "Proceed with caution"
        else:
            level, emoji, signal = "EXTREME", "🔴", "DO NOT BET"
            recommendation = "Discrepancy too large - possible Vegas adjustment"

        analysis = 'Vegas seems adjusted' if discrepancy > 50 else 'Prediction aligned with Vegas' if discrepancy < 20 else 'Moderate difference'

        response = f"""
┌─────────────────────────────────────────┐
│      VEGAS COMPARISON                   │
├─────────────────────────────────────────┤
│ Your Prediction: {prediction} points
│ Vegas O/U Line: {vegas} points
│ Discrepancy: {discrepancy:.2f} points
│
│ {emoji} {level}
│
│ Signal: {signal}
│ Recommendation: {recommendation}
│
│ Analysis: {analysis}
└─────────────────────────────────────────┘
        """

        await update.message.reply_text(response)

    except ValueError as e:
        await update.message.reply_text(f"❌ Error in values: {str(e)}")
    except Exception as e:
        logger.error(f"Error in compare command: {e}", exc_info=True)
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def condensed_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /condensed command to show Base Number for a day."""
    if not context.args:
        await update.message.reply_text(
            "❌ Please provide a day (1-31):\n"
            "/condensed <day>\n\n"
            "Example: /condensed 14"
        )
        return

    try:
        day = int(context.args[0])

        if day < 1 or day > 31:
            await update.message.reply_text("❌ Day must be between 1 and 31")
            return

        base_number = get_pd_value(day)

        if base_number is None:
            await update.message.reply_text(f"❌ No Base Number available for day {day}")
            return

        from apps.number_properties.models import NumberProperty
        try:
            num_prop = NumberProperty.objects.get(day_of_month=day)
            source = num_prop.primary_sequence or "Gematrinator"
        except NumberProperty.DoesNotExist:
            source = "CSV Data"

        response = f"""
📅 **Day {day}: Base Number = {base_number}**

Source: {source}

This value is used in the formula:
T = ((Base_Number + L + Date_Digit_Sum) / 2) x 4
        """

        await update.message.reply_text(response, parse_mode='Markdown')

    except ValueError:
        await update.message.reply_text("❌ Day must be a number between 1 and 31")
    except Exception as e:
        logger.error(f"Error in condensed command: {e}", exc_info=True)
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def formula_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /formula command to show formula explanation."""
    response = """
📐 **PREDICTION FORMULA**

**T = ((Base_Number + L + Date_Digit_Sum) / 2) x 4**

**Components:**

• **T** = Predicted total points
• **Base_Number** = From day properties (geometric shapes x sides)
• **L** = Linear Regression ML model output
• **Date_Digit_Sum** = Sum of all date digits (MM/DD/YYYY)

**Calculation Process:**

1. Get Base_Number from day properties
2. Get Date_Digit_Sum from game date
3. Sum = Base_Number + L + Date_Digit_Sum
4. Divide by 2
5. Multiply by 4
6. Result = T (predicted total)

**Example: Day 7 on 01/14/2026, NBA**
• Base_Number = 4 (from day 7 properties)
• L = 6.32 (ML model)
• Date_Digit_Sum = 16 (0+1+1+4+2+0+2+6)

1. Sum = 4 + 6.32 + 16 = 26.32
2. 26.32 / 2 = 13.16
3. 13.16 x 4 = 52.64 points

Use /sports for sport multipliers
Use /condensed <day> for Base Numbers
    """

    await update.message.reply_text(response, parse_mode='Markdown')


async def sports_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /sports command to show sport multipliers."""
    response = """
🏆 **SPORT MULTIPLIERS**

**Basketball:**
• NBA: 1.15
• WNBA: 1.15
• NCAA Basketball: 1.15
• Euroleague: 1.15

**Football:**
• NFL: 1.06
• NCAA Football: 1.06

**Baseball:**
• MLB: 0.90
• NCAA Baseball: 0.90

**Hockey:**
• NHL: 1.20
• NCAA Hockey: 1.20

**Soccer:**
• MLS: 1.10
• Premier League: 1.10
• La Liga: 1.10
• Serie A: 1.10
• Bundesliga: 1.10
• Ligue 1: 1.10
• Champions League: 1.10

**UFC/MMA:**
• UFC: 1.25
• UFC Title Fight: 1.25

**Default:** 1.15

Formula: T = ((Base_Number + L + Date_Digit_Sum) / 2) x 4
    """

    await update.message.reply_text(response, parse_mode='Markdown')


async def patterns_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /patterns command to show detected patterns."""
    try:
        from apps.predictions.pattern_recognition import pattern_tracker
        patterns = pattern_tracker.get_patterns_summary()

        if not patterns['patterns']:
            await update.message.reply_text(
                "📊 **Pattern Recognition**\n\n"
                "No patterns detected yet. Make more predictions to build pattern data.\n\n"
                f"Total predictions tracked: {patterns['total_predictions']}\n"
                f"Accuracy rate: {patterns['accuracy_rate']:.1f}%",
                parse_mode='Markdown'
            )
            return

        response = "📊 **Detected Patterns:**\n\n"
        for p in patterns['patterns'][:10]:
            response += f"• {p['description']}\n"

        response += f"\nTotal tracked: {patterns['total_predictions']}"
        response += f"\nAccuracy: {patterns['accuracy_rate']:.1f}%"
        response += f"\nLoss adjustment active: {'Yes' if patterns.get('loss_adjustment_active') else 'No'}"

        await update.message.reply_text(response, parse_mode='Markdown')

    except Exception as e:
        logger.error(f"Error in patterns command: {e}", exc_info=True)
        await update.message.reply_text("📊 Pattern recognition is initializing. Make predictions first.")


async def accuracy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /accuracy command to show prediction stats."""
    try:
        from apps.predictions.pattern_recognition import pattern_tracker
        stats = pattern_tracker.get_accuracy_stats()

        response = f"""
📈 **Prediction Accuracy Report**

Total Predictions: {stats['total']}
Correct: {stats['correct']}
Incorrect: {stats['incorrect']}
Pending: {stats['pending']}

Overall Accuracy: {stats['accuracy']:.1f}%

By Sport:
"""
        for sport, sport_stats in stats.get('by_sport', {}).items():
            response += f"  {sport}: {sport_stats['accuracy']:.1f}% ({sport_stats['total']} predictions)\n"

        response += f"\nLoss Adjustment Factor: {stats.get('adjustment_factor', 1.0):.3f}"
        response += f"\nStreak: {stats.get('streak', 'N/A')}"

        await update.message.reply_text(response, parse_mode='Markdown')

    except Exception as e:
        logger.error(f"Error in accuracy command: {e}", exc_info=True)
        await update.message.reply_text("📈 Accuracy tracking is initializing. Make predictions first.")


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command."""
    await update.message.reply_text(
        "Use these commands instead:\n"
        "/predict - For predictions\n"
        "/compare - Compare with Vegas\n"
        "/patterns - View patterns\n"
        "/accuracy - View accuracy\n"
        "/help - View all commands"
    )


async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /history command."""
    await update.message.reply_text(
        "Use these commands instead:\n"
        "/predict - For predictions\n"
        "/compare - Compare with Vegas\n"
        "/patterns - View patterns\n"
        "/accuracy - View accuracy\n"
        "/help - View all commands"
    )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors."""
    logger.error(f"Update {update} caused error {context.error}")
