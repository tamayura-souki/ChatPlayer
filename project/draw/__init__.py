try:
    from ..config import logger
except:
    import os, sys
    sys.path.append(os.pardir)
    from config import logger

from .draw import Render
from .pygame_draw import get_quit_event, PygameStrRender, GroupRender, PygameWindow