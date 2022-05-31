from django.conf import settings
from django.urls import URLPattern, URLResolver

import django_settings

urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [""])


def list_urls2(lis, acc=None):
    if acc is None:
        acc = []
    if not lis:
        return
    x = lis[0]

    if isinstance(x, URLPattern):
        print("URLPattern: ", dir(x))
        yield acc + [x.name, str(x.pattern)]
    elif isinstance(x, URLResolver):
        yield from list_urls2(
            x.url_patterns, acc + [x.app_name, x.namespace, str(x.pattern)]
        )
    yield from list_urls2(lis[1:], acc)



urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [""])
for x in urlconf.urlpatterns:
    print(x.url_patterns)



 urls = urlresolvers.get_resolver()


def func_for_sorting(i):
    if i.name is None:
        i.name = ''
    return i.name

all_urls = list()
def show_urls(urls):
    for url in urls.url_patterns:
        if isinstance(url, URLResolver):
            show_urls(url)
        elif isinstance(url, URLPattern):
            all_urls.append(url)
show_urls(urlconf)


all_urls.sort(key=func_for_sorting, reverse=False)



for p in list_urls2(urlconf.urlpatterns):
    print("".join(p))




from django.db.models import Q

from fn_portal.models import FN026, FN028, FN121

# update ssn where ssn is null:
# samples = FN121.objects.filter(ssn__isnull=True)
# for sample in samples:
#     sample.save()

#make sure that all gear codes are accounted for
# if not - make dummy records in the Gear table
# ensure that modes exist for all gear-orient-gruse combinations in FN121
# populate fk in Fn121 ssn, space, and mode
# drop fn121 gr, grtp, orient.

missing_modes = []
missing_spaces = []

mode_cache = {f"{x.project_id}-{x.gr.gr_code}-{x.orient}-{x.gruse}":x
            for x in FN028.objects.select_related('gr').all()}
space_cache = {x.project_id:x for x in FN026.objects.all()}

for sample in samples:
    orient = sample.orient if sample.orient else '9'
    mode_key = f"{sample.project_id}-{sample.gr}-{orient}-1"
    mode = mode_cache.get(mode_key)
    if mode:
        sample.mode = mode
    else:
        missing_modes.append(mode_key)
    space = space_cache.get(sample.project_id)

    if space:
        sample.space=space
    else:
        missing_spaces.append(sample.project.prj_cd)
    sample.save()




# print(f"Done. Found {len(missing_spaces)} samples without a space.")




from django.contrib.auth import get_user_model
from common.models import Lake, Species, Grid5

from fn_portal.models import Gear

User = get_user_model()



lake_cache = {x['abbrev']:x['id'] for x in Lake.objects.values('abbrev', 'id')}
species_cache = {x['spc']:x['id'] for x in Species.objects.values('spc', 'id')}
grid5_cache = {x['slug']:x['id'] for x in Grid5.objects.filter(lake__abbrev='HU').values('slug', 'id')}
user_cache =  {x['username'].upper():x['id'] for x in User.objects.values('username', 'id')}

foo = User.objects.all()
for x in foo:
    user_cache[f'{x.first_name.upper()} {x.last_name.upper()}'] = x.id


from fn_portal.models import FNProtocol
protocol_cache = {x['abbrev']:x['id'] for x in FNProtocol.objects.values('abbrev', 'id')}

gear_cache = {x['gr_code']:x['id'] for x in Gear.objects.values('gr_code', 'id')}



import django_settings
from django.db.models import Min, Max, F
from fn_portal.models import FN011, FN022, FN026, FN121


#get first and last date for each project:
foo = FN121.objects.values('project__prj_cd').annotate(ssn_date0=Min('effdt0'),
                                                 ssn_date1=Max('effdt1')).filter(effdt0=F('ssn_date0'),
                                                                                 effdt1=F('ssn_date1')).distinct("project__prj_cd")

for x in foo[:4]:
    print(x)




import django_settings
from django.db.models import OuterRef, Subquery, Count, Sum
from fn_portal.models import FN011, FN123, FN125




prj_cd = 'LHA_IA19_006'


biocnts = (FN125.objects.filter(catch=OuterRef('pk')).order_by()
           .values('catch_id')
           .annotate(biocnt=Count('*'))
           .values('biocnt')
           )

fn123 = FN123.objects.filter(effort__sample__project__prj_cd=prj_cd).update(
    biocnt=Subquery(biocnts)
)





from django.db.models import OuterRef, Subquery, Count, Sum
from fn_portal.models import FN011, FN123, FN125


fn011s = (FN011.objects.all()
         .annotate(biocnt=Sum('samples__effort__catch__biocnt'))
          .filter(biocnt__isnull=True)
          .values_list('prj_cd')
          )

prj_cds = [x[0] for x in fn011s]


biocnts = (
    FN125.objects.filter(catch=OuterRef("pk"))
    .order_by()
    .values("catch_id")
    .annotate(biocnt=Count("*"))
    .values("biocnt")
)
FN123.objects.filter(
    effort__sample__project__prj_cd__in=prj_cds
).update(biocnt=Subquery(biocnts))
print("Done!")




foo.filter(species__spc__in=[
    "334",
"131",
"093",
"091"
]).update(agedec1="X", agedec2='0')

foo.filter(species__spc__in=[
    "331",
"316",
"121"
]).update(agedec1="1", agedec2='0')
