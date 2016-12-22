
Changelog
=========

0.2.1 (2016-12-22)
-----------------------------------------
* fixed minor bugs
* README.md updated
* beautify the source codes

0.1.6x (2015-10-20)
-----------------------------------------
* Fixed minor bugs

0.1.6 (2015-10-20)
-----------------------------------------
* `use_dict` option to render dictionary. By default is `False`.
* `include_entity` option on searches. By default is `False`
* Introduccing `._pw_index_` attribute per each Entity
* Whoosh renamed by PonyWhoosh, with all config variables as well.
* `pk` on results for search is a list nowadays
* Support for Composite Primary Keys on Entity
* Improvements of Front-End Example Search Page and Results Page
* New contribuitor, alegomezc64 to make the design/js of front pages.

0.1.5 (2015-10-20)
-----------------------------------------
* wh.init_opts(**) depracted
* <your_url>/ponywhoosh
* config constant: WHOOSHEE_URL to add a view of search engine
* config constant:  PONYWHOOSH_DEBUG for debugging purposes
* fix bugs about search arguments and other stuffs.
* full_search now accepts models as strings as wells.
* Please look up into the documentation for more details about this version.



0.1.4 (2015-09-11)
-----------------------------------------
* Add new testing base: test.py
* Add support to search in fields with int, float and datetime type.
* Add include entity in results of search.
* Add pruning for options in search without support.
* Fixed some bugs in app.py (flask example app).
* Optimze the indexes as an method .optimize(), no by default.


0.1.3 (2015-08-29)
-----------------------------------------
* There were several changes, so please refer to documentation to see a complete description. Most of them, they were about new methods for whoosheers and, general methods like full_search, and the way you can perform a search within a entity.


0.1.2 (2015-08-15)
-----------------------------------------
* Add Documentation

0.1.1 (2015-08-15)
-----------------------------------------

* Add a new logo!!!
* Add examples in the documention
* The documentation is now available with Spinix

0.1.0 (2015-08-14)
-----------------------------------------

* First release on PyPI.