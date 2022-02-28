from django.contrib import admin

from fn_portal.models import (
    FN011,
    FN012,
    FN012Protocol,
    FNProtocol,
    Gear,
    GearFamily,
    SubGear,
    Gear2SubGear,
    GearEffortProcessType,
)


class Admin_FN011(admin.ModelAdmin):
    """Admin class for Projects (FN011)"""

    search_fields = ["prj_nm", "prj_cd"]
    list_display = ("prj_cd", "prj_nm", "prj_ldr", "prj_date0", "prj_date1")
    list_filter = ("lake", "protocol", "year")
    date_hierarchy = "prj_date0"

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("prj_cd",)
        return self.readonly_field


class Admin_FN012(admin.ModelAdmin):
    """Admin class for Species Sampling Specs (FN012)"""

    search_fields = ["project__prj_cd", "species__spc", "species__spc_nmco"]
    list_display = ("get_prj_cd", "species", "grp", "grp_des", "biosam")
    list_filter = ("species__spc", "grp")
    exclude = ("slug",)

    fields = [
        "project",
        "species",
        "grp",
        "grp_des",
        "biosam",
        "sizsam",
        "sizatt",
        "sizint",
        "fdsam1",
        "fdsam2",
        "spcmrk1",
        "spcmrk2",
        "agedec1",
        "agedec2",
        "flen_min",
        "flen_max",
        "tlen_min",
        "tlen_max",
        "rwt_min",
        "rwt_max",
        "k_min_error",
        "k_min_warn",
        "k_max_error",
        "k_max_warn",
        "flen2tlen_alpha",
        "flen2tlen_beta",
    ]

    def get_queryset(self, request):
        return (
            super(Admin_FN012, self)
            .get_queryset(request)
            .select_related("project", "species")
        )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("project", "species", "grp")
        return self.readonly_fields

    def get_prj_cd(self, obj):
        return obj.project.prj_cd


class Admin_FN012Protocol(admin.ModelAdmin):
    """Admin class for Protocol Species Sampling Specs (FN012)"""

    search_fields = [
        "lake__abbrev",
        "protocol__label",
        "species__spc",
        "species__spc_nmco",
    ]
    list_display = (
        "species",
        "grp",
        "grp_des",
        "lake",
        "protocol",
        "biosam",
    )
    list_filter = ("lake__abbrev", "species__spc", "grp", "protocol")
    exclude = ("slug",)

    fields = [
        "protocol__abbrev",
        "lake",
        "species",
        "grp",
        "grp_des",
        "biosam",
        "sizsam",
        "sizatt",
        "sizint",
        "fdsam1",
        "fdsam2",
        "spcmrk1",
        "spcmrk2",
        "agedec1",
        "agedec2",
        "flen_min",
        "flen_max",
        "tlen_min",
        "tlen_max",
        "rwt_min",
        "rwt_max",
        "k_min_error",
        "k_min_warn",
        "k_max_error",
        "k_max_warn",
        "flen2tlen_alpha",
        "flen2tlen_beta",
    ]

    def get_queryset(self, request):
        return (
            super(Admin_FN012Protocol, self)
            .get_queryset(request)
            .select_related("lake", "protocol", "species")
        )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("protocol", "lake", "species", "grp")
        return self.readonly_fields


class Admin_FNProtocol(admin.ModelAdmin):
    """Admin class for FN Assessment Protcols"""

    search_fields = ["abbrev", "label"]
    list_display = ("abbrev", "label", "confirmed", "active")
    list_filter = ("confirmed", "active")
    exclude = ("description_html",)


class Admin_Gear(admin.ModelAdmin):
    """Admin class for Gears"""

    search_fields = ["gr_code", "gr_label"]
    list_display = (
        "gr_label",
        "gr_code",
        "family",
        "confirmed",
        "depreciated",
        "assigned_to",
    )
    list_filter = ("family", "confirmed", "depreciated", "assigned_to")
    exclude = ("gr_des_html",)


class Admin_GearProcessType(admin.ModelAdmin):
    """Admin class for known process types associated with each gear"""

    list_display = ("gear", "gear_code", "eff", "process_type", "effdst")
    list_filter = ("process_type", "eff", "gear")
    search_fields = ["gear__gr_code", "gear__gr_label"]

    def gear_code(self, obj):
        """ """
        return obj.gear.gr_code


class Admin_GearFamily(admin.ModelAdmin):
    """Admin class for Gear Families"""

    list_display = ("family", "abbrev", "gear_type")
    list_filter = ("gear_type",)


class Admin_SubGear(admin.ModelAdmin):
    """Admin class for SubGear"""

    search_fields = ["mesh"]

    list_display = ("eff", "grlen", "grht", "gryarn", "family")
    list_filter = ("eff", "gryarn", "family")


class Admin_Gear2SubGear(admin.ModelAdmin):
    """Admin class for Gear2SubGear table - allow us to edit the order
    of subgears"""

    search_fields = ["gear__gr_code", "gear__gr_label", "subgear__mesh"]

    list_display = (
        "__str__",
        "eff",
        "panel_sequence",
        "panel_count",
        "mesh_mm",
        "family",
        "depreciated",
        "gryarn",
    )
    list_filter = (
        "gear__family",
        "gear__depreciated",
        "subgear__gryarn",
        "gear__gr_code",
    )

    def get_queryset(self, request):
        return (
            super(Admin_Gear2SubGear, self)
            .get_queryset(request)
            .select_related("gear", "subgear", "subgear__family", "gear__family")
        )

    def depreciated(self, obj):
        """ """
        return obj.gear.depreciated

    def eff(self, obj):
        """ """
        return obj.subgear.eff

    def mesh_mm(self, obj):
        """ """
        return obj.subgear.mesh

    def family(self, obj):
        """ """
        return obj.gear.family

    def gryarn(self, obj):
        """ """
        return obj.subgear.gryarn


admin.site.register(FN011, Admin_FN011)
admin.site.register(FN012, Admin_FN012)
admin.site.register(FN012Protocol, Admin_FN012Protocol)
admin.site.register(FNProtocol, Admin_FNProtocol)
admin.site.register(Gear, Admin_Gear)
admin.site.register(GearEffortProcessType, Admin_GearProcessType)
admin.site.register(SubGear, Admin_SubGear)
admin.site.register(Gear2SubGear, Admin_Gear2SubGear)
admin.site.register(GearFamily, Admin_GearFamily)
