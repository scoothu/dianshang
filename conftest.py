import sys
import os

project_root = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(project_root, 'lib')

if project_root not in sys.path:
    sys.path.insert(0, project_root)
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)
