from .FN012Base import FN012BaseFactory


def FN012Factory(agest_choices):
    """A factory fucntion that will return a pydandic validator class
    that includes current valid agest choices.

    Arguments:
    - `agest_choices`:

    """

    FN012Base = FN012BaseFactory(agest_choices)

    class FN012(FN012Base):
        """A validator for FN012 tables within a project. Exactly the same as
        the FN012 validator, with the addition of a project_id attribute (a
        required integer)"""

        project_id: int

    return FN012
