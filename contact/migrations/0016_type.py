# Generated by Django 2.2.1 on 2019-06-19 09:57

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0015_auto_20190618_1442'),
    ]

    operations = [
        migrations.CreateModel(
            name='Type',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Name of the Type', max_length=128)),
                ('organization_uuid', models.UUIDField(db_index=True, help_text="UUID of the organization that has access to the Type, if it's not global.", verbose_name='Organization UUID')),
                ('is_global', models.BooleanField(default=False, help_text='All organizations have access to global types.')),
            ],
        ),
    ]
