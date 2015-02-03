from unittest import TestCase


class TestConverter(TestCase):
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
