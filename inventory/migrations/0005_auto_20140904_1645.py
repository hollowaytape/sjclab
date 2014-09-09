# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_auto_20140901_1640'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('caption', models.CharField(max_length=100)),
                ('path', models.ImageField(upload_to='experiments/images/')),
                ('experiment', models.ForeignKey(to='inventory.Experiment', to_field=u'id')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=400)),
                ('experiment', models.ForeignKey(to='inventory.Experiment', to_field=u'id')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('path', models.FileField(upload_to='experiments/resources/')),
                ('experiment', models.ForeignKey(to='inventory.Experiment', to_field=u'id')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='room',
            name='location',
            field=models.CharField(default='Mellon Physics Hall', max_length=40),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='session',
        ),
        migrations.AlterField(
            model_name='text',
            name='year',
            field=models.CharField(max_length=8, choices=[('FR', 'Freshman'), ('JR', 'Junior'), ('SR', 'Senior'), ('OT', 'Other')]),
        ),
    ]
