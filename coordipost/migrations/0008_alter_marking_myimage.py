# Generated by Django 3.2.6 on 2021-10-02 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coordipost', '0007_rename_todeypoint_marking_todaypoint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marking',
            name='myimage',
            field=models.ImageField(default=None, null=True, upload_to=''),
        ),
    ]
