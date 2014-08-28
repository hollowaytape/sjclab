# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('text', models.ForeignKey(to_field=u'id', blank=True, to='inventory.Text', null=True)),
                ('session', models.IntegerField(null=True, blank=True)),
                ('procedure', models.TextField(null=True, blank=True)),
                ('main_photo', models.ImageField(null=True, upload_to='experiments/images/', blank=True)),
                ('resources', models.FileField(null=True, upload_to='inventory/resources/', blank=True)),
                ('on_program', models.BooleanField(default=True)),
                ('complete', models.BooleanField(default=False)),
                ('materials', models.ManyToManyField(to='inventory.Material', null=True, blank=True)),
                ('tags', models.ManyToManyField(to='inventory.Tag', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
