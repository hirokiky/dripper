=======
dripper
=======

Cleaning your messy data.

Getting started
===============

Consider you need to clean up some messy data.
Here is a deep nested dictionary containing unnecessary nesting, tuples and so.

.. code-block:: python

    some_messy_data = {
        "body": {
            "articles": [
                {"title": "Title",
                 "published": {"date": ("2014-11-05", "23:00:00")}},
            ],
        },
        "meta": {
            "meta1": {
                "meta3": ('19911105', {"author": "Author name"})
            },
            "meta4": {"assetType": 1}
        }
    }

Necessary values are ``'articles'``, ``'author'`` and ``'assetType'``.

Now let the hack begin with the dripper.
Defile 'declaration' dictionary to drip essential data.

.. code-block:: python

    declaration = {
        "articles": {
            "__type__": "list",  # 'articles' is list of dictionary
            "__source_root__": ['body', 'articles'],  # The root position of 'articles'
    
            "title": ["title"],  # each dictionary of 'articles' will contain 'title'
            "published": ["published", "date", 0],  # and 'published'. you can pass the path to the value
        },
        "meta": {
            "__source_root__": ["meta", "meta1", "meta3", 1],

            "author": ["author"],
            "author_lower": lambda d: d["author"].lower(),  # Pass a callable accepting one argument ('meta' dictionary)
        },
        "asset_type": ["meta", "meta4", "assetType"],
    }

And just use like this.

.. code-block:: python

    from dripper import dripper_factory
    d = dripper_factory(declaration)
    d(some_messy_data) == {
        "articles": [
            {'title': "Title",
             'published': "2014-11-05"},
        ],
        "meta": {
            "author": "Author name",
            "author_lower": "author name",
        },
        "asset_type": 1,
    }
