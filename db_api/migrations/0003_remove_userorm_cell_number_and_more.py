# Generated by Django 4.2.1 on 2023-05-26 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_api', '0002_bookorm_price_orderorm_choose_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userorm',
            name='cell_number',
        ),
        migrations.AddField(
            model_name='bookorm',
            name='deleted_by_cascade',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='orderorm',
            name='deleted_by_cascade',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name='bookorm',
            name='deleted',
            field=models.DateTimeField(db_index=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='orderorm',
            name='deleted',
            field=models.DateTimeField(db_index=True, editable=False, null=True),
        ),
    ]
