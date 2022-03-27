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
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import PigPosition, Score
from .forms import SignUpForm


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('wordchain:home')

    else:
        form = SignUpForm()
    return render(request, "registration/sign_up.html", {'form': form})


@login_required
def index(request):
    pig_position = PigPosition.objects.order_by('?').first()
    score, _ = Score.objects.get_or_create(user=request.user)
    if pig_position.points < 0:
        score.value = 0
    else:
        score.value += pig_position.points
    score.save()
    return render(request, 'polls/index.html', {'pig_position': pig_position, 'score': score.value})


