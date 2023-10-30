# Generated by Django 4.2.6 on 2023-10-30 11:44

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import hr.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=128)),
                ('last_name', models.CharField(default='', max_length=128)),
                ('annual_income', models.PositiveIntegerField(null=True, validators=[django.core.validators.MaxValueValidator(2000000)])),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True)),
                ('yoe', models.PositiveSmallIntegerField(db_comment='Years of experience', null=True, validators=[django.core.validators.MaxValueValidator(52)])),
                ('dob', models.DateField(db_comment='Date of birth in the format', null=True, validators=[hr.validators.validate_dob])),
                ('industry', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hr.industry')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
