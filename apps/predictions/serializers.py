"""
DRF Serializers for predictions API.
"""
from rest_framework import serializers
from .models import Team, Game, Prediction


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model."""
    
    class Meta:
        model = Team
        fields = [
            'id',
            'name',
            'sport',
            'gematria_values',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'gematria_values']


class GameSerializer(serializers.ModelSerializer):
    """Serializer for Game model."""
    
    team1 = TeamSerializer(read_only=True)
    team2 = TeamSerializer(read_only=True)
    actual_winner = TeamSerializer(read_only=True)
    
    team1_id = serializers.IntegerField(write_only=True)
    team2_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Game
        fields = [
            'id',
            'team1',
            'team2',
            'team1_id',
            'team2_id',
            'date',
            'status',
            'actual_winner',
            'team1_score',
            'team2_score',
            'notes',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PredictionSerializer(serializers.ModelSerializer):
    """Serializer for Prediction model."""
    
    game = GameSerializer(read_only=True)
    predicted_winner = TeamSerializer(read_only=True)
    
    lasso_vote_name = serializers.CharField(source='lasso_vote.name', read_only=True)
    xgboost_vote_name = serializers.CharField(source='xgboost_vote.name', read_only=True)
    linear_vote_name = serializers.CharField(source='linear_vote.name', read_only=True)
    model4_vote_name = serializers.CharField(source='model4_vote.name', read_only=True)
    
    recommendation = serializers.CharField(source='get_recommendation', read_only=True)
    model_breakdown_detail = serializers.SerializerMethodField()
    
    class Meta:
        model = Prediction
        fields = [
            'id',
            'game',
            'predicted_winner',
            'signal',
            'confidence',
            'model_consensus',
            'lasso_prediction',
            'xgboost_prediction',
            'linear_prediction',
            'model4_prediction',
            'lasso_vote_name',
            'xgboost_vote_name',
            'linear_vote_name',
            'model4_vote_name',
            'feature_vector',
            'was_correct',
            'recommendation',
            'model_breakdown_detail',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_model_breakdown_detail(self, obj):
        """Get detailed model breakdown."""
        return obj.model_breakdown


class PredictionRequestSerializer(serializers.Serializer):
    """Serializer for prediction request."""
    
    team1 = serializers.CharField(
        max_length=100,
        help_text="Name of the first team"
    )
    team2 = serializers.CharField(
        max_length=100,
        help_text="Name of the second team"
    )
    sport = serializers.ChoiceField(
        choices=['NBA', 'NFL', 'MLB', 'NHL', 'SOCCER', 'OTHER'],
        default='NBA',
        help_text="Sport type"
    )
    
    def validate(self, data):
        """Validate that teams are different."""
        if data['team1'].lower() == data['team2'].lower():
            raise serializers.ValidationError("Teams must be different")
        return data


class PredictionResponseSerializer(serializers.Serializer):
    """Serializer for prediction response."""
    
    predicted_winner = serializers.CharField()
    signal = serializers.CharField()
    confidence = serializers.FloatField()
    model_consensus = serializers.FloatField()
    recommendation = serializers.CharField()
    
    model_breakdown = serializers.DictField(
        child=serializers.DictField()
    )
    
    game_id = serializers.IntegerField()
    prediction_id = serializers.IntegerField()
    
    team1 = TeamSerializer()
    team2 = TeamSerializer()


class PredictionStatsSerializer(serializers.Serializer):
    """Serializer for prediction statistics."""
    
    total_predictions = serializers.IntegerField()
    completed_games = serializers.IntegerField()
    correct_predictions = serializers.IntegerField()
    accuracy = serializers.FloatField()
    
    signal_breakdown = serializers.DictField(
        child=serializers.IntegerField()
    )
    
    bullish_accuracy = serializers.FloatField()
    bearish_accuracy = serializers.FloatField()
    neutral_accuracy = serializers.FloatField()
    
    avg_confidence = serializers.FloatField()
    avg_consensus = serializers.FloatField()


class PredictionCalculateSerializer(serializers.Serializer):
    """Serializer for formula calculation endpoint"""
    linear_output = serializers.FloatField(required=True, help_text="Linear Regression output (L)")
    day_of_month = serializers.IntegerField(min_value=1, max_value=31, help_text="Day of month (1-31)")
    game_date = serializers.DateField(required=False, allow_null=True, help_text="Game date (YYYY-MM-DD)")
    sport = serializers.CharField(max_length=50, default='NBA')
    
    def validate_day_of_month(self, value):
        if value < 1 or value > 31:
            raise serializers.ValidationError("Day must be between 1 and 31")
        return value


class PredictionCalculateResponseSerializer(serializers.Serializer):
    """Serializer for formula calculation response"""
    linear_output = serializers.FloatField()
    day_of_month = serializers.IntegerField()
    base_number = serializers.IntegerField()
    base_calculation = serializers.CharField()
    properties = serializers.ListField(
        child=serializers.DictField(),
        help_text="List of day properties used in calculation"
    )
    date_digit_sum = serializers.IntegerField(help_text="Sum of all date digits (MM/DD/YYYY)")
    game_date = serializers.CharField(allow_null=True, help_text="Game date in YYYY-MM-DD format")
    step_1_sum = serializers.FloatField(help_text="Base_Number + L + Date_Digit_Sum")
    step_2_divide = serializers.FloatField(help_text="Step 1 / 2")
    step_3_multiply = serializers.FloatField(help_text="Step 2 × 4")
    sport = serializers.CharField()
    sport_multiplier = serializers.FloatField()
    predicted_total = serializers.FloatField()
    formula_steps = serializers.ListField(
        child=serializers.CharField(),
        help_text="Step-by-step formula explanation"
    )
    formula_latex = serializers.CharField()


class PredictionAutoCalculateSerializer(serializers.Serializer):
    """Serializer for automatic prediction with team names"""
    team1 = serializers.CharField(max_length=100, help_text="First team name")
    team2 = serializers.CharField(max_length=100, help_text="Second team name")
    day_of_month = serializers.IntegerField(min_value=1, max_value=31, help_text="Day of month (1-31)")
    game_date = serializers.DateField(required=False, allow_null=True, help_text="Game date (YYYY-MM-DD)")
    sport = serializers.CharField(max_length=50, default='NBA')
    
    def validate_day_of_month(self, value):
        if value < 1 or value > 31:
            raise serializers.ValidationError("Day must be between 1 and 31")
        return value
    
    def validate(self, data):
        if data['team1'].lower() == data['team2'].lower():
            raise serializers.ValidationError("Teams must be different")
        return data
