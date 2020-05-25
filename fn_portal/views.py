# from collections import Counter
# from django.http import HttpResponse

from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum, F, Count, Q
from django.views.generic import ListView
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect


# from django.core import serializers
from django.db import connection
import json

from datetime import datetime

from common.models import Lake

from .models import FN011, FN013, FN121, FN123, Gear, Species
from .forms import GearForm
from .filters import FN011Filter


# ==============================================
#             UTILS


def dictfetchall(cursor):
    """Return all rows from a cursor as a dict
    from: https://docs.djangoproject.com/en/1.10/topics/db/sql/"""

    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


class DateTimeEncoder(json.JSONEncoder):
    """to serialize dates using json.dumps.
    Copied from: http://stackoverflow.com/questions/11875770
    """

    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


# ==============================================
#            PROJECT VIEWS


class ProjectList(ListView):
    """
    """

    # modified to accept tag argument
    #
    filter_set = FN011Filter
    # filterset_class = FN011Filter
    template_name = "fn_portal/project_list.html"
    paginate_by = 50

    def get_queryset(self):

        search = self.request.GET.get("search")

        qs = FN011.objects.select_related("prj_ldr").all()

        if search:
            qs = qs.filter(Q(prj_cd__icontains=search) | Q(prj_nm__icontains=search))

        filtered_qs = FN011Filter(self.request.GET, qs)

        return filtered_qs.qs

    def get_context_data(self, **kwargs):
        """
        get any additional context information that has been passed in with
        the request.
        """

        context = super(ProjectList, self).get_context_data(**kwargs)

        context["filters"] = self.request.GET
        context["search"] = self.request.GET.get("search")
        context["first_year"] = self.request.GET.get("first_year")
        context["last_year"] = self.request.GET.get("last_year")

        lake_abbrev = self.request.GET.get("lake")
        if lake_abbrev:
            context["lake"] = Lake.objects.filter(abbrev=lake_abbrev).first()

        # need to add our factetted counts:
        qs = self.get_queryset()
        # calculate our facets by lake:
        lakes = (
            qs.select_related("lake")
            .all()
            .values(lakeName=F("lake__lake_name"), lakeAbbrev=F("lake__abbrev"))
            .order_by("lake")
            .annotate(N=Count("lake__lake_name"))
        )
        context["lakes"] = lakes

        project_source = (
            qs.values(name=F("source")).order_by("source").annotate(N=Count("source"))
        )

        context["project_source"] = project_source

        paginator = Paginator(self.object_list, self.paginate_by)
        page = self.request.GET.get("page")
        try:
            paged_qs = paginator.page(page)
        except PageNotAnInteger:
            paged_qs = paginator.page(1)
        except EmptyPage:
            paged_qs = paginator.page(paginator.num_pages)

        context["project_count"] = qs.count()
        context["object_list"] = paged_qs.object_list

        return context


def project_detail(request, slug):
    """This view is used to display the catch count information for a
    single project. The template contains linked, interactive maps and
    graphics.  Data for the map and graphics are provide by a complimentary json
    request (project_catch_counts2_json)

    Arguments:
    - `request`:

    """

    proj = FN011.objects.prefetch_related(
        "samples",
        "samples__effort",
        "samples__effort__catch",
        "samples__effort__catch__species",
    )

    project = get_object_or_404(proj, slug=slug)
    netsets = (
        FN121.objects.filter(project__slug=slug)
        .select_related("project")
        .order_by("project", "sam")
        .annotate(total_catch_count=Sum("effort__catch__catcnt"))
    )
    context = {"project": project, "netsets": netsets}

    return render(request, "fn_portal/project_detail.html", context)


def sample_detail(request, slug, sam):
    """

    Arguments:
    - `request`:
    - `slug`:
    - `sam`:

    """

    sample = get_object_or_404(FN121.objects.filter(project__slug=slug), sam=sam)
    context = {"sample": sample}
    return render(request, "fn_portal/sample_detail.html", context)


def project_catch_counts_json(request, slug):
    """

    Arguments:
    - `request`:
    """
    # catch by species for a project:
    # this is one that we will need:
    catchcounts = (
        FN123.objects.annotate(key=F("species__spc_nmco"))
        .annotate(project_code=F("effort__sample__project__prj_cd"))
        .values("key")
        .filter(effort__sample__project__slug=slug)
        .annotate(y=Sum("catcnt"))
        .order_by("key")
    )
    return JsonResponse(list(catchcounts), safe=False)


def sample_catch_counts_json(request, slug, sam):
    """

    Arguments:
    - `request`:
    """
    # catch by species for a project:
    # this is one that we will need:
    catchcounts = (
        FN123.objects.annotate(key=F("species__spc_nmco"))
        .values("key")
        .filter(effort__sample__project__slug=slug)
        .filter(effort__sample__sam=sam)
        .exclude(catcnt__isnull=True)
        .annotate(y=Sum("catcnt"))
        .order_by("key")
    )
    return JsonResponse(list(catchcounts), safe=False)


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

    catcnts = (
        FN123.objects.select_related(
            "effort", "species", "effort__sample", "effort_sample_project"
        )
        .annotate(prj_cd=F("effort__sample__project__prj_cd"))
        .annotate(sam=F("effort__sample__sam"))
        .annotate(eff=F("effort__eff"))
        .annotate(lift_date=F("effort__sample__effdt1"))
        .annotate(dd_lat=F("effort__sample__dd_lat"))
        .annotate(dd_lon=F("effort__sample__dd_lon"))
        .annotate(gear=F("effort__sample__gr"))
        .annotate(effst=F("effort__sample__effst"))
        .annotate(sidep=F("effort__sample__sidep"))
        .annotate(effdst=F("effort__effdst"))
        .annotate(grdep=F("effort__grdep"))
        .annotate(spc=F("species__spc_nmco"))
        .annotate(spc_code=F("species__spc"))
        .annotate(catch=F("catcnt"))
        .values(
            "prj_cd",
            "lift_date",
            "dd_lat",
            "dd_lon",
            "sam",
            "gear",
            "effst",
            "sidep",
            "eff",
            "grp",
            "effdst",
            "grdep",
            "spc",
            "spc_code",
            "catch",
        )
        .filter(effort__sample__project__slug=slug)
        .exclude(species__spc="000")
        .all()
    )

    return JsonResponse(list(catcnts), safe=False)


def project_spc_biodata(request, slug, spc):
    """This view is used to display the biological data for a
    particular species caught in a single project. The template
    contains linked, interactive graphics that can be used to filter
    the other figures.  The data for the graphics are provide by a
    complimentary json request (project_spc_biodata_json)

    Arguments:
    - `request`:
    - `slug`: a unique slug that identifies a project (lowercase project code)
    - `spc`: - a 2 or 3 digit MNR species code


    """

    project = get_object_or_404(FN011, slug=slug)
    species = get_object_or_404(Species, spc=spc)
    context = {"project": project, "species": species}

    return render(request, "fn_portal/project_spc_biodata.html", context)


def project_spc_biodata_json(request, slug, spc):
    """THis view returns the biological data for the species caught in a
    single project. Data is presented in the project spc_diodata
    template.  Data returned is a combination of the 121, 122, 123, and
    125 data for a SINGLE project.  The 121-123 data is used to filter
    the other records.

    Arguments:
    - `request`:
    - `slug`: a unique slug identifies a project (lowercase project code)
    - `spc`: - a 2 or 3 digit MNR species code

    """

    sql = """SELECT fn125.id, sam, grp,
               effdt1 as lift_date,
               fn011.year as yr,
               sidep,
               eff,
               species.spc,
               species.spc_nmco,
               flen, tlen, rwt, sex, mat, agea, xagem, clipc
          FROM fn_portal_fn125 fn125
                    left outer JOIN
               fn_portal_fn127 fn127 ON fn125.id = fn127.fish_id
                 JOIN
               fn_portal_fn123 fn123 ON fn123.id = fn125.catch_id
               JOIN
               fn_portal_fn122 fn122 ON fn122.id = fn123.effort_id
               JOIN
               fn_portal_fn121 fn121 ON fn121.id = fn122.sample_id
               JOIN
               fn_portal_fn011 fn011 ON fn011.id = fn121.project_id
               JOIN
               common_species species ON species.id = fn123.species_id
         WHERE fn011.slug = %s and species.spc=%s and (preferred=True or preferred is null)
         ORDER BY sam,
                  eff;
        """

    # cursor = connection.cursor()
    with connection.cursor() as cursor:
        cursor.execute(sql, [slug, spc])
        data = dictfetchall(cursor)

    return JsonResponse(data, safe=False)


def project_catch_over_time(request, slug):
    """Given a project slug, find all of the projects that have the same
    project prefix, project type and suffix (only the year changes)


    Arguments:
    - `request`:
    - `slug`:

    """

    project = get_object_or_404(FN011, slug=slug)
    slug_pattern = slug[:6] + "[0-9]{2}" + slug[8:]
    project_list = FN011.objects.filter(slug__regex=slug_pattern).all()

    context = {
        "project": project,
        "project_list": project_list,
        "slug_pattern": slug_pattern,
    }

    return render(request, "fn_portal/project_catch_over_time.html", context)


def project_catch_over_time_json(request, slug):
    """turns the catch count and effort information for all data matching
    a particular project code for trend through time.

    Data from this view is used in trend though time views/templates.

    Arguments:
    - `request`:

    """

    slug_pattern = slug[:6] + "[0-9]{2}" + slug[8:]

    # TODO - select_related

    catcnts = (
        FN123.objects.exclude(catcnt__isnull=True)
        .annotate(year=F("effort__sample__project__year"))
        .annotate(prj_cd=F("effort__sample__project__prj_cd"))
        .annotate(sam=F("effort__sample__sam"))
        .annotate(eff=F("effort__eff"))
        .annotate(lift_date=F("effort__sample__effdt1"))
        .annotate(dd_lat=F("effort__sample__dd_lat"))
        .annotate(dd_lon=F("effort__sample__dd_lon"))
        .annotate(gear=F("effort__sample__gr"))
        .annotate(effst=F("effort__sample__effst"))
        .annotate(sidep=F("effort__sample__sidep"))
        .annotate(effdst=F("effort__effdst"))
        .annotate(grdep=F("effort__grdep"))
        .annotate(spc=F("species__spc_nmco"))
        .annotate(spc_code=F("species__spc"))
        .annotate(catch=F("catcnt"))
        .values(
            "prj_cd",
            "lift_date",
            "year",
            "dd_lat",
            "dd_lon",
            "sam",
            "gear",
            "effst",
            "sidep",
            "eff",
            "grp",
            "effdst",
            "grdep",
            "spc",
            "spc_code",
            "catch",
        )
        .filter(effort__sample__project__slug__regex=slug_pattern)
        .all()
    )

    return JsonResponse(list(catcnts), safe=False)


# =================================================
#            GEAR VIEWS


def gear_list(request, username=None):
    """Return a simple list of Gears in our Gear table.

    Arguments:
    - `request`:
    - `slug`:
    """

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None

    if user:
        gear_list = Gear.objects.filter(assigned_to=user).order_by("gr_code")
    else:
        gear_list = Gear.objects.all().order_by("gr_code")

    context = {"gear_list": gear_list, "user": user}

    return render(request, "fn_portal/gear_list.html", context)


def edit_gear(request, gear_code):
    """A view that will allow us to edit our gear attributes."""

    gear = Gear.objects.filter(gr_code=gear_code).first()

    if request.method == "POST":
        form = GearForm(request.POST, instance=gear)
        if form.is_valid():
            gear = form.save()
            gear.gr_code = gear_code
            gear.save()
            return redirect("fn_portal:gear_detail", gear_code=gear.gr_code)
    else:
        form = GearForm(instance=gear)
        context = {"gear_code": gear_code, "form": form}
        return render(request, "fn_portal/gear_form.html", context)


def edit_subgear(request, gear_code, eff):
    """A view that will allow us to edit our gear attributes."""
    pass


def gear_detail(request, gear_code):
    """

    Arguments:
    - `request`:
    - `slug`:
    """

    gear = Gear.objects.filter(gr_code=gear_code).first()

    fn013_gear = FN013.objects.filter(gr=str(gear_code)).all()

    projects = (
        FN011.objects.filter(samples__gr=str(gear_code))
        .distinct()
        .annotate(N=Count("samples"))
    )

    context = {
        "fn013_gear": fn013_gear,
        "gear": gear,
        "gear_code": gear_code,
        "projects": projects,
    }
    return render(request, "fn_portal/gear_detail.html", context)
