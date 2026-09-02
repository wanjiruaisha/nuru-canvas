from django.contrib import admin

from .models import Photo, Profile, Reaction, Tag


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username', 'user__email')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'uploaded_by',
        'created_at',
        'like_count',
        'dislike_count',
    )
    search_fields = ('title', 'description')
    list_filter = ('tags', 'created_at')
    filter_horizontal = ('tags',)


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'photo',
        'reaction_type',
        'created_at',
    )
    list_filter = ('reaction_type', 'created_at')
    search_fields = ('user__username', 'photo__title')