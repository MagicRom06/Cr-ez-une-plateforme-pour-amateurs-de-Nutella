from django.core.management.base import BaseCommand

from .main import main


class Command(BaseCommand):
    help = 'load data'

    def handle(self, *args, **kwargs):
        main()
