=======
dripper
=======

Cleaning your messy data.

.. contents::
    :depth: 1

Getting started
===============

Consider cleaning up some messy data.
Here is a deep nested dictionary containing lots of unnecessary nesting and tuple.

.. code-block:: python

    some_messy_data = {
        "body": {
            "article": {
                 "articlesbody": {
                     "articlesmeta": {
                         "articles_meta_3": "Monty Python",
                     }
                 }
            },
        },
        "published": {
            "datetime": ("2014-11-05", "23:00:00"),
        }
    }

Values you want are ``'Monty Python'`` and ``'2014-11-05'``,
should be named ``'title'`` and ``'published_date'``

Now let the hack begin with the ``dripper``.

* Defile ``declaration`` dictionary
* Create dripper object by ``dripper.dripper_factory``
* Drip essential data

.. code-block:: python

    # Define
     declaration = {
        "title": ("body", "article", "articlesbody", "articlesmeta", "articles_meta_3"),
        "published_date": ("published", "datetime", 0)
    }
    
    # Create
    import dripper
    d = dripper.dripper_factory(declaration)
    
    # And drip
    dripped = d(some_messy_data)
    
    assert dripped == {
        "title": "Monty Python",
        "published_date": "2014-11-05",
    }

Installation
============

Just use pip to install

.. code-block:: console

    pip install dripper

Requirements
------------

``dripper`` won't require any kind of outer libraries.
Supporting Python versions are:

* Python 2.7
* Python 3.3
* Python 3.4
* Python 3.5

Basics
======

Above example is not all features of ``dripper``.
It is created to handle various data to clean up.

As value
--------

.. code-block:: python

    from dripper import dripper_factory
    declaration = {
        "title": ("meta", "meta1")
    })
    d = dripper_factory(declaration)
    d({"meta": {"meta1": "Monty Python"}}) == {"title": "Monty Python"}

Also you can specify string or integer directly.
It is as same as one-element tuple.

.. code-block:: python

    from dripper import dripper_factory
    declaration = {
        "title": "meta"
    })
    d = dripper_factory(declaration)
    d({"meta": "Monty Python"}) == {"title": "Monty Python"}

As dict
-------

``dripper`` can define nested dictionary.
Just pass nested dictionary to ``dripper_factory``.

.. code-block:: python

    from dripper import dripper_factory
    declaration = {
        "article": {
            "title": ["meta", "meta1"],
        }
    })
    d = dripper_factory(declaration)
    d({
        "meta": {
            "meta1": "Monty Python",
        },
    }) == {
        "article": {
            "title": "Monty Python",
        }
    }

You can apply ``'__source_root__'`` to set root path for dripping.

.. code-block:: python

    declaration = {
        "article": {
            "__source_root__": ("body", "meta"),
    ...
            "title": "meta1",
            "author": ("meta2", "meta22"),
        }
    })
    d = dripper_factory(declaration)
    d({
        "body": {
            "meta": {
                "meta1": "Monty Python",
                "meta2": {"meta22": "John Due"}
            }
        }
    }) == {
        "article": {
            "title": "Monty Python",
            "author": "John Due",
        }
    }

Technically, outermost dictionary of ``declaration`` is as same as inner dictionaries.
So you can specify ``'__source_root__'`` the dictionary.

As list
-------

``dripper`` can define list of dictionaries.
You need to apply ``'__type__': 'list'``.

.. code-block:: python

    from dripper import dripper_factory
    declaration = {
        "articles": {
            "__type__": "list",
            "__source_root__": "articles",
    ...
            "title": "meta1",
            "author": ["meta2", "meta22"],
        }
    })
    d = dripper_factory(declaration)
    d({
        "articles": [
            {"meta1": "Monty Python", "meta2": {"meta22": "John Doe"}},
            {"meta1": "Flying Circus", "meta2": {"meta22": "Jane Doe"}},
        ]
    }) == {
        "articles": [
            {"title": "Monty Python", "author": "John Doe"},
            {"title": "Flying Circus", "author": "Jane Doe"},
        ]
    }

Advanced
========

Converting
----------

Use ``dripper.ValueDripper`` to pass converter function.

.. code-block:: python

    import dripper
    declaration = {
        "title": dripper.ValueDripper(["title"], converter=lambda s: s.lower())
    }
    d = dripper.dripper_factory(declaration)
    d({"title": "TITLE"}) == {"title": "title"}


Technically, each ends (list) will be replaced by instance of ``dripper.ValueDripper``.

default value
-------------

Specify ``default`` keyword argument to change default value.
``None`` will be applied as default.

.. code-block:: python

    import dripper
    declaration = {
        "title": dripper.ValueDripper(["title"], default="default")
    }
    d = dripper.dripper_factory(declaration)
    d({}) == {"title": "default"}


Technically, each ends (list) will be replaced by instance of ``dripper.ValueDripper``.

Combining
---------

By combining ``dripper.ValueDripper``, result value of that key will be combined.

.. code-block:: python

    import dripper
    declaration = {
        "fullname": (dripper.ValueDripper(["firstname"]) +
                     dripper.ValueDripper(["lastname"]))
    }
    d = dripper.dripper_factory(declaration)
    d({"firstname": "Hrioki", "lastname": "Kiyohara"}) == {"fullname": "HriokiKiyohara"}
