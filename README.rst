=========
Pautomate
=========


.. image:: https://img.shields.io/travis/ammarnajjar/pautomate.svg
        :target: https://travis-ci.org/ammarnajjar/pautomate


.. image:: https://pyup.io/repos/github/ammarnajjar/pautomate/shield.svg
     :target: https://pyup.io/repos/github/ammarnajjar/pautomate/
     :alt: Updates


.. image:: https://readthedocs.org/projects/pautomate/badge/?version=latest
     :target: https://pautomate.readthedocs.io/en/latest/?badge=latest
     :alt: Documentation Status


.. image:: https://api.codacy.com/project/badge/Grade/04f9376738754681bb41b2170b9627cd
     :target: https://www.codacy.com/app/ammarnajjar/pautomate?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ammarnajjar/pautomate&amp;utm_campaign=Badge_Grade
     :alt: Quality


.. image:: https://api.codeclimate.com/v1/badges/66a1a426774d955d67bc/maintainability
     :target: https://codeclimate.com/github/ammarnajjar/pautomate/maintainability
     :alt: Maintainability



Automate my boring stuff.


* Free software: MIT license
* Documentation: https://pautomate.readthedocs.io.


Features
--------

* Uses click_ under the hood.
* Fetch repos from Gitlab using a personal token.
* Clone the repos if they don't exist.
* Get branches info of repos in a specific directory.
* Reset --hard branches with a flag (-r)
* Run multiple dotnet core commands on different projects in parallel.
* The dotnet command type can be passed as an argument.

Credits
-------

This package was created originally with Cookiecutter_ and
the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _click: https://github.com/pallets/click
