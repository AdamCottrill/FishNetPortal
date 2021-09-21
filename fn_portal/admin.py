from django.contrib import admin

from fn_portal.models import FNProtocol, Gear, GearFamily, SubGear, Gear2SubGear


class Admin_FNProtocol(admin.ModelAdmin):
    """Admin class for FN Assessment Protcols"""

    search_fields = ["abbrev", "label"]
    list_display = ("abbrev", "label", "confirmed", "active")
    list_filter = ("confirmed", "active")
    exclude = ("description_html",)


class Admin_Gear(admin.ModelAdmin):
    """Admin class for Gears"""

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


class Admin_GearFamily(admin.ModelAdmin):
    """Admin class for Gear Families"""

    list_display = ("family", "abbrev", "gear_type")
    list_filter = ("gear_type",)


class Admin_SubGear(admin.ModelAdmin):
    """Admin class for SubGear"""

    list_display = ("eff", "grlen", "grht", "gryarn", "family")
    list_filter = ("eff", "gryarn", "family")


class Admin_Gear2SubGear(admin.ModelAdmin):
    """Admin class for Gear2SubGear table - allow us to edit the order
    of subgears"""

    list_display = (
        "__str__",
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

    def depreciated(self, obj):
        """ """
        return obj.gear.depreciated

    def mesh_mm(self, obj):
        """ """
        return obj.subgear.mesh

    def family(self, obj):
        """ """
        return obj.gear.family

    def gryarn(self, obj):
        """ """
        return obj.subgear.gryarn


admin.site.register(FNProtocol, Admin_FNProtocol)
admin.site.register(Gear, Admin_Gear)
admin.site.register(SubGear, Admin_SubGear)
admin.site.register(Gear2SubGear, Admin_Gear2SubGear)
admin.site.register(GearFamily, Admin_GearFamily)
