"""
Shared test base class for JustBaddo.
Automatically runs seed_catalogue on test database creation so all tests
have access to the verified discography, playlists, and community records.
"""

from django.test import TestCase
from django.core.management import call_command
import os

class JustBaddoTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        with open(os.devnull, 'w') as fnull:
            call_command('seed_catalogue', stdout=fnull)
