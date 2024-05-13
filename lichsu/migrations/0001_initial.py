# Generated by Django 4.0.1 on 2024-05-12 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('manhdat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LichSuHanhDong',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mai_che', models.IntegerField(default=0)),
                ('quat_mat', models.IntegerField(default=0)),
                ('may_tuoi_nuoc', models.IntegerField(default=0)),
                ('den_chieu_sang', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('manhdat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='manhdat.manhdat')),
            ],
        ),
        migrations.CreateModel(
            name='LichSuCamBien',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nhiet_do', models.IntegerField(default=0)),
                ('do_am', models.IntegerField(default=0)),
                ('do_am_dat', models.IntegerField(default=0)),
                ('anh_sang', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('manhdat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='manhdat.manhdat')),
            ],
        ),
    ]