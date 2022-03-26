# Generated by Django 4.0.3 on 2022-03-24 18:30

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('doctor_id', models.AutoField(primary_key=True, serialize=False)),
                ('specialization', models.CharField(default='N/A', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('form_id', models.AutoField(primary_key=True, serialize=False)),
                ('patient_name', models.CharField(default='N/A', max_length=120)),
                ('relationship', models.CharField(default='N/A', max_length=20)),
                ('consultation_date', models.DateTimeField(max_length=20)),
                ('referral_advisor', models.CharField(default='N/A', max_length=120)),
                ('consultation_fees', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('consultation_visits', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('file', models.FileField(upload_to='')),
                ('hc_medical_advisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('medicine_id', models.AutoField(primary_key=True, serialize=False)),
                ('medicine_name', models.CharField(default='N/A', max_length=50)),
                ('brand', models.CharField(default='N/A', max_length=50)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('test_id', models.AutoField(primary_key=True, serialize=False)),
                ('test_name', models.CharField(default='N/A', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=120)),
                ('username', models.CharField(max_length=40, unique=True)),
                ('roll', models.CharField(max_length=6, unique=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('contact', models.CharField(default='N/A', max_length=10)),
                ('address', models.CharField(default='N/A', max_length=400)),
                ('designation', models.CharField(max_length=120)),
                ('roles', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=50)),
                ('reimbursement_amount', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('feedback', models.CharField(default='N/A', max_length=400)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('admin_update_date', models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0))),
                ('doctor_update_date', models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0))),
                ('account_sent_date', models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0))),
                ('account_approve_date', models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0))),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.form')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('patient_id', models.AutoField(primary_key=True, serialize=False)),
                ('bank_name', models.CharField(default='N/A', max_length=40)),
                ('department', models.CharField(default='N/A', max_length=20)),
                ('bank_IFSC', models.CharField(default='N/A', max_length=11)),
                ('bank_AC', models.CharField(default='N/A', max_length=18)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
        migrations.CreateModel(
            name='HCAdmin',
            fields=[
                ('admin_id', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
        migrations.CreateModel(
            name='FormTest',
            fields=[
                ('ft_id', models.AutoField(primary_key=True, serialize=False)),
                ('lab', models.CharField(default='N/A', max_length=50)),
                ('cost', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.form')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.test')),
            ],
        ),
        migrations.CreateModel(
            name='FormMedicine',
            fields=[
                ('fm_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(default=0)),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.form')),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.medicine')),
            ],
        ),
        migrations.AddField(
            model_name='form',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.patient'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user'),
        ),
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('acc_id', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
    ]
