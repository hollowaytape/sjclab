# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_auto_20140921_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='title',
            field=models.CharField(unique=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='link',
            name='url',
            field=models.CharField(max_length=400, validators=[django.core.validators.URLValidator()]),
        ),
        migrations.AlterField(
            model_name='material',
            name='location',
            field=models.CharField(default=b'Somewhere', max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='text',
            name='manual',
            field=models.CharField(default=b'NULL', max_length=30, null=True, choices=[(b'Observing Living Beings', b'Observing Living Beings'), (b'Measurement and Equilibrium', b'Measurement and Equilibrium'), (b'Constitution of Bodies', b'Constitution of Bodies'), (b'Mechanics', b'Mechanics'), (b'Electricity and Magnetism', b'Electricity and Magnetism'), (b"Maxwell's Papers", b"Maxwell's Papers"), (b'Atoms and Measurement', b'Atoms and Measurement'), (b'Genetics and Evolution', b'Genetics and Evolution')]),
        ),
        migrations.AlterField(
            model_name='text',
            name='title',
            field=models.CharField(unique=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='text',
            name='year',
            field=models.CharField(max_length=8, choices=[(b'Freshman', b'Freshman'), (b'Junior', b'Junior'), (b'Senior', b'Senior'), (b'Other', b'Other')]),
        ),
    ]
