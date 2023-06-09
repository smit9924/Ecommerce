# Generated by Django 4.1.7 on 2023-03-18 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='itemData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=50)),
                ('brand', models.CharField(max_length=50)),
                ('image', models.URLField(max_length=300)),
            ],
            options={
                'db_table': 'Item',
            },
        ),
    ]
