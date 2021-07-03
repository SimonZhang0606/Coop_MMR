def serialize(x, as_type=None, nullable=False):
    if nullable:
        return None if x is None else as_type(x)
    else:
        assert(x is not None)
        return as_type(x)
