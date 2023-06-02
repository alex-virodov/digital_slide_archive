Running Digital Slide Archive + OpenSlide with iSyntax support
==============================================================
1. Login to docker github: ``docker login ghcr.io -u <YOUR-USERNAME>``. See `Github docs <https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-to-the-container-registry>`_ for reference.
2.  Run DSA as usual, ``cd devops/dsa && DSA_USER=$(id -u):$(id -g) docker-compose up``. It will pull the prebuilt image.

Building Digital Slide Archive + OpenSlide with iSyntax support
===============================================================
1. You must be in linux shell/wsl2 shell. Checking out with git on windows will introduce windows endlines (^M) and will break scripts & patches.
2. ``python -m venv venv && source ./venv/bin/activate && pip install packaging requests``
3. ``git submodule update --init`` - to get openslide with isyntax-support.
4. ``cd large_image_wheels/ && ./rebuild.sh`` - this will take a long while (1 hour on a good machine, more on a weaker one).
   For repeated builds, can use ``./build.sh``, but need to run ``./rebuild.sh`` at least once to get package version checking.
   (Note: most of the built wheels will be unused, but I was not brave enough to untangle those dependencies and remove unneeded stuff.)
5. Build the dsa container: ``docker build -t ghcr.io/innovationcore/dsa_common_isyntax .`` in root directory.
6. Run DSA as usual, ``cd devops/dsa && DSA_USER=$(id -u):$(id -g) docker-compose up``.
 


Digital Slide Archive
=====================

The Digital Slide Archive is a system for working with large microscopy images.

- Organize images from a variety of assetstores, such as local file systems and S3.

- Provide user access controls.

- Image annotation and review.

- Run algorithms on all or parts of images.

Website
-------

See `<https://digitalslidearchive.github.io/digital_slide_archive/>`_ for information about the system.

Demo Instance
-------------

`http://demo.kitware.com/histomicstk/histomicstk <http://demo.kitware.com/histomicstk/histomicstk#?image=5c74528be62914004b10fd1e>`_.

Installation
------------

For installation instructions, see the complete `docker-compose example <./devops/dsa>`_.

There is an older method that doesn't use docker-compose.  See `here <./ansible>`_.

For local development including HistomicsUI, there are some `devops <./devops>`_ scripts.

There is a `migration guide <./ansible/migration.rst>`_  from the Girder 2 version and from the ``deploy_docker.py`` script.

Adding Docker Tasks
-------------------

Docker tasks conforming to the `slicer_cli_web <https://github.com/girder/slicer_cli_web>`_ module's requirements can be added.  These tasks appear in the HistomicsUI interface and in the Girder interface.  An administrator can add a Docker image by going to the slicer_cli_web plugin settings and entering the Docker image name there.  For instance, to get the HistomicsTK tasks, add ``dsarchive/histomicstk:latest``.

Funding
-------
This work was funded in part by the `NIH grant U24-CA194362-01 <http://grantome.com/grant/NIH/U24-CA194362-01>`_.
