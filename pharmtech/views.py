from django.shortcuts import render, render_to_response


def index(request):
    return render(request, 'homePage/index.html')