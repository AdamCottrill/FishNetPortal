from rest_framework import permissions
from ..utils import is_admin
from ..models import FN011


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAdminUserOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        # is_admin = super(IsAdminUserOrReadOnly, self).has_permission(request, view)
        # Python3:
        is_admin = super().has_permission(request, view)
        return request.method in permissions.SAFE_METHODS or is_admin


class IsPrjLeadCrewOrAdminOrReadOnly(permissions.BasePermission):
    """A custom permission class that will only allow the project lead,
    project crew, or a site administrator access the endpoint (for
    creating, updating or deleting project objects), but return false for others.

    """

    def is_project_lead_or_crew(self, request, view):
        """
        """
        prj_cd = view.kwargs.get("prj_cd")

        if prj_cd is None:
            slug = view.kwargs.get("slug", "")
            prj_cd = slug[:12]
        print("prj_cd={}".format(prj_cd))
        project = FN011.objects.get(slug=prj_cd.lower())

        return (
            request.user == project.prj_ldr or request.user in project.field_crew.all()
        )

    def has_permission(self, request, view):
        """
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return self.is_project_lead_or_crew(request, view)

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return self.is_project_lead_or_crew(request, view)

        # else:
        #     prj_cd = view.kwargs.get("prj_cd")
        #     project = FN011.objects.get(prj_cd=prj_cd)
        #     return (
        #         request.user == project.prj_ldr
        #         or request.user in project.field_crew.all()
        #     )
