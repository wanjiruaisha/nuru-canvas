from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Profile(models.Model):
    """Store additional information for each registered user."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


class Tag(models.Model):
    """Represent a category used to filter photos."""

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Photo(models.Model):
    """Represent a photograph or artwork in the gallery."""

    title = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to='photos/')
    tags = models.ManyToManyField(
        Tag,
        related_name='photos',
        blank=True
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='photos'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def like_count(self):
        return self.reactions.filter(reaction_type='like').count()

    @property
    def dislike_count(self):
        return self.reactions.filter(reaction_type='dislike').count()

    def __str__(self):
        return self.title


class Reaction(models.Model):
    """Store one like or dislike per user for each photo."""

    LIKE = 'like'
    DISLIKE = 'dislike'

    REACTION_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='photo_reactions'
    )
    photo = models.ForeignKey(
        Photo,
        on_delete=models.CASCADE,
        related_name='reactions'
    )
    reaction_type = models.CharField(
        max_length=7,
        choices=REACTION_CHOICES
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'photo'],
                name='unique_user_photo_reaction'
            )
        ]

    def __str__(self):
        return (
            f'{self.user.username} - '
            f'{self.reaction_type} - {self.photo.title}'
        )