"""
Frontend template rendering views for Django integration.
Allows Django to directly serve the Phase 1 frontend templates and static assets.
"""

from django.shortcuts import render
from django.http import Http404
from django.views.generic import TemplateView
import os
from django.conf import settings

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['user'] = self.request.user
        ctx['is_authenticated'] = self.request.user.is_authenticated
        return ctx

def render_page(request, page_name):
    """
    Renders any frontend page template from frontend/pages/<page_name>.html.
    Provides authentication context and ensures cache-control prevents stale history.
    """
    clean_name = os.path.basename(page_name)
    if not clean_name.endswith('.html'):
        clean_name += '.html'

    page_path = settings.BASE_DIR / 'frontend' / 'pages' / clean_name
    if not os.path.exists(page_path):
        raise Http404(f"Page '{clean_name}' not found.")

    response = render(request, f"pages/{clean_name}", {
        'page_name': clean_name,
        'user': request.user,
        'is_authenticated': request.user.is_authenticated
    })
    response['Cache-Control'] = 'no-cache, must-revalidate'
    return response
