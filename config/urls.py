"""
Main URL Configuration for JustBaddo (Phase 2: Backend Development).

Mounts:
- Django Admin (/admin/)
- Frontend Template Pages (/, /pages/<page_name>.html)
- API v1 Endpoints (/api/v1/...)
  - /api/v1/core/
  - /api/v1/accounts/
  - /api/v1/music/
  - /api/v1/playback/
  - /api/v1/playlists/
  - /api/v1/community/
  - /api/v1/arena/
  - /api/v1/stories/
  - /api/v1/notifications/
  - /api/v1/licensing/
  - /api/v1/moderation/
- Resource aliases (/api/v1/albums/, /api/v1/tracks/, etc.)
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from core.views import HealthCheckView, PlatformMetadataView
from core.frontend_views import IndexView, render_page, members_view
from music.views import AlbumListView, AlbumDetailView, TrackDetailView
from community.views import PostListCreateView, PostDetailView
from accounts.views import (
    CurrentUserProfileView, PublicUserProfileView,
    AccountLoginTemplateView, AccountRegisterTemplateView,
    AccountSignoutTemplateView, AccountForgotPasswordTemplateView,
    AccountResetPasswordTemplateView, AccountVerifyEmailTemplateView,
    AccountResendVerificationView, AccountWelcomeTemplateView
)

api_v1_patterns = [
    # Core & Metadata
    path('core/', include('core.urls', namespace='core')),
    path('health/', HealthCheckView.as_view(), name='api-health'),
    path('platform/', PlatformMetadataView.as_view(), name='api-platform'),

    # Domain Applications
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('music/', include('music.urls', namespace='music')),
    path('playback/', include('playback.urls', namespace='playback')),
    path('playlists/', include('playlists.urls', namespace='playlists')),
    path('community/', include('community.urls', namespace='community')),
    path('arena/', include('arena.urls', namespace='arena')),
    path('stories/', include('stories.urls', namespace='stories')),
    path('notifications/', include('notifications.urls', namespace='notifications')),
    path('licensing/', include('licensing.urls', namespace='licensing')),
    path('moderation/', include('moderation.urls', namespace='moderation')),

    # REST Resource Aliases matching frontend design conventions
    path('profiles/', CurrentUserProfileView.as_view(), name='api-profile-alias'),
    path('profiles/<str:username>/', PublicUserProfileView.as_view(), name='api-public-profile-alias'),
    path('albums/', AlbumListView.as_view(), name='api-albums-alias'),
    path('albums/<slug:slug>/', AlbumDetailView.as_view(), name='api-album-detail-alias'),
    path('tracks/<str:track_id>/', TrackDetailView.as_view(), name='api-track-detail-alias'),
    path('posts/', PostListCreateView.as_view(), name='api-posts-alias'),
    path('posts/<str:post_id>/', PostDetailView.as_view(), name='api-post-detail-alias'),
]

urlpatterns = [
    # Favicon
    path('favicon.ico', RedirectView.as_view(url='/static/images/favicon.svg', permanent=True)),

    # Django Administration
    path('admin/', admin.site.urls),

    # REST API v1
    path('api/v1/', include((api_v1_patterns, 'api-v1'))),
    path('api/', include((api_v1_patterns, 'api-root'))),  # Default /api/ forwards to v1

    # Frontend Template Rendering (Modular integration with Phase 1 templates)
    path('', IndexView.as_view(), name='frontend-index'),
    path('index.html', IndexView.as_view(), name='frontend-index-html'),
    path('members/', members_view, name='frontend-members'),
    path('members', members_view, name='frontend-members-slashless'),

    # Dedicated Authentication Suite
    path('accounts/login/', AccountLoginTemplateView.as_view(), name='accounts-login'),
    path('accounts/register/', AccountRegisterTemplateView.as_view(), name='accounts-register'),
    path('accounts/logout/', AccountSignoutTemplateView.as_view(), name='accounts-logout'),
    path('accounts/forgot-password/', AccountForgotPasswordTemplateView.as_view(), name='accounts-forgot-password'),
    path('accounts/reset-password/', AccountResetPasswordTemplateView.as_view(), name='accounts-reset-password'),
    path('accounts/verify-email/', AccountVerifyEmailTemplateView.as_view(), name='accounts-verify-email'),
    path('accounts/resend-verification/', AccountResendVerificationView.as_view(), name='accounts-resend-verification'),
    path('accounts/welcome/', AccountWelcomeTemplateView.as_view(), name='accounts-welcome'),

    # Direct Route Aliases for legacy and frontend links
    path('pages/login.html', AccountLoginTemplateView.as_view()),
    path('pages/register.html', AccountRegisterTemplateView.as_view()),
    path('pages/forgot-password.html', AccountForgotPasswordTemplateView.as_view()),
    path('pages/reset-password.html', AccountResetPasswordTemplateView.as_view()),
    path('pages/verify-email.html', AccountVerifyEmailTemplateView.as_view()),
    path('pages/welcome.html', AccountWelcomeTemplateView.as_view()),

    path('pages/<str:page_name>', render_page, name='frontend-page'),
]

# Serve static files and media in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
