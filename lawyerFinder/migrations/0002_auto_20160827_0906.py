# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lawyerFinder', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webstaticcontents',
            name='contents',
            field=models.CharField(max_length=65536),
        ),
    ]
