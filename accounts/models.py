from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    ROLE_CHOICES = [
        ('player',    'Player'),
        ('organizer', 'Organizer'),
        ('admin',     'Admin'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='player',
    )

    address = models.CharField(max_length=255, blank=True)
    phone   = models.CharField(max_length=20,  blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


class PlayerProfile(models.Model):
    """
    Extra profile info specific to players.
    One-to-one with CustomUser — one profile per player.
    """

    INGAME_ROLE_CHOICES = [
    ('',            'Prefer not to say'),
    ('assault',     'Assault'),
    ('skirmisher',  'Skirmisher'),
    ('support',     'Support'),
    ('controller',  'Controller'),
    ('recon',       'Recon'),
]

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='player_profile',
    )

    # in-game role the player prefers
    ingame_role = models.CharField(
        max_length=20,
        choices=INGAME_ROLE_CHOICES,
        blank=True,
    )

    # optional short bio
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} — {self.ingame_role}"
