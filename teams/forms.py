from django import forms
from .models import Team


class CreateTeamForm(forms.ModelForm):
    class Meta:
        model  = Team
        fields = ['name', 'game']


class JoinByCodeForm(forms.Form):
    team_code = forms.CharField(
        max_length=10,
        label='Team Code',
    )


class InvitePlayerForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label='Search by username',
    )

