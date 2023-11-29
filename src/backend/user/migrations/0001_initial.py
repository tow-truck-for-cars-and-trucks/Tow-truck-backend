<<<<<<< HEAD
# Generated by Django 4.2.7 on 2023-11-08 12:44

import django.contrib.auth.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
=======
# Generated by Django 4.2.7 on 2023-11-27 12:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import user.utils


class Migration(migrations.Migration):

>>>>>>> develop
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
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
                (
                    "password",
                    models.CharField(max_length=128, verbose_name="password"),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
<<<<<<< HEAD
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="date joined",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        max_length=150,
                        unique=True,
                        verbose_name="Имя пользователя",
                    ),
                ),
                (
                    "tel",
                    models.CharField(
                        db_index=True,
                        max_length=254,
                        unique=True,
                        verbose_name="Номер телефона",
=======
                    "first_name",
                    models.CharField(max_length=150, verbose_name="Имя"),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="Фамилия"
                    ),
                ),
                (
                    "phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=128,
                        region="RU",
                        unique=True,
                        verbose_name="Телефон",
>>>>>>> develop
                    ),
                ),
                (
                    "email",
                    models.EmailField(
<<<<<<< HEAD
                        db_index=True,
=======
                        error_messages={
                            "unique": "Этот адрес электронной почты уже зарегистрован."
                        },
>>>>>>> develop
                        max_length=254,
                        unique=True,
                        verbose_name="Электронная почта",
                    ),
                ),
                (
<<<<<<< HEAD
                    "first_name",
                    models.CharField(max_length=150, verbose_name="Имя"),
                ),
                (
                    "last_name",
                    models.CharField(max_length=150, verbose_name="Фамилия"),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("User", "Пользователь"),
                            ("Admin", "Администратор"),
                        ],
                        default="User",
                        help_text="Роль пользователя с правами доступа",
                        max_length=30,
                        verbose_name="Роль",
=======
                    "is_staff",
                    models.BooleanField(
                        default=False, verbose_name="Стафф статус"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False, verbose_name="Super статус"
                    ),
                ),
                (
                    "is_verified",
                    models.BooleanField(
                        default=False, verbose_name="Подтверждение"
>>>>>>> develop
                    ),
                ),
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
            options={
                "verbose_name": "Пользователь",
                "verbose_name_plural": "Пользователи",
<<<<<<< HEAD
                "ordering": ("username",),
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
=======
                "ordering": ("email", "phone"),
                "unique_together": {("email", "phone")},
            },
        ),
        migrations.CreateModel(
            name="Avatar",
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
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=user.utils.get_avatar_path,
                        verbose_name="Аватар",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="avatar",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Аватар",
                "verbose_name_plural": "Аватарки",
                "ordering": ("user",),
            },
>>>>>>> develop
        ),
    ]
