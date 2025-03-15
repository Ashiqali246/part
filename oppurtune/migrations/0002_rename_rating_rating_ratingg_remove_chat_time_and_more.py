# Generated by Django 5.1.2 on 2025-03-09 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oppurtune', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='rating',
            new_name='ratingg',
        ),
        migrations.RemoveField(
            model_name='chat',
            name='time',
        ),
        migrations.AddField(
            model_name='job_provider',
            name='id_proof',
            field=models.FileField(default=1, upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rating',
            name='review',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='users_table',
            name='idproof',
            field=models.FileField(default=1, upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workers_table',
            name='email',
            field=models.CharField(default=1, max_length=40),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='users_table',
            name='dob',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='workers_table',
            name='dob',
            field=models.CharField(max_length=100),
        ),
    ]
