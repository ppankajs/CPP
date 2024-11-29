from django.db import migrations

def create_default_policies(apps, schema_editor):
    Policy = apps.get_model('insurance', 'Policy')  # Replace 'insurance' with your app's name

    # Create three default policies if they don't already exist
    policies = [
        {
            'name': 'Basic Insurance Plan',
            'description': 'Covers basic repairs and liabilities.',
            'price': 100,
            'default': True
        },
        {
            'name': 'Standard Insurance Plan',
            'description': 'Includes more extensive coverage for accidents.',
            'price': 200,
            'default': True
        },
        {
            'name': 'Premium Insurance Plan',
            'description': 'Comprehensive coverage, including theft and damage.',
            'price': 300,
            'default': True
        }
    ]

    for policy in policies:
        # Ensure the policy doesn't already exist
        Policy.objects.get_or_create(
            name=policy['name'],
            defaults={
                'description': policy['description'],
                'price': policy['price'],
                'default': policy['default']
            }
        )

class Migration(migrations.Migration):
    dependencies = [
        ('insurance', '0001_initial')  # Replace with your actual previous migration
    ]

    operations = [
        migrations.RunPython(create_default_policies),
    ]
