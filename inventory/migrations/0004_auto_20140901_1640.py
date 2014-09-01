# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='location',
            field=models.CharField(default='Somewhere', max_length=100, null=True),
        ),
    ]
