from django import forms
from .models import Tournament


GAME_CHOICES = [
    ('valorant', 'Valorant'),
    ('pubg',     'PUBG'),
]


class TournamentForm(forms.ModelForm):

    # multiple checkbox selection for games
    games = forms.MultipleChoiceField(
        choices=GAME_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        help_text='Select one or both games',
    )

    class Meta:
        model  = Tournament
        fields = [
            'name', 'description', 'rules',
            'venue', 
        ]
       

    
    def clean_games(self):
        # join list ['valorant','pubg'] → "valorant,pubg" for storage
        return ','.join(self.cleaned_data['games'])


