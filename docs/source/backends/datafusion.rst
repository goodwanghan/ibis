.. _install.datafusion:

`Datafusion <https://arrow.apache.org/datafusion/>`_
====================================================

.. note::

   The Datafusion backend is experimental

Install
-------

Install ibis along with its dependencies for the datafusion backend:

::

  pip install 'ibis-framework[datafusion]'

or

::

  conda install -c conda-forge ibis-datafusion

Connect
-------

Create a client by passing a dictionary that maps table names to paths to
:func:`ibis.datafusion.connect`:

.. code-block:: python

   >>> import ibis
   >>> data_sources = {"t": "path/to/file.parquet", "s": "path/to/file.csv"}
   >>> client = ibis.datafusion.connect(data_sources)
   >>> t = client.table("t")

.. _api.datafusion:

API
---
.. currentmodule:: ibis.backends.datafusion

The Datafusion client is accessible through the ``ibis.datafusion`` namespace.

Use ``ibis.datafusion.connect`` to create a Datafusion client.

.. autosummary::
   :toctree: ../generated/

   Backend.connect
   Backend.database
   Backend.list_tables
   Backend.table
   Backend.register_csv
   Backend.register_parquet
