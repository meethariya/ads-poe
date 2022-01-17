from django.shortcuts import render, redirect
from . import store

# Create your views here.
def home(request):
    dictionary={}
    if request.method == 'POST':
        data = request.POST
        button = data.get('action')
        if button == "Partition":
            partitions = int(data.get('partitions'))
            dictionary = store.rrpartition(partitions)
        elif button == "Reset":
            dictionary = store.reset_partition()
    # fetching all database info
    info = store.infor()
    # merging dictionary
    dictionary = dictionary|info
    return render(request, 'rrpartition/home.html',dictionary)

def search(request):
    dictionary = {}
    if request.method == 'POST':
        data = request.POST
        button = data.get('action')
        if button == 'Search':
            eid = int(data.get('eid'))
            dictionary = store.search(eid)
            print(eid)
        elif button == "Home":
            return redirect('/')
    return render(request, 'rrpartition/search.html', dictionary)