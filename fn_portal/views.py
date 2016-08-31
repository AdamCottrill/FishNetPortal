
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





def project_catch_counts2(request, slug):
    """This view is used to display the catch count information for a
    single project. The template contains linked, interactive maps and
    graphics.  Data for the map and graphics are provide by a complimentary json
    request (project_catch_counts2_json)

    Arguments:
    - `request`:

    """

    project = get_object_or_404(FN011, slug=slug)

    return render_to_response('fn_portal/project_detail2.html',
                              {'object': project},
                              context_instance=RequestContext(request))




def project_catch_counts2_json(request, slug):
    """THis view returns the catch count data for the project detail
    pages.  Data returned is a combination of the 121, 122 and 123 data
    for a SINGLE project.

    records with spc_code of 0 ('000') are excluded because they do
    not actually contain any catch information - they are only used to
    provide effort in cpue calculations.

    Arguments:
    - `request`:
    - `slug`: a unique slug identifies a project (lowercase project code)

    """

    catcnts = FN123.objects.\
          annotate(prj_cd=F('effort__sample__project__prj_cd')).\
          annotate(sam=F('effort__sample__sam')).\
          annotate(eff=F('effort__eff')).\
          annotate(lift_date=F('effort__sample__effdt1')).\
          annotate(dd_lat=F('effort__sample__dd_lat')).\
          annotate(dd_lon=F('effort__sample__dd_lon')).\
          annotate(gear=F('effort__sample__gr')).\
          annotate(effst=F('effort__sample__effst')).\
          annotate(sidep=F('effort__sample__sidep')).\
          annotate(effdst=F('effort__effdst')).\
          annotate(grdep=F('effort__grdep')).\
          annotate(spc=F('species__common_name')).\
          annotate(spc_code=F('species__species_code')).\
          annotate(catch=F('catcnt')).\
          values('prj_cd','lift_date', 'dd_lat', 'dd_lon', 'sam', 'gear',
                 'effst', 'sidep', 'eff', 'grp', 'effdst', 'grdep', 'spc',
                 'spc_code', 'catch').\
          filter(effort__sample__project__slug=slug).\
          exclude(spc_code=0).all()

    return JsonResponse(list(catcnts), safe=False)





def project_catch_over_time(request, slug):
    """Given a project slug, find all of the projects that have the same
    project prefix, project type and suffix (only the year changes)


    Arguments:
    - `request`:
    - `slug`:

    """

    project = get_object_or_404(FN011, slug=slug)
    slug_pattern = slug[:6] + '[0-9]{2}' + slug[8:]
    project_list = FN011.objects.filter(slug__regex=slug_pattern).all()

    return render_to_response('fn_portal/project_catch_over_time.html',
                              {'project': project,
                               'project_list': project_list,
                               'slug_pattern': slug_pattern},
                              context_instance=RequestContext(request))




def project_catch_over_time_json(request, slug):
    """turns the catch count and effort information for all data matching
    a particular project code for trend through time.

    Data from this view is used in trend though time views/templates.

    Arguments:
    - `request`:

    """

    slug_pattern = slug[:6] + '[0-9]{2}' + slug[8:]

    catcnts = FN123.objects.\
          annotate(year=F('effort__sample__project__year')).\
          annotate(prj_cd=F('effort__sample__project__prj_cd')).\
          annotate(sam=F('effort__sample__sam')).\
          annotate(eff=F('effort__eff')).\
          annotate(lift_date=F('effort__sample__effdt1')).\
          annotate(dd_lat=F('effort__sample__dd_lat')).\
          annotate(dd_lon=F('effort__sample__dd_lon')).\
          annotate(gear=F('effort__sample__gr')).\
          annotate(effst=F('effort__sample__effst')).\
          annotate(sidep=F('effort__sample__sidep')).\
          annotate(effdst=F('effort__effdst')).\
          annotate(grdep=F('effort__grdep')).\
          annotate(spc=F('species__common_name')).\
          annotate(spc_code=F('species__species_code')).\
          annotate(catch=F('catcnt')).\
          values('prj_cd','lift_date', 'year', 'dd_lat', 'dd_lon', 'sam',
                 'gear', 'effst', 'sidep', 'eff', 'grp', 'effdst', 'grdep',
                 'spc', 'spc_code', 'catch').\
          filter(effort__sample__project__slug__regex=slug_pattern).all()

    return JsonResponse(list(catcnts), safe=False)
