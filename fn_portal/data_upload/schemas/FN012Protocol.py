from .FN012Base import FN012BaseFactory


def FN012ProtocolFactory(agest_choices):
    """A factory fucntion that will return a pydandic validator class
    that includes current valid agest choices.

    Arguments:
    - `agest_choices`:

    """

    FN012Base = FN012BaseFactory(agest_choices)

    class FN012Protocol(FN012Base):
        """A validator for FN012 objects within a protocol. Exactly the same
        as the FN012 validator, with the addition of a protocol_id and
        lake_id attributes (required integers)
        """

        lake_id: int
        protocol_id: int

    return FN012Protocol
