# Generated by Django 4.0.6 on 2022-08-05 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_remove_choice_user_choice_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventuser',
            name='event',
            field=models.ForeignKey(default='e33da628-426b-4c5c-8212-27051da43f69', on_delete=django.db.models.deletion.CASCADE, to='events.event'),
            preserve_default=False,
        ),
    ]
