from copy import deepcopy
import operator

from dripper.compat import reduce
from dripper.exceptions import DrippingError


def dig_in(source, items):
    digging = deepcopy(source)
    for item in items:
        try:
            digging = digging[item]
        except (TypeError, KeyError, IndexError):
            raise DrippingError
    return digging


class ValueDripper(object):
    def __init__(self, source_root, converter=None):
        if isinstance(source_root, (str, int)):
            self.source_root = (source_root,)
        else:
            self.source_root = source_root
        assert converter is None or callable(converter), "converter argument should be callable."
        self.converter = converter

    def __call__(self, converting):
        dug_in = dig_in(converting, self.source_root)
        if self.converter:
            return self.converter(dug_in)
        return dug_in

    def __add__(self, other):
        return MixDripper((self, other))


class DictDripper(object):
    def __init__(self, source_root, drippers):
        if isinstance(source_root, (str, int)):
            self.source_root = (source_root,)
        else:
            self.source_root = source_root
        self.drippers = drippers

    def __call__(self, converting):
        try:
            dug_in = dig_in(converting, self.source_root)
            return {key: d(dug_in) for key, d in self.drippers.items()}
        except DrippingError:
            return {}


class ListDripper(object):
    def __init__(self, source_root, drippers):
        if isinstance(source_root, (str, int)):
            self.source_root = (source_root,)
        else:
            self.source_root = source_root
        self.drippers = drippers

    def __call__(self, converting):
        try:
            dug_in = dig_in(converting, self.source_root)
        except DrippingError:
            return []

        dict_dripper = DictDripper([], self.drippers)
        return [dict_dripper(d) for d in dug_in]


class MixDripper(object):
    def __init__(self, drippers, mixer=operator.add):
        self.drippers = drippers
        self.mixer = mixer

    def __call__(self, converting):
        return reduce(self.mixer, (d(converting) for d in self.drippers))


def dripper_factory(declaration):
    if isinstance(declaration, (list, tuple, int, str)):
        return ValueDripper(declaration)

    elif callable(declaration):
        return declaration

    elif isinstance(declaration, dict):
        drippers_dec = {k: v for k, v in declaration.items()
                        if not k.startswith('__') and not k.endswith('__')}
        drippers = {key: dripper_factory(dec) for key, dec in drippers_dec.items()}
        source_root = declaration.get('__source_root__', [])
        conv_type = declaration.get('__type__', 'dict')

        if conv_type == 'dict':
            return DictDripper(source_root, drippers)
        elif conv_type == 'list':
            return ListDripper(source_root, drippers)
        else:  # pragma: nocover
            raise AssertionError("Invalid __type__ {} specified".format(conv_type))
