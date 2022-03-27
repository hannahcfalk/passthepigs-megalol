# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.db import models
from django.contrib.auth.models import User


class PigPosition(models.Model):
    name = models.CharField(max_length=50)
    url_name = models.CharField(max_length=50)
    points = models.IntegerField()
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class Score(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    value = models.IntegerField(default=0)
