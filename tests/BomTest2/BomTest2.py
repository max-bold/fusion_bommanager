# Author-
# Description-

import adsk.core
import adsk.fusion
import adsk.cam
import traceback


class comlist(list):
    def names(self) -> list:
        res = []
        for com in self:
            res.append(com['name'])
        return res

    def byname(self, name: str) -> dict:
        for com in self:
            if com['name'] == name:
                return com
        return None


def getflatbom(root: adsk.fusion.Component) -> comlist:
    ocs = root.allOccurrences
    cl = comlist()
    for oc in ocs:
        component = oc.component
        if component.allOccurrences.count > 0:
            comtype = 'assembly'
        else:
            comtype = 'part'
        # if not haschildren:
        if component.name in cl.names():
            cl.byname(component.name)['count'] += 1
        else:
            rec = {
                'name': component.name,
                'id': component.id,
                'type': comtype,
                'count': 1,
                'partnumber':component.partNumber,
                'description':component.description
            }
            cl.append(rec)
    return cl


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)

        if design:
            root = design.rootComponent
            print(f'root.id: {root.id}')
            comdict = getflatbom(root)
            for rec in comdict:
                print(rec)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
