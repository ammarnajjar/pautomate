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
* All logs are stored in a JSON format.

Credits
-------

- This package was created originally with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

- `logjson` was created originally by Michael Blan Palmer.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _click: https://github.com/pallets/click
