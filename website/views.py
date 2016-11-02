import json
import urllib2

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Question

class IndexView(generic.ListView):
    template_name = 'site/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
                pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'site/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'site/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'site/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('site:results', args=(question.id,)))

def giphy(request, giphy_search):
    #Query giphy api here
    url = urllib2.urlopen('http://api.giphy.com/v1/gifs/search?q=' + giphy_search + '=&api_key=dc6zaTOxFJmzC')
    thing = json.load(url)
    images = []
    for i in thing['data']:
        for j in [i['images']['fixed_width']['url']]:
            images.append(j)
    giphy_json = images
    return render(request, 'site/giphy.html', {'giphy': giphy_json})