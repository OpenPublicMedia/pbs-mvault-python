#!/bin/env python

from fabric.api import local
from fabric.context_managers import shell_env

def tests():
    """
    Run tests

    """
    with shell_env():
        local('python -m unittest discover')