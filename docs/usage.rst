=====
Usage
=====

To use Pautomate in a project
-----------------------------

import as::

 import pautomate

To use Pautomate as a CLI Application
-------------------------------------

Show help:
^^^^^^^^^^

Just run::

 pautomate --help

 usage: pautomate [-h] {fetch,releases,branches} ...

 Automate my boring stuff

 positional arguments:
   {fetch,releases,branches}
     fetch               Clone/fetch projects from Gitlab using the private token
     releases            Get lastest stable releases in the local workspace
     branches            Get branches infos in the local workspace

 options:
   -h, --help            show this help message and exit

""""

Commands:
^^^^^^^^^

- **branches**:

Get branches informations in the current directory::

 pautomate -t . branches

The target is by default the current directory.

Get the branches informations after resetting hard to head::

 pautomate beanches -r

Get the branches informations, checkout develop branch then hard reset it to origin/develop::

 pautomate beanches -rd

Careful that these are **distructive** commands, for they use `git reset --hard` on all the repos treated.

To select only repositories that contatin a specific pattern in them and get thier informations (e.g: `py`)::

 pautomate branches py  # only repositories with "py" in them will be considerd

The last set of agruments acts like a filter. More than one argument can also be given, and all will be considerd as filters::

 pautomate branches py api service  # only repositories with "py" in them will be considerd

More info can be found using the help command::

 pautomate beanches --help

- **fetch**:

Clone all repositories on a gitlab isntance using the personal access token. If the repositories is already cloned, it will be fetched again, and the current local branch will be soft reset to the origin branch.

`develop` branch if exists will also be reset to match `origin/develop`, this guarantees that `develop` stays alway in sync with `origin`.

This command requires some external configurations, and those configurations should be sotred in a `config.json` file in the target directory.

The structure of `config.json` should be like::

 {
    "gitlab_url": "e.g.: gitlab.com",
    "gitlab_token": "e.g: kjhasd8123hasdz123",
	"gitlab_group_id" : "e.g: 41",
    "ignore_list": ["test", "example"],
 }

Meanwhile the option `ìgnore_list` is optional, the other two are mandatory to be able to fetch/Clone the repositories from the desired gitlab instance.

More about gitlab personal access tokens can be found in the official documentation_.

`ignore_list` is a list of string patterns to exlclude from fetching/cloning.


To fetch repositories::

 pautomate fetch

To pass a white list pattern::

 pautomate fetch py demo    # fetch/clone only what has "py" or "demo" in its name

The list of fetched repositories will be stored on disk in a file called `repos`.
This file will be used if exists to gather informations about the repositories
instead of calling the gitlab API, which saves some time.

More info can be found using the help command::

 pautomate fetch --help

- **releases**:

Checks for the repositories fetched before, and shows the latest stable release.

To fetch repositories::

 pautomate releases

To pass a white list pattern::

 pautomate releases api client    # releases for only what has "api" or "client" in its path

More info can be found using the help command::

 pautomate releases --help

Entry Points
------------

There is an extra entry point supported for each command, to make it faster to get the job done. So each command can also be executed in a short form::

 pautomate fetch    -> fetch
 pautomate branches -> branches
 pautomate releases -> releases


Docker
------

To run using docker:

- build image::

   docker build --rm -f "Dockerfile" -t pautomate .

- run the desired entry point::

   docker run --rm -v $(pwd):/ws:rw -it pautomate --help
   docker run --rm -v $(pwd):/ws:rw -it pautomate fetch --help
   docker run --rm -v $(pwd):/ws:rw -it pautomate branches --help
   docker run --rm -v $(pwd):/ws:rw -it pautomate releases --help


.. _documentation: target https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html
