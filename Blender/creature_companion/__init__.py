import bpy
import os
import sys

from . import resources
from . import registration

from . import properties
from . import operators
from . import menus
from . import panels
from . import handlers
from . import validations


def register():
    resources.load_resources()

    validations.register()
    registration.register()

    properties.register()
    operators.register()
    menus.register()
    panels.register()
    handlers.register()


def unregister():
    handlers.unregister()
    panels.unregister()
    menus.unregister()
    operators.unregister()
    properties.unregister()

    registration.unregister()
    validations.unregister()

    resources.unload_resources()