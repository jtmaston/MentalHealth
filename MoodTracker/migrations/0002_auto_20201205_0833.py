# Generated by Django 3.1.4 on 2020-12-05 08:33

from django.db import migrations
import fernet_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('MoodTracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='note',
            field=fernet_fields.fields.EncryptedTextField(),
        ),
    ]