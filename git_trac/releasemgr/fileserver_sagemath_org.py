
# -*- coding: utf-8 -*-
"""
Fab file for interaction with the sagemath.org server
"""

from __future__ import (absolute_import, division, print_function, unicode_literals)

import os

try:
    import fabric
    from fabric.api import env, run, sudo, put, settings, cd
    from fabric.contrib.files import exists
except ImportError:
    # Fabric shoud be py3-compatible any time now, but not yet
    pass


env_sagemath = dict(
    use_ssh_config=True,
    user='files',
    host_string='fileserver',
)


def package_name(url_or_path):
    tarball_name = os.path.basename(url_or_path)
    return tarball_name.split('-', 1)[0]


def upload_tarball(url_or_path):
    """
    Add tarball to http://sagemath.org/packages/upstream
    """
    with settings(**env_sagemath):
        package = package_name(url_or_path)
        destination = os.path.join('/home/files/files/spkg/upstream', package)
        run('mkdir -p {0}'.format(destination))
        run('touch {0}'.format(os.path.join(destination, 'index.html')))
        if os.path.exists(url_or_path):        # is local file
            put(url_or_path, os.path.join(destination, os.path.basename(url_or_path)))
        else:                                  # should be a url
            with cd(destination):
                run('wget --no-directories -p -N ' + url_or_path)
        run('/home/files/publish-files.sh')


def upload_dist_tarball(tarball, devel=True):
    """
    Add sdist tarball to http://sagemath.org/packages/

    INPUT:

    - ``devel`` -- boolean. Whether this is a beta/rc release.
    """
    if devel:
        destination = '/home/files/files/devel'
    else:
        destination = '/home/files/files/src'
    with settings(**env_sagemath):
        basename = os.path.basename(tarball)
        put(tarball, os.path.join(destination, basename))
        run('/home/files/publish-files.sh')


def upload_temp_confball(confball):
    """
    Add temporary tarball to ​http://old.files.sagemath.org/configure/

    These are for testing only and not send out to the mirror network
    """
    destination = '/home/files/files-old/configure'
    with settings(**env_sagemath):
        basename = os.path.basename(confball)
        put(confball, os.path.join(destination, basename))




# def upload_tarball(url):
#     """
#     Add tarball to http://sagemath.org/packages/upstream
#     """
#     if os.path.exists(url):        # is local file
#         put(url, os.path.join('/www-data/tmp/upstream', os.path.basename(url)))
#     else:                          # should be a url
#         with cd('/www-data/tmp/upstream'):
#             run('wget --no-directories -p -N ' + url)
#     with cd('/www-data/sagemath-org/scripts'):
#         run('./mirror_upstream.py /www-data/tmp/upstream')
#         run('./mirror-index.py')
#         run('./fix_permissions.sh')
#     run('/www-data/sagemath-org/go_live.sh')
