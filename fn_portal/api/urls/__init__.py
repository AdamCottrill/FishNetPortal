from .CommonLists import urlpatterns as common_urls
from .FN011 import urlpatterns as fn011_urls
from .FN012 import urlpatterns as fn012_urls
from .FN013 import urlpatterns as fn013_urls
from .FN014 import urlpatterns as fn014_urls
from .FN022 import urlpatterns as fn022_urls
from .FN026 import urlpatterns as fn026_urls
from .FN028 import urlpatterns as fn028_urls
from .FN121 import urlpatterns as fn121_urls
from .FN122 import urlpatterns as fn122_urls
from .FN123 import urlpatterns as fn123_urls
from .FN124 import urlpatterns as fn124_urls
from .FN125 import urlpatterns as fn125_urls
from .FN126 import urlpatterns as fn126_urls
from .FN127 import urlpatterns as fn127_urls

urlpatterns = []

urlpatterns.extend(common_urls)
urlpatterns.extend(fn011_urls)
urlpatterns.extend(fn012_urls)
urlpatterns.extend(fn013_urls)
urlpatterns.extend(fn014_urls)

urlpatterns.extend(fn022_urls)
urlpatterns.extend(fn026_urls)
urlpatterns.extend(fn028_urls)
urlpatterns.extend(fn121_urls)
urlpatterns.extend(fn122_urls)
urlpatterns.extend(fn123_urls)
urlpatterns.extend(fn124_urls)
urlpatterns.extend(fn125_urls)
urlpatterns.extend(fn126_urls)
urlpatterns.extend(fn127_urls)
