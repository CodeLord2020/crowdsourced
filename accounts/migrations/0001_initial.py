# Generated by Django 4.2.16 on 2024-12-24 19:53

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("cloud_resource", "__first__"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Role",
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
                    "role_type",
                    models.CharField(
                        choices=[
                            ("VOLUNTEER", "Volunteer"),
                            ("RESPONDER", "Responder"),
                            ("REPORTER", "Reporter"),
                            ("ADMIN", "Admin"),
                            ("SUPERADMIN", "Super Admin"),
                        ],
                        max_length=20,
                        unique=True,
                    ),
                ),
                ("description", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "role",
                "verbose_name_plural": "roles",
            },
        ),
        migrations.CreateModel(
            name="UserLocation",
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
                    "location",
                    models.CharField(
                        blank=True,
                        help_text="Geographic location in 'latitude,longitude' format",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "location_accuracy",
                    models.FloatField(
                        blank=True,
                        help_text="Accuracy of location in meters",
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                    ),
                ),
                (
                    "location_updated_at",
                    models.DateTimeField(
                        auto_now=True, help_text="Last time location was updated"
                    ),
                ),
                (
                    "address",
                    models.TextField(blank=True, help_text="Human-readable address"),
                ),
                (
                    "device_info",
                    models.JSONField(
                        default=dict,
                        help_text="Information about the device that reported location",
                    ),
                ),
            ],
            options={
                "ordering": ["-location_updated_at"],
                "indexes": [
                    models.Index(
                        fields=["location_updated_at"],
                        name="accounts_us_locatio_3aa337_idx",
                    )
                ],
            },
        ),
        migrations.CreateModel(
            name="User",
            fields=[
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
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("last_name", models.CharField(blank=True, max_length=100, null=True)),
                ("first_name", models.CharField(blank=True, max_length=100, null=True)),
                ("username", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="email address"
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(
                        blank=True,
                        max_length=17,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Phone number must be entered in the format: '+999999999'",
                                regex="^\\+?1?\\d{9,15}$",
                            )
                        ],
                    ),
                ),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                ("emergency_contact", models.CharField(blank=True, max_length=100)),
                (
                    "emergency_phone",
                    models.CharField(
                        blank=True,
                        max_length=17,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Phone number must be entered in the format: '+999999999'",
                                regex="^\\+?1?\\d{9,15}$",
                            )
                        ],
                    ),
                ),
                ("bio", models.TextField(blank=True)),
                ("last_active", models.DateTimeField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("is_verified", models.BooleanField(default=False)),
                (
                    "verification_token",
                    models.UUIDField(default=uuid.uuid4, editable=False),
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
                    "location",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="user",
                        to="accounts.userlocation",
                    ),
                ),
                (
                    "profile_picture",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="cloud_resource.profilepicresource",
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
                "verbose_name": "user",
                "verbose_name_plural": "users",
            },
        ),
        migrations.CreateModel(
            name="UserRole",
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
                ("assigned_at", models.DateTimeField(auto_now_add=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "assigned_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="role_assignments",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Assigned By",
                    ),
                ),
                (
                    "role",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="accounts.role"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_roles",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["user", "role", "is_active"],
                        name="accounts_us_user_id_cdaa7d_idx",
                    )
                ],
                "unique_together": {("user", "role")},
            },
        ),
        migrations.AddIndex(
            model_name="user",
            index=models.Index(
                fields=["email", "is_active"], name="accounts_us_email_f69303_idx"
            ),
        ),
    ]
