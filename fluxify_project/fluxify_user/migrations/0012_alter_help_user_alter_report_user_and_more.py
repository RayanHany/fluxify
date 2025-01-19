# Generated by Django 5.1.4 on 2025-01-19 15:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fluxify_post', '0006_alter_post_mark_post_image'),
        ('fluxify_user', '0011_alter_user_custome_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='help',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='help_user', to='fluxify_user.user_custome'),
        ),
        migrations.AlterField(
            model_name='report',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reports_user', to='fluxify_user.user_custome'),
        ),
        migrations.AlterField(
            model_name='verification',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='verification_user', to='fluxify_user.user_custome'),
        ),
        migrations.CreateModel(
            name='SavedPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saved_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fluxify_post.post_mark')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='saved_user', to='fluxify_user.user_custome')),
            ],
        ),
    ]
