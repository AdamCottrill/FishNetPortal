
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Sum,F
from django.http import JsonResponse
from django.template import RequestContext

#import json

from fn_portal.models import *


def project_list(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def project_detail(request, slug):
    """

    Arguments:
    - `request`:
    - `slug`:
    """

    project = get_object_or_404(FN011, slug=slug)

    return render_to_response('fn_portal/project_detail.html',
                              {'project': project},
                              context_instance=RequestContext(request))



def sample_detail(request, slug, sam):
    """

    Arguments:
    - `request`:
    - `slug`:
    - `sam`:

    """

    project = get_object_or_404(FN011, slug=slug)
    sample = get_object_or_404(FN121, project=project, sam=sam)

    return render_to_response('fn_portal/project_detail.html',
                              {'sample': sample},
                              context_instance=RequestContext(request))



def project_catch_counts(request, prj_cd):
    """

    Arguments:
    - `request`:
    """

    project = get_object_or_404(FN011, prj_cd=prj_cd)

    return render_to_response('fn_portal/project_detail.html',
                              {'project': project},
                              context_instance=RequestContext(request))


def project_catch_counts_json(request, slug):
    """

    Arguments:
    - `request`:
    """
    #catch by species for a project:
    #this is one that we will need:
    catchcounts = FN123.objects.annotate(key=F('species__common_name')).\
                  annotate(project_code=F('effort__sample__project__prj_cd')).\
                  values('key').\
                  filter(effort__sample__project__slug=slug).\
                  annotate(y=Sum('catcnt')).order_by('key')
    return JsonResponse(list(catchcounts), safe=False)


def sample_catch_counts_json(request, slug, sam):
    """

    Arguments:
    - `request`:
    """
    #catch by species for a project:
    #this is one that we will need:
    catchcounts = FN123.objects.annotate(key=F('species__common_name')).\
                  values('key').\
                  filter(effort__sample__project__slug=slug).\
                  filter(effort__sample__sam=sam).\
                  annotate(y=Sum('catcnt')).order_by('key')
    return JsonResponse(list(catchcounts), safe=False)
