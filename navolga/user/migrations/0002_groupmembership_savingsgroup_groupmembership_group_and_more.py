# Generated by Django 5.1.4 on 2025-02-01 16:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
                ('role', models.CharField(choices=[('member', 'Member'), ('admin', 'Admin')], default='member', max_length=20)),
                ('account_balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('has_loan', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SavingsGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_groups', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(related_name='savings_groups', through='user.GroupMembership', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='groupmembership',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.savingsgroup'),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('deposit', 'Deposit'), ('withdraw', 'Withdraw'), ('loan', 'Loan'), ('loan_repayment', 'Loan Repayment')], max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('balance_after_transaction', models.DecimalField(decimal_places=2, max_digits=12)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.savingsgroup')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.userprofile')),
            ],
        ),
    ]
