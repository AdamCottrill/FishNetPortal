from .FN012Base import FN012Base


class FN012Protocol(FN012Base):
    """A validator for FN012 objects within a protocol. Exactly the same
    as the FN012 validator, with the addition of a protocol_id and
    lake_id attributes (required integers)
    """

    lake_id: int
    protocol_id: int
