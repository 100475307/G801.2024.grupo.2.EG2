"""
archivo build
"""
#   -*- coding: utf-8 -*-
from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")


NAME = "Proyecto prueba"
DEFAULT_TASK = "publish"


@init
def setProperties():
    """
    esta funcion hace un pass
    """
