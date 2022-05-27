from .common_views import SpeciesListView, ProjectLeadListView, LakeExtentListView

from .gear_views import GearListView, GearEffortProcessTypeListView

from .FN0_views import (
    FNProtocolListView,
    FN011ListView,
    FN011DetailView,
    FN012ListView,
    FN012ProtocolListView,
    FN013ListView,
    FN013DetailView,
    FN014ListView,
    FN014DetailView,
    FN022ListView,
    FN022DetailView,
    FN026ListView,
    FN026DetailView,
    FN028ListView,
    FN028DetailView,
)


from .FN1_views import (
    # ProjectWizardCreateProject,
    project_wizard,
    NetSetList,
    FN121LimnoList,
    EffortList,
    CatchCountList,
    LengthTallyList,
    BioSampleList,
    FN125TagReadOnlyList,
    FN125LampreyReadOnlyList,
    FN126ReadOnlyList,
    FN127ReadOnlyList,
    # CRUD Endpoints:
    FN121ListView,
    FN121DetailView,
    FN122ListView,
    FN122DetailView,
    FN123ListView,
    FN123DetailView,
    FN125ListView,
    FN125DetailView,
)
