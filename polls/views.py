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
            return redirect('polls:start-game')

    else:
        form = SignUpForm()
    return render(request, "registration/sign_up.html", {'form': form})


@login_required
def highscores(request):
    return render(request, "polls/highscores.html", {'high_scores' : HighScores.objects.all().order_by('-highscore')})


@login_required
def start_game(request):
    return render(request, "polls/start-game.html")


@login_required
def save_game(request):
    score, _ = Score.objects.get_or_create(user=request.user)
    highscore, _ = HighScores.objects.get_or_create(user=request.user)
    if score.value > highscore.highscore:
        highscore.highscore = score.value
        highscore.save()
    score.value = 0
    score.save()
    return redirect('polls:highscores')


@login_required
def play_game(request):
    pig_position = PigPosition.objects.order_by('?').first()
    score, _ = Score.objects.get_or_create(user=request.user)
    if pig_position.url_name == "makinbacon":
        score.value = 0
    elif pig_position.url_name == "piggyback":
        score.value = 0
        score.save()
        return render(request, 'polls/game-over.html', {'score': score.value})
    else:
        score.value += pig_position.points
    score.save()
    return render(request, 'polls/play-game.html', {'pig_position': pig_position, 'score': score.value})


