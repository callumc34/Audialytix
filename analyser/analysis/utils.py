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
        result[descriptor] = pool[descriptor].tolist()

    return result
