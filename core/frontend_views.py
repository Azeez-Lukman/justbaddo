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

def render_page(request, page_name):
    """
    Renders any frontend page template from frontend/pages/<page_name>.html.
    """
    clean_name = os.path.basename(page_name)
    if not clean_name.endswith('.html'):
        clean_name += '.html'

    page_path = settings.BASE_DIR / 'frontend' / 'pages' / clean_name
    if not os.path.exists(page_path):
        raise Http404(f"Page '{clean_name}' not found.")

    return render(request, f"pages/{clean_name}", {'page_name': clean_name})
