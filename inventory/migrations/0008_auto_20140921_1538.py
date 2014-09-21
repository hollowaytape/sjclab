# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import inventory.models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_auto_20140918_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='path',
            field=models.ImageField(upload_to=b'experiments/images/', validators=[inventory.models.validate_filesize]),
        ),
        migrations.AlterField(
            model_name='resource',
            name='path',
            field=models.FileField(upload_to=b'experiments/resources/', validators=[inventory.models.validate_filesize]),
        ),
    ]
