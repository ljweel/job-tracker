from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resumes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resumeevent',
            name='target_role',
        ),
        migrations.RemoveField(
            model_name='resumeevent',
            name='memo',
        ),
    ]
