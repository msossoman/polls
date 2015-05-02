from django.shortcuts import get_object_or_404, render # import 2 shortcut modules for use with requests
from django.http import HttpResponseRedirect # imports 'HttpResponseRedirect' module to specify path to redirect to after voting on poll choice
from django.core.urlresolvers import reverse # imports 'reverse' module so URLs can be called using namespaces instead of the full URL; also allows URL to be changed without having to go back and change all references to the URL in multiple places within project and app code 
from django.views import generic # imports 'generic' module so generic class-based views can be accessed
from django.utils import timezone # imports 'timezone' module so now() function can be accessed

from .models import Choice, Question # imports 'Choice' and 'Question' models that were created for polls app

class IndexView(generic.ListView): # creates class object that will define the view for polls/index.html as a generic ListView, which uses a template for a page that contains a list of objects.
	template_name = 'polls/index.html' # replaces the ListView default template with the index.html template created for polls app
	context_object_name = 'latest_question_list' # defines the name of the context object in a more "user-friendly" term 

	def get_queryset(self): # function that will get the 'set' of question objects when a 'query' for those objects is made
		return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5] # filters query results to only include 5 question objects published in the past, and it sorts them by date published

class DetailView(generic.DetailView): # creates class object that will define the view for polls/details.html as a generic DetailView, which uses a template for a page that contains the specified object
	model = Question # specifies that Question is the model being acted upon
	template_name = 'polls/detail.html' # replaces the DetailView default template with the detail.html template created for polls app

	def get_queryset(self): # same as above in IndexView
		return Question.objects.filter(pub_date__lte=timezone.now()) # same as above in IndexView without sorting latest 5 question objects

class ResultsView(generic.DetailView): # creates class object that will define the view for polls/results.html as a generic DetailView
	model = Question # specifies that Question is the model being acted upon
	template_name = 'polls/results.html' # replaces the DetailView default template with the results.html template created for polls app

def vote(request, question_id): # creates function that will handle voting for question choices
	p = get_object_or_404(Question, pk=question_id) # defines variable using get_object_or_404 shortcut method; accepts 2 arguments - 1st points to Question model, and 2nd points to a particular question using it's id
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice']) # uses POST method to make changes on the server based on the users vote
	except (KeyError, Choice.DoesNotExist): # except statement returns an error message if user didn't submit vote, and it takes user back to detail view so they can try another vote
		return render(request, 'polls/detail.html', {
			'question': p,
			'error_message': "You didn't select a choice.",
			})
	else: # performs methods below if the above exception is not raised
		selected_choice.votes += 1 # increments vote total by 1 for the choice the user selected
		selected_choice.save() # saves the users vote
		return HttpResponseRedirect(reverse('polls:results', args=(p.id,))) # redirects the user to the polls/results.html URL for the question they just voted on