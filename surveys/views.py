from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .forms import NewCommentForm
from django.http import HttpResponse
from .models import *

def home(request):
    # surveys = get_list_or_404(Survey)
    surveys = Survey.objects.all()

    fields = [field.name for field in Source._meta.get_fields()]
    fields.remove('comments')  # to not show foreignkey - comments on home page
    return render(request, 'home.html', {'surveys': surveys, 'fields': fields})

def source(request, pk):
    surveys = get_list_or_404(Survey)
    source_f = get_object_or_404(Source, pk=pk)  # get object-source chosen by user on main page
    dup_sources = Source.objects.filter(dup_id=source_f.dup_id)  # get all object-sources related to this source
    user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        source_id = request.POST.get('source_id', None)  # get from hidden field source pk for current tab
        source = dup_sources.get(pk=source_id)  # get current object-source

        # Make master source-object or make normal
        if request.POST.get('master', False):
            # to prevent from getting several master sources
            if not source.master_source:
                for src in list(dup_sources.filter(master_source=True)):
                    src.master_source = False
                    src.save()

            source.master_source = False if source.master_source else True
            source.save()

        # Create/Edit comment
        else:
            form = NewCommentForm(request.POST)  # use existing or created comment

            if form.is_valid():
                comment = form.save(commit=False)
                comment.source = source
                comment.created_by = user
                comment.save()

                if source.master_source:
                    source.comment = comment
                    source.source_class = comment.source_class
                    source.save()

        return redirect('source', pk=source_id)  # TODO: redirect to the created topic page
    else:
        form = NewCommentForm()
    return render(request, 'source.html', {'surveys': surveys, 'source_f': source_f, 'dup_sources': dup_sources, 'form': form})