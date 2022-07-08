Creating recipes
----------------

To retrieve a list of random ingredients,
you can use the ``lumache.get_random_ingredients()`` function:

.. py:function:: lumache.get_random_ingredients(kind=None)

   Return a list of random ingredients as strings.

   :param kind: Optional "kind" of ingredients.
   :type kind: list[str] or None
   :raise lumache.InvalidKindError: If the kind is invalid.
   :return: The ingredients list.
   :rtype: list[str]

The ``kind`` parameter should be either ``"meat"``, ``"fish"``,
or ``"veggies"``. Otherwise, :py:func:`lumache.get_random_ingredients`

#:py:func:`fpdf_table.main.PDFTable.barcode` will raise an exception.
#
.. py:exception:: lumache.InvalidKindError

   Raised if the kind is invalid.


Welcome to Lumache's documentation!
===================================

**Lumache** (/lu'make/) is a Python library for cooks and food lovers that
creates recipes mixing random ingredients.  It pulls data from the `Open Food
Facts database <https://world.openfoodfacts.org/>`_ and offers a *simple* and
*intuitive* API.

Check out the :doc:`usage` section for further information, including how to
:ref:`install <installation>` the project.


.. hint:: This is a note admonition.
   This is the second line of the first paragraph.

.. important:: This is a note admonition.
   This is the second line of the first paragraph.

.. tip:: This is a note admonition.
   This is the second line of the first paragraph.

.. autofunction:: ../../pruebas.py.minimal_example

