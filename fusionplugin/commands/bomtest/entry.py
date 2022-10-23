import adsk.core
import os
from ...lib import peewee

from ...lib import fusion360utils as futil
from ... import config
app = adsk.core.Application.get()
ui = app.userInterface

CMD_ID = 'bomtest1'
CMD_NAME = 'BOM tests'
CMD_Description = 'BOM Manager tests'

IS_PROMOTED = True

WORKSPACE_ID = 'FusionSolidEnvironment'
PANEL_ID = 'SolidScriptsAddinsPanel'
COMMAND_BESIDE_ID = 'ScriptsManagerCommand'

ICON_FOLDER = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'resources',' ')

local_handlers = []

db = peewee.MySQLDatabase('test2', user='root',
                          password='root', host='localhost', port=3306, autoconnect=True)



class basemodel(peewee.Model):
    class Meta:
        database = db

class userrec(basemodel):
    id = peewee.IntegerField(primary_key =True,unique=True)
    name = peewee.CharField(max_length=100)

db.connect()

def start():
    cmd_def = ui.commandDefinitions.addButtonDefinition(
        CMD_ID, CMD_NAME, CMD_Description, ICON_FOLDER)
    futil.add_handler(cmd_def.commandCreated, command_created)
    workspace = ui.workspaces.itemById(WORKSPACE_ID)
    panel = workspace.toolbarPanels.itemById(PANEL_ID)
    control = panel.controls.addCommand(cmd_def, COMMAND_BESIDE_ID, False)
    control.isPromoted = IS_PROMOTED


def stop():
    workspace = ui.workspaces.itemById(WORKSPACE_ID)
    panel = workspace.toolbarPanels.itemById(PANEL_ID)
    command_control = panel.controls.itemById(CMD_ID)
    command_definition = ui.commandDefinitions.itemById(CMD_ID)
    if command_control:
        command_control.deleteMe()
    if command_definition:
        command_definition.deleteMe()

def command_created(args: adsk.core.CommandCreatedEventArgs):
    futil.log(f'{CMD_NAME} Command Created Event')
    inputs = args.command.commandInputs
    inputs.addTextBoxCommandInput('userid','User ID',formattedText='User ID', numRows=1, isReadOnly=False)
    inputs.addTextBoxCommandInput('username','User name',formattedText='User name', numRows=1, isReadOnly=False)
    futil.add_handler(args.command.execute, command_execute, local_handlers=local_handlers)
    # user: userrec = userrec.get(userrec.id == 2)
    # ui.messageBox(f'id:{user.id}, name:{user.name}')

def command_execute(args: adsk.core.CommandEventArgs):
    futil.log(f'{CMD_NAME} Command Execute Event')
    inputs = args.command.commandInputs
    useridbox: adsk.core.TextBoxCommandInput = inputs.itemById('userid')
    usernamebox: adsk.core.TextBoxCommandInput = inputs.itemById('username')
    user = userrec()
    user.id = useridbox.text
    user.name = usernamebox.text
    print(user.save(force_insert=True))