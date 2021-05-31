
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def userProfile(request):
	context = {'user': request.user}
	return render(request, 'registration/profile.html', context)