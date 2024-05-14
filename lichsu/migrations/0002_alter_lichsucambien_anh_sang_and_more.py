# Generated by Django 5.0.1 on 2024-05-14 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lichsu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lichsucambien',
            name='anh_sang',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='lichsucambien',
            name='do_am',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='lichsucambien',
            name='do_am_dat',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='lichsucambien',
            name='nhiet_do',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='lichsuhanhdong',
            name='den_chieu_sang',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='lichsuhanhdong',
            name='mai_che',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='lichsuhanhdong',
            name='may_tuoi_nuoc',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='lichsuhanhdong',
            name='quat_mat',
            field=models.FloatField(default=0),
        ),
    ]
