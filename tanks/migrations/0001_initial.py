# Generated by Django 3.1.3 on 2021-05-10 08:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('homolog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Zbiornik',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numer', models.CharField(max_length=4)),
                ('dataBadania', models.DateField(default='2020-01-01')),
                ('nr_odbioru', models.IntegerField(default=1)),
                ('nr_rozrywania', models.IntegerField(default=1)),
                ('pekniecie', models.IntegerField(choices=[(0, 'empty'), (1, 'plastyczne'), (2, 'kruche')], default=0)),
                ('rodzaj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tracks', to='homolog.rodzaj')),
            ],
            options={
                'verbose_name': 'Zbiornik',
                'verbose_name_plural': 'Zbiorniki',
            },
        ),
        migrations.CreateModel(
            name='Badanie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('woda', models.FloatField()),
                ('cisnienie', models.IntegerField()),
                ('czas', models.TimeField()),
                ('zbiornik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tanks.zbiornik')),
            ],
            options={
                'verbose_name': 'Badanie',
                'verbose_name_plural': 'Badania',
            },
        ),
    ]