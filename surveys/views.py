from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .forms import NewCommentForm, OptCommentForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import *


@login_required
def home(request):
    # surveys = get_list_or_404(Survey)
    surveys = Survey.objects.all()
    return render(request, 'home.html', {'surveys': surveys, 'fields': Survey.get_fields_to_show()})


def get_opt_master_sources(opt_sources):
    opt_names = []
    for survey_sources in opt_sources:
        if survey_sources and survey_sources.filter(master_source=True).exists():
            opt_names.append(survey_sources.filter(master_source=True)[0].name)
        else:
            opt_names.append(None)
    return tuple(opt_names)


def handle_comment_request(request, prim_source, opt_sources):
    # Create/Edit comment for XRAY SOURCE
    if 'x_comment' in request.POST:
        # Edit existing comment or create new one
        try:
            comment = Comment.objects.get(source=prim_source, created_by=request.user)
            comment.updated_at = datetime.now()
        except Comment.DoesNotExist:
            comment = Comment.objects.create(comment='create', source=prim_source, created_by=request.user)

        form = NewCommentForm(request.POST, instance=comment)  # use existing or created comment
        if form.is_valid():
            form.save()
            comment.save()

    # Create/Edit comment for OPTICAL OBJECT
    elif 'opt_comment' in request.POST:
        # Edit existing comment or create new one
        try:
            opt_comment = OptComment.objects.get(source=prim_source, created_by=request.user)
            opt_comment.updated_at = datetime.now()
        except OptComment.DoesNotExist:
            opt_comment = OptComment.objects.create(comment='create', source=prim_source, created_by=request.user)

        opt_form = OptCommentForm(request.POST, instance=opt_comment)
        if opt_form.is_valid():
            opt_form.save()
            opt_comment.master_ls, opt_comment.master_gaia, opt_comment.master_ps = get_opt_master_sources(opt_sources)
            opt_comment.save()


def handle_status_request(request, prim_source, opt_dict):
    # Make 'master' source-object or normal
    if 'master' in request.POST and request.user.is_superuser:
        prim_source.master_source = False if prim_source.master_source else True
        prim_source.save()

    # Make superuser comment final for xray_source by superuser
    elif 'final' in request.POST and request.user.is_superuser:
        comment = prim_source.comments.get(created_by=request.user)
        prim_source.comment = comment.comment
        prim_source.source_class = comment.source_class
        prim_source.save()

    # Make optical source 'master' or normal for xray source
    elif 'opt_master' in request.POST and request.user.is_superuser:
        # get survey and id of requested opt source
        opt_source_id = request.POST.get('opt_source_id')
        opt_source_type = request.POST.get('opt_source_type')
        # get requested source and change its 'master' status
        opt_source = opt_dict[opt_source_type].get(pk=opt_source_id)
        # update all opt sources from same survey and same xray source
        if opt_source.master_source:
            opt_source.master_source = False
            opt_source.meta_object = None
            opt_source.save()
        else:
            opt_source.master_source = True
            opt_source.meta_object = prim_source.meta_object  # important to make this link
            opt_source.save()
            # TODO: think about this update
            opt_dict[opt_source_type].exclude(pk=opt_source_id).update(master_source=False, meta_object=None)

    # Make optical source 'probable' or normal for xray source
    elif 'probable_master' in request.POST and request.user.is_superuser:
        pass


@login_required
def source(request, pk):
    # for parsing source fields on source page
    postfixes = ['_e1', '_e2', '_e3', '_e4', '_e5', '_e6', '_e7', '_e8']
    base_fields = [field.name for field in Source._meta.get_fields() if not field.name[-3:] in postfixes]
    # opt_surveys = ['LS', 'GAIA', 'PS1', 'SDSS', 'WISE']
    opt_surveys = ['LS', 'GAIA', 'PS1']

    surveys = get_list_or_404(Survey)
    prim_source = get_object_or_404(Source, pk=pk)  # get object-source chosen by user on main page
    dup_sources = prim_source.meta_object.object_sources.all()  # get all object-sources related to this source

    # get list of query sets - optical sources from different surveys
    opt_sources = []
    for s_name in opt_surveys:
        opt_sources.append(Source.get_opt_survey_sources(prim_source, s_name))

    # zip surveys and corresponding optical sources for template nested nav-tabs
    opt_survey_sources = dict(zip(opt_surveys, opt_sources))
    # TODO: make flat array from list of query sets
    opt_sources_flat = sum([list(opt_s) for opt_s in opt_sources if opt_s], [])

    if request.method == 'POST':
        # Handle all cases of POST method
        if ('x_comment' in request.POST) or ('opt_comment' in request.POST):
            # Handle xray/opt comment cases of POST method
            handle_comment_request(request, prim_source, opt_sources)

        else:
            # Handle status cases of POST method - master/final comment/probable
            handle_status_request(request, prim_source, opt_survey_sources)
        return redirect('source', pk=prim_source.pk)

    else:
        # create form for xray source
        form = NewCommentForm()
        # create form for optical source
        opt_form = OptCommentForm()

    return render(request, 'source.html', {'surveys': surveys, 'source': prim_source, 'base_fields': base_fields,
                                           'dup_sources': dup_sources, 'form': form,
                                           'opt_form': opt_form, 'opt_surveys': opt_surveys,
                                           'opt_sources': opt_sources_flat, 'opt_survey_sources': opt_survey_sources})
