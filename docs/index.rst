.. FPDF Table documentation master file, created by
   sphinx-quickstart on Mon Jun 27 12:07:46 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to fpdf-table documentation!
======================================
**fpdf-table** is a *fast, framework-agnostic library* for generating PDF reports in a similar way as HTML tables are created,
everything you draw is inside a table ( container with a border ), it also allows you to create reports in a more *elegant* and *DRY* way.

What is fpdf-table
------------------
**fpdf-table** is built on top of `fpdf2 <https://pyfpdf.github.io/fpdf2/index.html>`_, is somewhat inspired by HTML tables and jspdf-autotable,
provides abstraction to manipulate everything in the form of tables, provides unique features and several utilities.

.. note::

   This library does not parse HTML tables to PDF, you can do it through fpdf2 but only in a very limited way.

Main features
--------------
* Make tables fast
* Make tables with fixed height rows
* Everything that `fpdf2 <https://pyfpdf.github.io/fpdf2/index.html>`_ does.



.. toctree::
   :maxdepth: 2
   :caption: Contents:

   source/usage
   source/api/pdf_table
   source/test




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
