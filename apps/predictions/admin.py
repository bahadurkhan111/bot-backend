"""
Django admin configuration for predictions app.
"""
from django.contrib import admin
from .models import Team, Game, Prediction


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'sport', 'created_at']
    list_filter = ['sport']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at', 'gematria_values']
    
    actions = ['recalculate_gematria']
    
    def recalculate_gematria(self, request, queryset):
        """Admin action to recalculate gematria values for selected teams."""
        count = 0
        for team in queryset:
            team.calculate_gematria_values()
            count += 1
        self.message_user(request, f"Recalculated gematria for {count} team(s)")
    recalculate_gematria.short_description = "Recalculate gematria values"


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'date', 'status', 'actual_winner']
    list_filter = ['status', 'date']
    search_fields = ['team1__name', 'team2__name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Game Info', {
            'fields': ('team1', 'team2', 'date', 'status')
        }),
        ('Results', {
            'fields': ('actual_winner', 'team1_score', 'team2_score', 'notes')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = [
        'game',
        'predicted_winner',
        'signal',
        'confidence',
        'was_correct',
        'created_at'
    ]
    list_filter = ['signal', 'was_correct', 'created_at']
    search_fields = [
        'game__team1__name',
        'game__team2__name',
        'predicted_winner__name'
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
        'model_breakdown',
        'feature_vector'
    ]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Prediction', {
            'fields': ('game', 'predicted_winner', 'signal', 'confidence', 'model_consensus')
        }),
        ('Model Predictions', {
            'fields': (
                'lasso_prediction', 'lasso_vote',
                'xgboost_prediction', 'xgboost_vote',
                'linear_prediction', 'linear_vote',
                'model4_prediction', 'model4_vote',
            )
        }),
        ('Accuracy', {
            'fields': ('was_correct',)
        }),
        ('Technical Details', {
            'fields': ('feature_vector', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def model_breakdown(self, obj):
        """Display formatted model breakdown in admin."""
        breakdown = obj.model_breakdown
        return str(breakdown)
    model_breakdown.short_description = "Model Breakdown"
