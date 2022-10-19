"""Views for api endpoints."""


from django.db import transaction

from rest_framework import status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..serializers import (
    FN011WizardSerializer,
    FN022Serializer,
    FN026SimpleSerializer,
    FN028SimpleSerializer,
    ProjectGearProcessTypeSerializer,
)
from ..utils import (
    flatten_gear,
    check_distinct_seasons,
)


@api_view(["POST"])
@permission_classes([AllowAny])
def project_wizard(request):
    """

    This api_view endpoint only accepts post requests generated from
    the FN project wizard. the response is a structured json object
    that contain elements for FN011, FN022, FN026, FN028, gear, and
    associated process types.  The entire function is wrapped in a
    transaction and only commits the data to the data base is the
    entire objects can be successfully parsed and converted into
    django objects.

    If the data is valid and all of the entities can be created, it
    returns a 200 response.  If there is an error anywhere in the
    parsing/validation process, a bad request response is retruned
    along with the associated errros object.

    """

    def serializeAndSave(items, serializer, project):
        """A helper function to serialize, validate and save each of our child
        elements. If there is a issued validateding any of the elements, the
        trasaction is rollback and an error response is returned.

        Arguments:
        - `items`:
        - `serializer`:
        - `project`:

        """

        for item in items:
            item["project"] = project.slug
            serialized_item = serializer(data=item)
            if serialized_item.is_valid(raise_exception=True):
                serialized_item.save()

    def duplicateCheck(label, data, fields):
        "raise an error if any of the values in fields are duplicated."
        for field in fields:
            values = [x.get(field) for x in data]
            if len(values) != len(list(set(values))):
                msg = {label: f"Duplicate values found for {field}."}
                raise serializers.ValidationError(msg)

    def duplicateModeAttributes(data):
        "raise an error if any of the values in fields are duplicated."
        values = [f"{x['gear']}-{x['set_type']}-{x['orient']}" for x in data]
        if len(values) != len(list(set(values))):
            msg = {
                "fn028": "Combinations of gear, orient, and set_type must be unique."
            }
            raise serializers.ValidationError(msg)

    if request.method == "POST":

        data = request.data

        fn011 = FN011WizardSerializer(data=data["fn011"])
        fn022 = data.get("fn022", [])
        fn026 = data.get("fn026", [])
        fn028 = data.get("fn028", [])

        gears = flatten_gear(data.get("gear_array", []))

        try:
            with transaction.atomic():

                if fn011.is_valid(raise_exception=True):
                    project = fn011.save()

                if len(fn022):
                    duplicateCheck(
                        "fn022", fn022, ["ssn", "ssn_des", "ssn_date0", "ssn_date1"]
                    )
                    if check_distinct_seasons(fn022) is False:
                        msg = {"fn022": "Seasons must be distinct and cannot overlap."}
                        raise serializers.ValidationError(msg)

                    serializeAndSave(fn022, FN022Serializer, project)
                else:
                    msg = {"fn022": "At least one season must be specified"}
                    raise serializers.ValidationError(msg)

                if len(fn026):
                    duplicateCheck("fn026", fn026, ["space", "space_des"])
                    serializeAndSave(fn026, FN026SimpleSerializer, project)
                else:
                    msg = {"fn026": "At least one spatial strata must be specified"}
                    raise serializers.ValidationError(msg)

                if len(fn028):
                    duplicateCheck("fn028", fn028, ["mode", "mode_des"])
                    duplicateModeAttributes(fn028)
                    serializeAndSave(fn028, FN028SimpleSerializer, project)
                else:
                    msg = {"fn028": "At least one mode must be specified"}
                    raise serializers.ValidationError(msg)
                if len(gears):
                    serializeAndSave(gears, ProjectGearProcessTypeSerializer, project)
                else:
                    msg = {
                        "gear_array": "At least one gear and process type must be specified"
                    }
                    raise serializers.ValidationError(msg)

        except serializers.ValidationError as error:

            return Response(error.args, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"message": "Success!", "data": request.data},
            status=status.HTTP_201_CREATED,
        )
