import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.main import app as application  # <== Esto es vital que esté bien
