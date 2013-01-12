# -*- coding: utf-8 -*-

from fabric.api import require, run, local, env, put, cd
from fabric.contrib.files import exists

env.use_ssh_config = True

env.hosts = ['linfiniti2']
env.sitename = 'osm-reporter'
env.path = '/home/web/%s' % (env.sitename,)
env.repo = 'git://github.com:timlinux/osm-reporter.git'

def _install_dependencies():
    """Use pip to install required packages."""
    # PyPI mirror list is at http://pypi.python.org/mirrors
    require('hosts')
    run('/%(path)s/python/bin/pip install --timeout=60 '
        '--log %(path)s/log/pip.log '
        '--download-cache PIP-DOWNLOAD-CACHE -M '
        '--mirrors b.pypi.python.org '
        '--mirrors c.pypi.python.org '
        '--mirrors d.pypi.python.org '
        '--mirrors e.pypi.python.org '
        '--mirrors f.pypi.python.org '
        '-r %(path)s/REQUIREMENTS.txt 2>%(path)s/log/pip.errs' % env)


def _pull():
    """Pull the lastest version."""
    require('hosts')
    with cd('%(path)s' % env):
        run('git pull origin master')

def _deploy():
    """Deploy the website."""
    with cd('%(path)s' % env):
        if not exists(env.path + '/log'):
            run('mkdir -p %s/log' % env.path)
    _pull()
    _install_dependencies()
    with cd('%(path)s' % env):
        run('touch apache/osm-reporter.wsgi')


# ------------------------- TOP-LEVEL COMMANDS -------------------------


def bootstrap():
    """Bootstrap the project"""
    require('hosts')
    run('git clone %s %s' % (env.repo, env.path))
    run('mkdir -p %s/log' % env.path)
    if not exists(env.path + '/python'):
        run('virtualenv %s/python' % env.path)
    _install_dependencies()


def push():
    _pull()


def deploy():
    """
    Wraps all the steps up to deploy to the live server.
    """
    _deploy()
