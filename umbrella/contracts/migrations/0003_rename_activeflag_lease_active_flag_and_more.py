# Generated by Django 4.0.1 on 2022-03-16 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0002_alter_lease_createdby_alter_lease_file_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lease',
            old_name='activeflag',
            new_name='active_flag',
        ),
        migrations.RenameField(
            model_name='lease',
            old_name='analyticsdata',
            new_name='analytics_data',
        ),
        migrations.RenameField(
            model_name='lease',
            old_name='analytics2',
            new_name='analytics_two',
        ),
        migrations.RenameField(
            model_name='lease',
            old_name='createdby',
            new_name='created_by',
        ),
        migrations.RenameField(
            model_name='lease',
            old_name='createdon',
            new_name='created_on',
        ),
        migrations.RenameField(
            model_name='lease',
            old_name='modifiedby',
            new_name='modified_by',
        ),
        migrations.RenameField(
            model_name='lease',
            old_name='modifiedon',
            new_name='modified_on',
        ),
        migrations.RemoveField(
            model_name='lease',
            name='pdf_hash',
        ),
        migrations.AddField(
            model_name='lease',
            name='file_hash',
            field=models.TextField(unique=True),
            preserve_default=False,
        ),
    ]
