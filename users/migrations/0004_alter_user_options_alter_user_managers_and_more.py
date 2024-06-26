# Generated by Django 5.0.1 on 2024-04-09 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("users", "0003_delete_choice_delete_question"),
    ]

    operations = [
        migrations.AlterModelOptions(name="user", options={},),
        migrations.AlterModelManagers(name="user", managers=[],),
        migrations.RemoveField(model_name="user", name="date_joined",),
        migrations.RemoveField(model_name="user", name="first_name",),
        migrations.RemoveField(model_name="user", name="groups",),
        migrations.RemoveField(model_name="user", name="is_active",),
        migrations.RemoveField(model_name="user", name="is_staff",),
        migrations.RemoveField(model_name="user", name="is_superuser",),
        migrations.RemoveField(model_name="user", name="last_name",),
        migrations.RemoveField(model_name="user", name="name",),
        migrations.RemoveField(model_name="user", name="user_permissions",),
        migrations.AddField(
            model_name="user",
            name="full_name",
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="user",
            name="profile_picture",
            field=models.ImageField(
                blank=True, null=True, upload_to="profile_pictures"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="password",
            field=models.CharField(max_length=128, verbose_name="password"),
        ),
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("full_name", models.CharField(blank=True, max_length=150)),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
    ]
