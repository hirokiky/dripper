from unittest import TestCase


class TestDigIn(TestCase):
    def _callFUT(self, *args, **kwargs):
        from dripper.drippers import dig_in
        return dig_in(*args, **kwargs)

    def test__list(self):
        actual = self._callFUT(['result'], [0])
        self.assertEqual(actual, 'result')

    def test__dict(self):
        actual = self._callFUT({'title': 'learning python'}, ['title'])
        self.assertEqual(actual, 'learning python')

    def test__deep_source(self):
        actual = self._callFUT(
            {'body': {'meta': {'meta4': ('meta22', {'meta33': 'learning python'})}}},
            ['body', 'meta', 'meta4', 1, 'meta33']
        )
        self.assertEqual(actual, 'learning python')

    def test__key_error(self):
        with self.assertRaises(KeyError):
            self._callFUT({}, ['bomb'])

    def test__type_error(self):
        with self.assertRaises(TypeError):
            self._callFUT([], ['bomb'])

    def test__index_error(self):
        with self.assertRaises(IndexError):
            self._callFUT([], [10000])


class TestValueDripper(TestCase):
    def _makeOne(self, *args, **kwargs):
        from dripper.drippers import ValueDripper
        return ValueDripper(*args, **kwargs)

    def test__call(self):
        target = self._makeOne(['title'])
        actual = target({'title': 'learning python'})
        self.assertEqual(actual, 'learning python')


class TestDictDripper(TestCase):
    def _makeOne(self, *args, **kwargs):
        from dripper.drippers import DictDripper
        return DictDripper(*args, **kwargs)

    def test__call(self):
        def title_dripper(converting):
            return converting['title']

        target = self._makeOne(['meta'], {'title': title_dripper})
        actual = target({'meta': {'title': 'learning python'}})
        self.assertEqual(actual, {'title': 'learning python'})


class TestListDripper(TestCase):
    def _makeOne(self, *args, **kwargs):
        from dripper.drippers import ListDripper
        return ListDripper(*args, **kwargs)

    def test__call(self):
        def title_dripper(converting):
            return converting['title']

        target = self._makeOne(['meta'], {'title': title_dripper})
        actual = target({'meta': [{'title': 'learning python'}, {'title': 'python cookbook'}]})
        self.assertEqual(actual, [{'title': 'learning python'}, {'title': 'python cookbook'}])


class TestDripperFactory(TestCase):
    def _callFUT(self, *args, **kwargs):
        from dripper.drippers import dripper_factory
        return dripper_factory(*args, **kwargs)

    def test__list(self):
        from dripper.drippers import ValueDripper
        actual = self._callFUT(['foo', 'bor'])
        self.assertIsInstance(actual, ValueDripper)
        self.assertEqual(actual.source_root, ['foo', 'bor'])

    def test__callable(self):
        def dummy_dripper(converting):
            pass
        actual = self._callFUT(dummy_dripper)
        self.assertIs(actual, dummy_dripper)

    def test__dict(self):
        from dripper.drippers import DictDripper, ValueDripper
        actual = self._callFUT({'foo': ['hoge', 'fuga']})
        self.assertIsInstance(actual, DictDripper)
        self.assertEqual(actual.source_root, [])
        self.assertIsInstance(actual.drippers['foo'], ValueDripper)
        self.assertEqual(actual.drippers['foo'].source_root, ['hoge', 'fuga'])

    def test__dict__dict_type(self):
        from dripper.drippers import DictDripper, ValueDripper
        actual = self._callFUT({
            '__type__': 'dict',
            '__source_root__': ['hoge'],
            'foo': ['fuga', 'piyo']
        })
        self.assertIsInstance(actual, DictDripper)
        self.assertEqual(actual.source_root, ['hoge'])
        self.assertIsInstance(actual.drippers['foo'], ValueDripper)
        self.assertEqual(actual.drippers['foo'].source_root, ['fuga', 'piyo'])

    def test__dict__list_type(self):
        from dripper.drippers import ListDripper, DictDripper, ValueDripper
        actual = self._callFUT({
            '__type__': 'list',
            '__source_root__': ['hoge'],
            'foo': ['fuga', 'piyo']
        })
        self.assertIsInstance(actual, ListDripper)
        self.assertEqual(actual.source_root, ['hoge'])
        self.assertIsInstance(actual.drippers['foo'], ValueDripper)
        self.assertEqual(actual.drippers['foo'].source_root, ['fuga', 'piyo'])


class TestDripper(TestCase):
    def _callFUT(self, decralation, source):
        from dripper.drippers import dripper_factory
        return dripper_factory(decralation)(source)

    def test__it(self):
        source = {
            "body": {
                "articles": [
                    {"title": "Title",
                     "published": {"date": ["2014-11-05"]}},
                ],
            },
            "meta": {
                "meta1": {
                    "meta3": [{"author": "Author name"}]
                },
                "meta4": {"assetType": 1}
            }
        }
        declaration = {
            "articles": {
                "__type__": "list",
                "__source_root__": ['body', 'articles'],

                "title": ["title"],
                "title_lower": lambda d: d['title'].lower(),
                "published": ["published", "date", 0],
            },
            "meta": {
                "__source_root__": ["meta", "meta1", "meta3", 0],
                "author": ["author"],
            },
            "asset_type": ["meta", "meta4", "assetType"],
        }
        actual = self._callFUT(declaration, source)
        self.assertEqual(
            actual,
            {
                "articles": [
                    {'title': "Title",
                     'title_lower': 'title',
                     'published': "2014-11-05"},
                ],
                "meta": {
                    "author": "Author name",
                },
                "asset_type": 1,
            }
        )
