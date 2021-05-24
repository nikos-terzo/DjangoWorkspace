from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
# @login_required
def index(request):
	resp = """<!DOCTYPE html>
<html>
	<header></header>
	<body>
    <p>Hello</p>
	</body>
</html>"""
	return HttpResponse(resp)