# Generated by Django 5.1.2 on 2024-11-13 11:34

import django.contrib.auth.models
import django.contrib.auth.validators
import django.contrib.postgres.fields
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_1', models.CharField(max_length=50)),
                ('line_2', models.CharField(max_length=50)),
                ('line_3', models.CharField(blank=True, max_length=50, null=True)),
                ('pin_code', models.IntegerField(validators=[django.core.validators.MaxValueValidator(0), django.core.validators.MinValueValidator(999999)])),
                ('country', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
            ],
        ),
        migrations.CreateModel(
            name='TripExtra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=50)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trip_name', models.CharField(max_length=100)),
                ('trip_type', models.CharField(choices=[('rural', 'Rural'), ('agro', 'Agro')], max_length=10)),
                ('trip_type_2', models.CharField(choices=[('group', 'Group'), ('solo', 'Solo')], max_length=10)),
                ('description', models.TextField()),
                ('price', models.FloatField()),
                ('min_people', models.IntegerField()),
                ('max_people', models.IntegerField()),
                ('discount_codes', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, null=True, size=None)),
                ('itenary', models.JSONField()),
                ('includes', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), size=None)),
                ('excludes', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), size=None)),
                ('allowed_extras', models.ManyToManyField(to='api.tripextra')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('auth_provider', models.CharField(choices=[('google', 'Google'), ('email', 'Email')], max_length=10)),
                ('billing_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.billingaddress')),
                ('groups', models.ManyToManyField(blank=True, related_name='custom_user_set', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='custom_user_permissions_set', to='auth.permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='BookedTrips',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extras_included', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('final_cost', models.FloatField()),
                ('is_done', models.BooleanField(default=False)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.trip')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.user')),
            ],
        ),
    ]