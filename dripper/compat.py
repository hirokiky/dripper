import sys
PY3 = sys.version_info[0] == 3


if PY3:
    from functools import reduce  # NOQA
else:
    reduce = reduce
