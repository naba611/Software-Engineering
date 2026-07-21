from django.db import models
from django.conf import settings
import random
import string


def generate_team_code():
    # generates a random 6-character uppercase code e.g. "AX9K2M"
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


class Team(models.Model):

    GAME_CHOICES = [
        ('valorant', 'Valorant'),
        ('pubg',     'PUBG'),
    ]

    name = models.CharField(max_length=100, unique=True)

    # which game this team plays
    game = models.CharField(max_length=20, choices=GAME_CHOICES)

    # the player who created and leads the team
    captain = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='captained_teams',
    )

    # unique code players can use to join
    team_code = models.CharField(
        max_length=10,
        unique=True,
        default=generate_team_code,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def max_size(self):
        # Valorant = 5, PUBG = 4
        return 5 if self.game == 'valorant' else 4

    def is_full(self):
        return self.memberships.count() >= self.max_size()

    def __str__(self):
        return f"{self.name} ({self.game})"


class TeamMembership(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='memberships',
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='memberships',
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'team')

    def __str__(self):
        return f"{self.user.username} → {self.team.name}"


class TeamInvite(models.Model):
    """
    Captain searches a username and sends an invite.
    Invited player can accept or reject.
    """

    STATUS_CHOICES = [
        ('pending',  'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='invites',
    )

    # the player being invited
    invited_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_invites',
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # can't invite the same player twice to the same team
        unique_together = ('team', 'invited_user')

    def __str__(self):
        return f"Invite: {self.invited_user.username} → {self.team.name} ({self.status})"


class JoinRequest(models.Model):

    STATUS_CHOICES = [
        ('pending',  'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='join_requests',
    )

    player = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='join_requests',
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # player can only have one pending request per team
        unique_together = ('team', 'player')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.player.username} → {self.team.name} ({self.status})"





