from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Photo, Profile, Reaction, Tag


class GalleryTests(TestCase):
    """Test the main NuruCanvas features."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='tester',
            email='tester@example.com',
            password='SecurePassword123!'
        )

        self.nature_tag = Tag.objects.create(
            name='Nature'
        )

        self.artwork_tag = Tag.objects.create(
            name='Artwork'
        )

        self.nature_photo = Photo.objects.create(
            title='Nature Photo',
            description='A beautiful nature photograph.',
            image='photos/nature-test.jpg',
            uploaded_by=self.user
        )

        self.nature_photo.tags.add(self.nature_tag)

        self.artwork_photo = Photo.objects.create(
            title='Artwork Photo',
            description='A colourful piece of artwork.',
            image='photos/artwork-test.jpg',
            uploaded_by=self.user
        )

        self.artwork_photo.tags.add(self.artwork_tag)

    def test_profile_is_created_automatically(self):
        """Every new user should receive a profile."""

        self.assertTrue(
            Profile.objects.filter(user=self.user).exists()
        )

    def test_gallery_requires_login(self):
        """Logged-out visitors should be sent to login."""

        home_url = reverse('photo_gallery:home')
        login_url = reverse('photo_gallery:login')

        response = self.client.get(home_url)

        self.assertRedirects(
            response,
            f'{login_url}?next={home_url}'
        )

    def test_logged_in_user_can_view_gallery(self):
        """Authenticated users should see gallery photos."""

        self.client.force_login(self.user)

        response = self.client.get(
            reverse('photo_gallery:home')
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nature Photo')
        self.assertContains(response, 'Artwork Photo')

    def test_photos_can_be_filtered_by_tag(self):
        """Nature filtering should exclude artwork-only photos."""

        self.client.force_login(self.user)

        response = self.client.get(
            reverse('photo_gallery:home'),
            {'tag': self.nature_tag.slug}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response,  'Nature Photo')
        self.assertNotContains(response, 'Artwork Photo')

    def test_user_can_register(self):
        """A visitor should be able to create an account."""

        response = self.client.post(
            reverse('photo_gallery:register'),
            {
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password1': 'StrongRegistration789!',
                'password2': 'StrongRegistration789!',
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            User.objects.filter(username='newuser').exists()
        )

        new_user = User.objects.get(username='newuser')

        self.assertTrue(
            Profile.objects.filter(user=new_user).exists()
        )

    def test_user_can_edit_profile(self):
        """A user should be able to update account information."""

        self.client.force_login(self.user)

        response = self.client.post(
            reverse('photo_gallery:edit_profile'),
            {
                'username': 'updatedtester',
                'email': 'updated@example.com',
                'bio': 'I enjoy photography.',
            }
        )

        self.assertEqual(response.status_code, 302)

        self.user.refresh_from_db()
        self.user.profile.refresh_from_db()

        self.assertEqual(
            self.user.username,
            'updatedtester'
        )

        self.assertEqual(
            self.user.profile.bio,
            'I enjoy photography.'
        )

    def test_reaction_can_be_created_removed_and_changed(self):
        """A reaction should toggle and switch correctly."""

        self.client.force_login(self.user)

        like_url = reverse(
            'photo_gallery:react_to_photo',
            args=[self.nature_photo.pk, 'like']
        )

        dislike_url = reverse(
            'photo_gallery:react_to_photo',
            args=[self.nature_photo.pk, 'dislike']
        )

        # Create a like.
        self.client.post(like_url)

        reaction = Reaction.objects.get(
            user=self.user,
            photo=self.nature_photo
        )

        self.assertEqual(
            reaction.reaction_type,
            Reaction.LIKE
        )

        # Clicking Like again removes it.
        self.client.post(like_url)

        self.assertFalse(
            Reaction.objects.filter(
                user=self.user,
                photo=self.nature_photo
            ).exists()
        )

        # Create a dislike.
        self.client.post(dislike_url)

        reaction = Reaction.objects.get(
            user=self.user,
            photo=self.nature_photo
        )

        self.assertEqual(
            reaction.reaction_type,
            Reaction.DISLIKE
        )

        # Switch the dislike to a like.
        self.client.post(like_url)

        reaction.refresh_from_db()

        self.assertEqual(
            reaction.reaction_type,
            Reaction.LIKE
        )

        self.assertEqual(
            Reaction.objects.filter(
                user=self.user,
                photo=self.nature_photo
            ).count(),
            1
        )