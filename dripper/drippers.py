from copy import deepcopy


def dig_in(source, items):
    digging = deepcopy(source)
    for item in items:
        digging = digging[item]
    return digging


class ValueDripper(object):
    def __init__(self, source_root):
        self.source_root = source_root

    def __call__(self, converting):
        return dig_in(converting, self.source_root)


class DictDripper(object):
    def __init__(self, source_root, drippers):
        self.source_root = source_root
        self.drippers = drippers

    def __call__(self, converting):
        dug_in = dig_in(converting, self.source_root)
        return {key: d(dug_in) for key, d in self.drippers.items()}


class ListDripper(object):
    def __init__(self, source_root, drippers):
        self.source_root = source_root
        self.drippers = drippers

    def __call__(self, converting):
        dict_dripper = DictDripper([], self.drippers)
        return [dict_dripper(dug_in) for dug_in in dig_in(converting, self.source_root)]


def dripper_factory(declaration):
    if isinstance(declaration, list):
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
