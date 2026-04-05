"""
ChatBot Views for Sports Prediction System
Uses Groq (primary), Gemini (fallback), or OpenAI (last resort).
"""
import os
import re
import json
import logging
from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.http import StreamingHttpResponse

logger = logging.getLogger(__name__)


def _build_live_context(user_message: str) -> str:
    """Fetch real data relevant to the user's message and inject it as context."""
    context_parts = []
    msg_lower = user_message.lower()

    # Detect team matchup queries (e.g. "Lakers vs Rockets", "analyze celtics vs rockets")
    vs_pattern = re.search(
        r'(\b[A-Za-z]+)\s+(?:vs\.?|versus|against)\s+([A-Za-z]+)',
        user_message, re.IGNORECASE
    )

    if vs_pattern:
        team1 = vs_pattern.group(1).strip().title()
        team2 = vs_pattern.group(2).strip().title()

        # Detect sport from message
        sport = 'NBA'
        for s in ['NFL', 'MLB', 'NHL', 'WNBA', 'MLS', 'UFC']:
            if s.lower() in msg_lower:
                sport = s
                break

        today = datetime.now()
        day_of_month = today.day
        date_str = today.strftime('%Y-%m-%d')

        # Run actual formula calculation
        try:
            from apps.predictions.formula import apply_formula
            formula = apply_formula(
                linear_output=6.32,
                day_of_month=day_of_month,
                game_date=date_str,
                sport=sport
            )
            context_parts.append(
                f"\n## LIVE FORMULA RESULT for {team1} vs {team2} ({date_str}):\n"
                f"- Base_Number = {formula['base_number']} (day {day_of_month})\n"
                f"- L (linear output) = {formula['linear_output']}\n"
                f"- Date_Digit_Sum = {formula['date_digit_sum']} (from {date_str})\n"
                f"- Step 1: {formula['base_number']} + {formula['linear_output']} + {formula['date_digit_sum']} = {formula['step_1_sum']}\n"
                f"- Step 2: {formula['step_1_sum']} / 2 = {formula['step_2_divide']}\n"
                f"- Step 3: {formula['step_2_divide']} x 4 = {formula['step_3_multiply']}\n"
                f"- **Predicted Total = {formula['predicted_total']}**\n"
                f"- Sport multiplier: {formula.get('sport_multiplier', 1)}\n"
            )
        except Exception as e:
            logger.debug(f"Formula context error: {e}")

        # Get live scores if available
        try:
            from apps.predictions.sports_scraper import sports_scraper
            scores = sports_scraper.get_scores(sport)
            matching = [g for g in scores if
                        team1.lower() in g['team1'].lower() or team1.lower() in g['team2'].lower() or
                        team2.lower() in g['team1'].lower() or team2.lower() in g['team2'].lower()]
            if matching:
                g = matching[0]
                context_parts.append(
                    f"\n## LIVE SCORE DATA:\n"
                    f"- {g['team1']} ({g['team1_record']}) {g['score1']} vs {g['team2']} ({g['team2_record']}) {g['score2']}\n"
                    f"- Status: {g['status']}\n"
                )
        except Exception as e:
            logger.debug(f"Scores context error: {e}")

    # Fetch pattern data if user asks about patterns/accuracy
    if any(word in msg_lower for word in ['pattern', 'accuracy', 'stats', 'track']):
        try:
            from apps.predictions.pattern_recognition import pattern_tracker
            stats = pattern_tracker.get_accuracy_stats()
            context_parts.append(
                f"\n## LIVE PATTERN DATA:\n"
                f"- Total predictions: {stats['total_predictions']}\n"
                f"- Adjustment factor: {stats['adjustment_factor']}\n"
            )
        except Exception:
            pass

    # Fetch news gematria if user asks about news/headlines/gematria
    if any(word in msg_lower for word in ['news', 'headline', 'cnn', 'vatican', 'gematria signal']):
        try:
            from apps.predictions.news_scraper import news_scraper
            analysis = news_scraper.analyze_headlines('CNN', 5)
            key_nums = analysis.get('key_numbers', {})
            if key_nums:
                nums_str = ', '.join(f"{k}={v}" for k, v in key_nums.items())
                context_parts.append(
                    f"\n## LIVE CNN GEMATRIA KEY NUMBERS:\n{nums_str}\n"
                )
        except Exception:
            pass

    if context_parts:
        return (
            "\n\n---\nIMPORTANT: Use ONLY the following REAL DATA in your response. "
            "Do NOT make up or hallucinate any numbers. Use these exact values:\n"
            + '\n'.join(context_parts)
        )
    return ""

# Initialize AI clients — priority: Groq > Gemini > OpenAI
groq_client = None
gemini_model = None
openai_client = None
active_provider = None

groq_key = os.getenv('GROQ_API_KEY', '')
gemini_key = os.getenv('GEMINI_API_KEY', '')
openai_key = os.getenv('OPENAI_API_KEY', '')

if groq_key:
    try:
        from groq import Groq
        groq_client = Groq(api_key=groq_key)
        active_provider = 'groq'
        logger.info("Groq AI initialized (Llama 3.3 70B)")
    except Exception as e:
        logger.error(f"Failed to initialize Groq: {e}")

if gemini_key:
    try:
        import google.generativeai as genai
        genai.configure(api_key=gemini_key)
        gemini_model = genai.GenerativeModel('gemini-2.0-flash')
        if not active_provider:
            active_provider = 'gemini'
        logger.info("Gemini AI initialized")
    except Exception as e:
        logger.error(f"Failed to initialize Gemini: {e}")

if openai_key:
    try:
        from openai import OpenAI
        openai_client = OpenAI(api_key=openai_key)
        if not active_provider:
            active_provider = 'openai'
        logger.info("OpenAI initialized")
    except Exception as e:
        logger.error(f"Failed to initialize OpenAI: {e}")

SYSTEM_PROMPT = """You are an expert AI assistant for a sports prediction system that uses Machine Learning, Numerology (Gematria), and pattern recognition to predict outcomes across ALL sports markets.

## CURRENT FORMULA:
T = ((Base_Number + L + Date_Digit_Sum) / 2) x 4

Where:
- **T** = Predicted Total points for the game
- **Base_Number** = From day of month (1-31) using Gematrinator number properties
  - Based on geometric shapes (Triangular, Square, Tetrahedral, Pentagonal, Star, Cube)
  - Shapes multiplied by sides/faces (Triangle=3, Square=4, Cube=6, etc.)
  - Range: 4 to 78 depending on the day
- **L** = Linear Regression ML model output (adjusted by loss-aware system)
- **Date_Digit_Sum** = Sum of all digits in game date (MM/DD/YYYY)
  - Example: 01/14/2026 → 0+1+1+4+2+0+2+6 = 16

## NEWS GEMATRIA SIGNALS:
The system scrapes CNN and Vatican News headlines daily, runs them through 26 gematria calculators (ordinal, reduction, jewish, chaldean, etc.) to extract numerical signals. These numbers can be cross-referenced with game data for additional prediction accuracy.

## SUPPORTED SPORTS:
NBA, WNBA, NCAA Basketball, NFL, NCAA Football, MLB, NHL, MLS, Premier League, La Liga, Serie A, Bundesliga, Champions League, UFC/MMA, Euroleague, and more.

## PATTERN RECOGNITION:
The system tracks every prediction and learns from outcomes:
- Day-of-month accuracy patterns
- Sport-specific accuracy trends
- Win/loss streaks
- Over/under bias detection
- Base number correlation analysis

## LOSS-AWARE ADJUSTMENT:
When predictions are wrong, the system automatically adjusts:
- Tracks prediction errors over time
- Uses exponential moving average to correct systematic bias
- Learning rate decreases as more data is collected

## SPORTS DATA:
The system pulls live data from ESPN API and NBA.com CDN:
- Live scores and schedules for all major sports
- Team standings, records, and head coaches
- Recent game results

## YOUR CAPABILITIES:
1. Analyze ANY sports market the user asks about
2. Explain the prediction formula step by step
3. Discuss team matchups and provide insights
4. Explain pattern recognition findings
5. Help users understand when to bet and when to avoid
6. Compare predictions with Vegas lines
7. Provide sport-specific analysis and context
8. Explain gematria and numerological concepts
9. Analyze news headline gematria signals

## IMPORTANT:
- Be confident but honest about prediction limitations
- Sports betting involves risk - always note this
- Explain the math clearly when asked
- The system learns and improves over time through the loss-aware adjustment

Be helpful, knowledgeable, and thorough. Give actionable insights.
"""


def _stream_groq(user_message):
    """Stream response from Groq (Llama 3.3 70B)."""
    try:
        live_context = _build_live_context(user_message)
        stream = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT + live_context},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1500,
            stream=True
        )

        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                yield f"data: {json.dumps({'content': delta.content})}\n\n"

        yield f"data: {json.dumps({'done': True})}\n\n"

    except Exception as e:
        logger.error(f"Groq streaming error: {e}")
        yield f"data: {json.dumps({'content': 'Groq error: ' + str(e)})}\n\n"
        yield f"data: {json.dumps({'done': True})}\n\n"


def _stream_gemini(user_message):
    """Stream response from Gemini."""
    try:
        live_context = _build_live_context(user_message)
        response = gemini_model.generate_content(
            SYSTEM_PROMPT + live_context + "\n\n---\nUser: " + user_message,
            stream=True,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 1500,
            }
        )

        for chunk in response:
            if chunk.text:
                yield f"data: {json.dumps({'content': chunk.text})}\n\n"

        yield f"data: {json.dumps({'done': True})}\n\n"

    except Exception as e:
        logger.error(f"Gemini streaming error: {e}")
        yield f"data: {json.dumps({'content': 'Gemini error: ' + str(e)})}\n\n"
        yield f"data: {json.dumps({'done': True})}\n\n"


def _stream_openai(user_message):
    """Stream response from OpenAI."""
    try:
        live_context = _build_live_context(user_message)
        stream = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT + live_context},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1000,
            stream=True
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield f"data: {json.dumps({'content': chunk.choices[0].delta.content})}\n\n"

        yield f"data: {json.dumps({'done': True})}\n\n"

    except Exception as e:
        logger.error(f"OpenAI streaming error: {e}")
        yield f"data: {json.dumps({'content': 'OpenAI error: ' + str(e)})}\n\n"
        yield f"data: {json.dumps({'done': True})}\n\n"


@api_view(['POST'])
@permission_classes([AllowAny])
def chatbot_message(request):
    """
    Handle chatbot messages. Priority: Groq > Gemini > OpenAI.

    POST /api/bot/chat/
    Request: {"message": "How does the formula work?"}
    """
    try:
        user_message = request.data.get('message', '').strip()

        if not user_message:
            return Response(
                {'error': 'Message is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if groq_client:
            generator = _stream_groq(user_message)
        elif gemini_model:
            generator = _stream_gemini(user_message)
        elif openai_client:
            generator = _stream_openai(user_message)
        else:
            return Response(
                {
                    'response': 'ChatBot is not configured. Set GROQ_API_KEY, GEMINI_API_KEY, or OPENAI_API_KEY in .env',
                    'success': False
                },
                status=status.HTTP_200_OK
            )

        response = StreamingHttpResponse(generator, content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        return response

    except Exception as e:
        logger.error(f"ChatBot error: {str(e)}")
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def chatbot_info(request):
    """
    Get chatbot configuration info.

    GET /api/bot/info/
    """
    models = {
        'groq': 'llama-3.3-70b-versatile',
        'gemini': 'gemini-2.0-flash',
        'openai': 'gpt-4o-mini',
    }

    return Response({
        'model': models.get(active_provider, 'none'),
        'provider': active_provider or 'none',
        'configured': active_provider is not None,
        'formula': 'T = ((Base_Number + L + Date_Digit_Sum) / 2) x 4',
        'status': 'active' if active_provider else 'not_configured'
    })
