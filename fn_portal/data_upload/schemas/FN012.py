from .FN012Base import FN012Base


class FN012(FN012Base):
    """A validator for FN012 tables within a project. Exactly the same as
    the FN012 validator, with the addition of a project_id attribute (a
    required integer)"""

    project_id: int
