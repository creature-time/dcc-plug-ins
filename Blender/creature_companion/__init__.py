import bpy
import os
import sys

def register():
    sys.path.append(os.path.dirname(__file__))
    import creaturetime
    creaturetime.register()

def unregister():
    import creaturetime
    creaturetime.unregister()
    sys.path.append(os.path.dirname(__file__))
