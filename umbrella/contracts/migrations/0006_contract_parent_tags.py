# Generated by Django 4.0.2 on 2022-04-21 12:09

from django.db import migrations, models
import django.db.models.deletion
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contracts', '0005_clause_kdp_alter_node_clause_alter_node_contract'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='contracts.contract'),
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('tag_group', models.CharField(blank=True, choices=[('nature', 'Nature'), ('type', 'Type'), ('groups', 'Groups'), ('others', 'Others')], max_length=128, null=True)),
                ('contract', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tags', to='contracts.contract')),
                ('user_groups', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tags', to='auth.group')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
