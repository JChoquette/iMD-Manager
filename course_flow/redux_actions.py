from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Node

def dispatch_wf(workflow, action):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "workflow_" + str(workflow.pk),
        {"type": "workflow_action", "action": action},
    )


def dispatch_to_parent_wf(workflow, action):
    channel_layer = get_channel_layer()
    for parent_node in Node.objects.filter(linked_workflow=workflow):
        parent_workflow = parent_node.get_workflow()
        async_to_sync(channel_layer.group_send)(
            "workflow_" + str(parent_workflow.pk),
            {"type": "workflow_action", "action": action},
        )


def dispatch_wf_lock(workflow, action):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "workflow_" + str(workflow.pk),
        {"type": "lock_update", "action": action},
    )


# Actions for reduers
def unlock(object_id, object_type):
    return {
        "lock": False,
        "object_id": object_id,
        "object_type": object_type,
    }


def changeThroughID(through_type, old_id, new_id):
    return {
        "type": through_type + "/changeID",
        "payload": {"old_id": old_id, "new_id": new_id},
    }


def deleteSelfAction(id, objectType, parentID, extra_data):
    return {
        "type": objectType + "/deleteSelf",
        "payload": {"id": id, "parent_id": parentID, "extra_data": extra_data},
    }


def insertBelowAction(response_data, objectType):
    return {"type": objectType + "/insertBelow", "payload": response_data}


def insertChildAction(response_data, objectType):
    return {"type": objectType + "/insertChild", "payload": response_data}


def setLinkedWorkflowAction(response_data):
    return {"type": "node/setLinkedWorkflow", "payload": response_data}


def newNodeAction(response_data):
    return {"type": "node/newNode", "payload": response_data}


def newOutcomeAction(response_data):
    return {"type": "outcome/newOutcome", "payload": response_data}

def newChildOutcomeAction(response_data):
    return {"type": "childoutcome/newOutcome", "payload": response_data}


def columnChangeNodeWeek(id, delta_x, columns):
    return {
        "type": "node/movedColumnBy",
        "payload": {"id": id, "delta_x": delta_x, "columns": columns},
    }


def newNodeLinkAction(response_data):
    return {"type": "nodelink/newNodeLink", "payload": response_data}


def changeField(id, objectType, json):
    return {
        "type": objectType + "/changeField",
        "payload": {"id": id,"objectType":objectType,"json":json},
    }


def updateOutcomenodeDegreeAction(response_data):
    return {"type": "outcomenode/updateDegree", "payload": response_data}


def updateOutcomehorizontallinkDegreeAction(response_data):
    return {
        "type": "outcomehorizontallink/updateDegree",
        "payload": response_data,
    }

def updateChildOutcomehorizontallinkDegreeAction(response_data):
    return {
        "type": "childoutcomehorizontallink/updateDegree",
        "payload": response_data,
    }


def newStrategyAction(response_data):
    return {"type": "strategy/addStrategy", "payload": response_data}


def toggleStrategyAction(response_data):
    return {"type": "strategy/toggleStrategy", "payload": response_data}


def gridMenuItemAdded(response_data):
    return {"type": "gridmenu/itemAdded", "payload": response_data}



def replaceStoreData(data_package):
    return {
        "type": 'replaceStoreData',
        "payload": data_package
    }