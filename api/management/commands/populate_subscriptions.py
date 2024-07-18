from django.core.management.base import BaseCommand
from api.models import Plan, Subscription
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the database with sample subscriptions'

    def handle(self, *args, **kwargs):
        # Example users
        users = User.objects.all()

        if not users.exists():
            self.stdout.write(self.style.ERROR('No users found in the database. Please create some users first.'))
            return

        # Example plans
        plans = Plan.objects.all()

        if not plans.exists():
            self.stdout.write(self.style.ERROR('No plans found in the database. Please create some plans first.'))
            return

        # Create subscriptions for each user
        for user in users:
            for plan in plans:
                subscription, created = Subscription.objects.get_or_create(
                    user=user,
                    plan=plan,
                    defaults={
                        'start_date': timezone.now(),
                        'end_date': timezone.now() + timezone.timedelta(days=plan.duration_days)
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Subscription for user "{user.email}" with plan "{plan.name}" created successfully.'))
                else:
                    self.stdout.write(self.style.WARNING(f'Subscription for user "{user.email}" with plan "{plan.name}" already exists.'))

        self.stdout.write(self.style.SUCCESS('Database populated with example subscriptions.'))
