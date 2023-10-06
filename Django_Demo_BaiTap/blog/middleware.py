from django.shortcuts import render
import sys
from django.http import Http404
from blog.models import Blog1
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

class Blog1DeletedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # if request.path.startswith('/display/'):
        response = self.get_response(request)
        if request.method == 'POST' and 'delete_clicked' in request.POST:
                print("Deleted")
        if request.method == 'POST' and 'update_clicked' in request.POST:
                print("Updated")
        return response

