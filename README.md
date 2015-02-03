# dripper

Cleaning your messy data.

## Getting started

```python
some_messy_data = {
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
```

You need defile 'declaration' dictionary to drip essential data.

```python
declaration = {
    "articles": {
        "__type__": "list",
        "__source_root__": ['body', 'articles'],

        "title": ["title"],
        "published": ["published", "date", 0],
    },
    "meta": {
        "__source_root__": ["meta", "meta1", "meta3", 0],
        "author": ["author"],
    },
    "asset_type": ["meta", "meta4", "assetType"],
}
```

And just use.

```python
from dripper import dripper_factory
d = dripper_factory(declaration)
d(some_messy_data) == {
    "articles": [
        {'title': "Title",
         'published': "2014-11-05"},
    ],
    "meta": {
        "author": "Author name",
    },
    "asset_type": 1,
}
```
