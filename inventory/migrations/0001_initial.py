# encoding: utf8
from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Text',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('manual', models.CharField(default='NULL', max_length=30, null=True, choices=[('OBSV', 'Observing Living Beings'), ('EQLB', 'Measurement and Equilibrium'), ('CONS', 'Constitution of Bodies'), ('MECH', 'Mechanics'), ('ELEC', 'Electricity and Magnetism'), ('MXWL', "Notes to Maxwell's Papers"), ('ATOM', 'Atoms and Measurement'), ('GENS', 'Genetics and Evolution')])),
                ('year', models.CharField(max_length=8, choices=[('FR', 'Freshman'), ('JR', 'Junior'), ('SR', 'Senior')])),
                ('author', models.CharField(default='Manual Authors', max_length=80, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField()),
                ('date_modified', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=75)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('room', models.ForeignKey(to_field=u'id', blank=True, to='inventory.Room', null=True)),
                ('location', models.CharField(default='Somewhere', max_length=100)),
                ('count', models.IntegerField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
