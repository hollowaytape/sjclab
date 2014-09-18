# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_auto_20140911_1939'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='location',
            new_name='floor',
        ),
        migrations.AddField(
            model_name='room',
            name='hall',
            field=models.CharField(max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='room',
            name='number',
            field=models.CharField(max_length=20),
        ),
    ]
