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

from .models import PigPosition, Score, HighScores
from .forms import SignUpForm


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('polls:index')

    else:
        form = SignUpForm()
    return render(request, "registration/sign_up.html", {'form': form})


@login_required
def index(request):
    pig_position = PigPosition.objects.order_by('?').first()
    score, _ = Score.objects.get_or_create(user=request.user)
    score.count += 1
    if pig_position.points == -1:
        score.value = 0
    elif pig_position.points == -2:
        score.value = 0
        return render(request, 'polls/game-over.html', {'score': score.value, 'high_scores': HighScores.objects.all()})
    else:
        score.value += pig_position.points
    score.save()
    if score.value >= 100:
        high_score, _ = HighScores.objects.get_or_create(user=request.user)
        if high_score.min_count > score.count:
            high_score.min_count = score.count
            high_score.save()
        current_score = score.value
        score.value = 0
        score.count = 0
        score.save()
        return render(request, 'polls/game-over.html', {'score': current_score, 'high_scores': HighScores.objects.all()})
    return render(request, 'polls/index.html', {'pig_position': pig_position, 'score': score.value})


