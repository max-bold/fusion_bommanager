import adsk.core
import os

from ...lib import fusion360utils as futil
from ... import config
app = adsk.core.Application.get()
ui = app.userInterface

CMD_ID = 'bomextract'
CMD_NAME = 'BOM extract'
CMD_Description = 'BOM Manager extract to DB'

IS_PROMOTED = True

WORKSPACE_ID = 'FusionSolidEnvironment'
PANEL_ID = 'SolidScriptsAddinsPanel'
COMMAND_BESIDE_ID = 'ScriptsManagerCommand'

ICON_FOLDER = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'resources',' ')

local_handlers = []

def start():
    cmddef: adsk.core.CommandDefinition = ui.commandDefinitions.addButtonDefinition(CMD_ID, CMD_NAME, CMD_Description)
    futil.add_handler(cmddef.commandCreated, commandcreated)
    ws = ui.workspaces.itemById(WORKSPACE_ID)
    panel = ws.toolbarPanels.itemById(PANEL_ID)
    cont: adsk.core.CommandControl = panel.controls.addCommand(cmddef)
    cont.isPromoted = IS_PROMOTED

def stop():
    ws = ui.workspaces.itemById(WORKSPACE_ID)
    panel = ws.toolbarPanels.itemById(PANEL_ID)
    cont = panel.controls.itemById(CMD_ID)
    comdef = ui.commandDefinitions.itemById(CMD_ID)
    if cont:
        cont.deleteMe()
    if comdef:
        comdef.deleteMe()

def commandcreated(args: adsk.core.CommandCreatedEventArgs):
    pass

def commandexec(args: adsk.core.CommandEventArgs):
    pass