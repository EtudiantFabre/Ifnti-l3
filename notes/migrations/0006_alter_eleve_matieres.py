# Generated by Django 4.1.2 on 2022-12-09 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Notes', '0005_alter_eleve_matieres'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eleve',
            name='matieres',
            field=models.ManyToManyField(to='Notes.matiere', verbose_name='Matières appartenant au niveau sélectionné '),
        ),
    ]
