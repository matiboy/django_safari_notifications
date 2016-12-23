from django.core.management.base import BaseCommand
import inquirer
from ...models import ICON_SIZES, validate_website_push_id


class Command(BaseCommand):
    help = 'Create a new domain and corresponding domain names'

    def handle(self, *args, **options):
        questions = [
            inquirer.Text(name='name', message='Name to appear on notifications'),
            inquirer.Text(
                name='website_push_id',
                message='Website push ID (from Apple Developer certificate)',
                validate=lambda _, wpid: validate_website_push_id(wpid)
            )
        ]

        answers = inquirer.prompt(questions)

        print(answers)
