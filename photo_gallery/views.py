from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    ProfileUpdateForm,
    RegistrationForm,
    UserUpdateForm,
)

from .models import Photo, Tag, Profile


def register(request):
    """Create a user account and log the new user in."""

    if request.user.is_authenticated:
        return redirect('photo_gallery:home')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                'Your NuruCanvas account was created successfully.'
            )

            return redirect('photo_gallery:home')
    else:
        form = RegistrationForm()

    return render(
        request,
        'photo_gallery/register.html',
        {'form': form}
    )


@login_required
def home(request):
    """Display all photos and optionally filter them by tag."""

    tag_slug = request.GET.get('tag')
    selected_tag = None

    photos = Photo.objects.select_related(
        'uploaded_by'
    ).prefetch_related('tags')

    if tag_slug:
        selected_tag = get_object_or_404(
            Tag,
            slug=tag_slug
        )

        photos = photos.filter(
            tags=selected_tag
        ).distinct()

    tags = Tag.objects.all()

    context = {
        'photos': photos,
        'tags': tags,
        'selected_tag': selected_tag,
    }

    return render(
        request,
        'photo_gallery/home.html',
        context
    )


@login_required
def photo_detail(request, pk):
    """Display the complete information for one photo."""

    photo = get_object_or_404(
        Photo.objects.select_related(
            'uploaded_by'
        ).prefetch_related('tags'),
        pk=pk
    )

    return render(
        request,
        'photo_gallery/photo_detail.html',
        {'photo': photo}
    )

@login_required
def profile(request):
    """Display the currently logged-in user's profile."""

    user_profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    return render(
        request,
        'photo_gallery/profile.html',
        {'profile': user_profile}
    )


@login_required
def edit_profile(request):
    """Allow the current user to update their profile."""

    user_profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':
        user_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )

        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=user_profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(
                request,
                'Your profile was updated successfully.'
            )

            return redirect('photo_gallery:profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=user_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(
        request,
        'photo_gallery/edit_profile.html',
        context
    )