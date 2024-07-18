from django.core.management.base import BaseCommand
from api.models import Plan

class Command(BaseCommand):
    help = 'Populate the database with example plans and subscriptions'

    def handle(self, *args, **kwargs):
        plans = [
            {
                'name': 'Free Plan',
                'description': 'This is a free plan.',
                'price': 0.00,
                'duration_days': 366
            },
            {
                'name': 'Basic Plan',
                'description': 'This is a basic plan.',
                'price': 5.00,
                'duration_days': 30
            },
            {
                'name': 'Standard Plan',
                'description': 'This is a standard plan.',
                'price': 10.00,
                'duration_days': 30
            },
            {
                'name': 'Premium Plan',
                'description': 'This is a premium plan.',
                'price': 20.00,
                'duration_days': 30
            },
            {
                'name': 'Basic Plan Year',
                'description': 'This is a basic year plan.',
                'price': 60.00,
                'duration_days': 366
            },
            {
                'name': 'Standard Plan Year',
                'description': 'This is a standard year plan.',
                'price': 120.00,
                'duration_days': 366
            },
            {
                'name': 'Premium Plan Year',
                'description': 'This is a premium year plan.',
                'price': 240.00,
                'duration_days': 366
            }
        ]

        for plan_data in plans:
            plan, created = Plan.objects.get_or_create(**plan_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Plan "{plan.name}" created successfully.'))
            else:
                self.stdout.write(self.style.WARNING(f'Plan "{plan.name}" already exists.'))

        self.stdout.write(self.style.SUCCESS('Database populated with example plans.'))
