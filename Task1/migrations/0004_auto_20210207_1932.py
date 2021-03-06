# Generated by Django 2.2 on 2021-02-07 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Task1', '0003_account_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='useractivities',
            name='created_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='useractivities',
            name='edited_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='type_of_user',
            field=models.CharField(choices=[('education', 'education'), ('recreational', 'recreational'), ('social', 'social'), ('diy', 'diy'), ('charity', 'charity'), ('cooking', 'cooking'), ('relaxation', 'relaxation'), ('music', 'music'), ('busywork', 'busywork')], max_length=50),
        ),
    ]
