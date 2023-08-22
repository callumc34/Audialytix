def pool_to_dict(pool: "essentia.Pool") -> dict:
    """
    Convert a pool to a dictionary.

    :param      pool:  The pool
    :type       pool:  Pool

    :returns:   The dictionary of the pool
    :rtype:     dict
    """

    result = {}

    for descriptor in pool.descriptorNames():
        # TODO(Callum): Figure out why they are 2d arrays instead of 1d
        result[descriptor] = pool[descriptor].tolist()[0]

    return result
