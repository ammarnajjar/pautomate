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

 Usage: pautomate [OPTIONS] COMMAND [ARGS]...

   Console interface for pautomate

 Options:
   -t, --target PATH  [.] Target workspace.
   --help             Show this message and exit.

 Commands:
   branches    Get branches infos in the local workspace Arguments: - args...
   dotnet      Run dotnet services in parallel via dotnet core CLI Arguments:...
   fetch       Clone/fetch projects from Gitlab using the private token...

""""

Commands:
^^^^^^^^^

- **branches**:

Get branches informations in the current directory::

 pautomate -t . branches

The target is by default the current directory.

Get the branches informations after resetting hard to head::

 pautomate beanches -r

Careful that this is a **distructive** command, for it uses `git reset --hard` on all the repos treated.

To select only repositories that contatin a specific pattern in them and get thier informations (e.g: `py`)::

 pautomate branches py  # only repositories with "py" in them will be considerd

The last set of agruments acts like a filter. More than one argument can also be given, and all will be considerd as filters::

 pautomate branches py api service  # only repositories with "py" in them will be considerd

More info can be found using the help command::

 pautomate dotnet --help

- **fetch**:

Clone all repositories on a gitlab isntance using the personal access token. If the repositories is already cloned, it will be fetched again, and the current local branch will be soft reset to the origin branch.

`develop` branch if exists will also be reset to match `origin/develop`, this guarantees that `develop` stays alway in sync with `origin`.

This command requires some external configurations, and those configurations should be sotred in a `config.json` file in the target directory.

The structure of `config.json` should be like::

 {
    "gitlab_url": "e.g.: gitlab.com",
    "gitlab_token": "e.g: kjhasd8123hasdz123",
    "ignore_list": ["test", "example"],
 }

Meanwhile the option `ìgnore_list` is optional, the other two are mandatory to be able to fetch/Clone the repositories from the desired gitlab instance.

More about gitlab personal access tokens can be found in the official documentation_.

`ignore_list` is a list of string patterns to exlclude from fetching/cloning.


To fetch repositories::

 pautomate fetch

To pass a white list pattern::

 pautomate fetch py demo    # fetch/clone only what has "py" or "demo" in its name

More info can be found using the help command::

 pautomate fetch --help

- **dotnet**:

Executes a specific dotnet core command on multiple dotnet core projects in parallel.

A default list can be configured in a `config.json` file in the target directory::

 {
     "dotnet_projects": ["dotnet_pro1", "dotnet_pro2"]
 }

So these projects will be looked up then the passed dotnet command will be executed in all of them in parallel.

A process pool will be initialized to conatain the running processes.

All the allowed dotnet commands are supported e.g.::

 pautomate dotnet run      # run projects in config.json in parallel
 pautomate dotnet run -w   # run projects in watch mode
 pautomate dotnet test -w  # run test projects in watch mode
 pautomate dotnet clean py demo  # dotnet clean only projects that has either "py" or "demo" in its name
 pautomate dotnet build demo  # dotnet build only projects that has "demo" in its name

More info can be found using the help command::

 pautomate dotnet --help

Entry Points
------------

There is an extra entry point supported for each command, to make it faster to get the job done. So each command can also be executed in a short form::

 pautomate fetch    -> fetch
 pautomate branches -> branches
 pautomate dotnet   -> dnet


Docker
------

To run using docker:

- build image::

 docker build --rm -f "Dockerfile" -t pautomate .

- run the desired entry point::

 docker run --rm -v $(pwd):/ws:rw -it pautomate --help
 docker run --rm -v $(pwd):/ws:rw -it pautomate dotnet --help
 docker run --rm -v $(pwd):/ws:rw -it pautomate fetch --help
 docker run --rm -v $(pwd):/ws:rw -it pautomate branches --help


.. _documentation: target https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html
