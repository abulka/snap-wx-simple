import wx
# from pydbg import dbg
import time

from wxasync import AsyncBind, WxAsyncApp, StartCoroutine
import asyncio
from asyncio.events import get_event_loop

ASYNC_VERSION = True

from gui.settings import FOUND_RELMGR

if FOUND_RELMGR:
    from relmgr.relationship_manager import RelationshipManager
else:
    import wx.lib.ogl as RelationshipManager

print('done', RelationshipManager)

