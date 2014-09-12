# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_auto_20140904_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='location',
            field=models.CharField(default='First Floor', max_length=40),
        ),
        migrations.AlterField(
            model_name='resource',
            name='experiment',
            field=models.ForeignKey(to_field=u'id', blank=True, to='inventory.Experiment', null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='experiment',
            field=models.ForeignKey(to_field=u'id', blank=True, to='inventory.Experiment', null=True),
        ),
        migrations.AlterField(
            model_name='link',
            name='experiment',
            field=models.ForeignKey(to_field=u'id', blank=True, to='inventory.Experiment', null=True),
        ),
    ]
