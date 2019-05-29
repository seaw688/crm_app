# Generated by Django 2.1.5 on 2019-03-15 18:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MAIN', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_projects', to=settings.AUTH_USER_MODEL),
        ),
    ]
