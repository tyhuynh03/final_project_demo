# Generated by Django 5.0.1 on 2024-04-09 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0009_alter_user_password"),
    ]

    operations = [
        migrations.RemoveField(model_name="user", name="name",),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
