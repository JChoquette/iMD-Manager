import * as Constants from "./Constants.js";
import {deleteSelf, insertedAt, columnChanged, updateValue, updateOutcomenodeDegree} from "./PostFunctions.js"
import * as Redux from "redux";

export const moveColumnWorkflow = (id,new_position,new_parent,child_id) => {
    return {
        type: 'columnworkflow/movedTo',
        payload:{id:id,new_index:new_position,new_parent:new_parent,child_id:child_id}
    }
}

export const moveWeekWorkflow = (id,new_position,new_parent,child_id) => {
    return {
        type: 'weekworkflow/movedTo',
        payload:{id:id,new_index:new_position,new_parent:new_parent,child_id:child_id}
    }
}

export const deleteSelfAction = (id,parentID,objectType,extra_data) => {
    return {
        type: objectType+"/deleteSelf",
        payload:{id:id,parent_id:parentID,extra_data:extra_data}
    }
}

export const insertBelowAction = (response_data,objectType) => {
    return {
        type: objectType+"/insertBelow",
        payload:response_data
    }
}

export const insertChildAction = (response_data,objectType) => {
    return {
        type: objectType+"/insertChild",
        payload:response_data
    }
}

export const setLinkedWorkflowAction = (response_data) => {
    return {
        type: "node/setLinkedWorkflow",
        payload:response_data
    }
}

export const newNodeAction = (response_data) => {
    return {
        type: "node/newNode",
        payload:response_data
    }
}

export const newOutcomeAction = (response_data) => {
    return {
        type: "outcome/newOutcome",
        payload:response_data
    }
}

export const columnChangeNodeWeek = (id,delta_x,columns) => {
    return {
        type: 'node/movedColumnBy',
        payload:{id:id,delta_x,columns:columns}
    }
}

export const moveNodeWeek = (id,new_position,new_parent,nodes_by_column,child_id) => {
    return {
        type: 'nodeweek/movedTo',
        payload:{id:id,new_index:new_position,new_parent:new_parent,nodes_by_column:nodes_by_column,child_id:child_id}
    }
}

export const newNodeLinkAction = (response_data) => {
    return {
        type: 'nodelink/newNodeLink',
        payload:response_data
    }
}

export const changeField = (id,objectType,field,value) => {
    return {
        type: objectType+'/changeField',
        payload:{id:id,field:field,value:value}
    }
}

export const moveOutcomeOutcome = (id,new_position,new_parent,child_id) => {
    return {
        type: 'outcomeoutcome/movedTo',
        payload:{id:id,new_index:new_position,new_parent:new_parent,child_id:child_id}
    }
}

export const addOutcomeToNodeAction = (response_data) => {
    return {
        type: "outcome/addToNode",
        payload:response_data
    }
}
export const addParentOutcomeToOutcomeAction = (response_data) => {
    return {
        type: "outcome/addParentOutcome",
        payload:response_data
    }
}

export const newStrategyAction = (response_data) => {
    return {
        type: "strategy/addStrategy",
        payload:response_data
    }
}
export const toggleStrategyAction = (response_data) => {
    return {
        type: "strategy/toggleStrategy",
        payload:response_data
    }
}
export const gridMenuItemAdded = (response_data) => {
    return {
        type: "gridmenu/itemAdded",
        payload:response_data
    }
}


export function workflowReducer(state={},action){
    switch(action.type){
        case 'columnworkflow/movedTo':
            var new_columnworkflow_set = state.columnworkflow_set.slice();
            for(var i=0;i<new_columnworkflow_set.length;i++){
                if(new_columnworkflow_set[i]==action.payload.id){
                    new_columnworkflow_set.splice(action.payload.new_index,0,new_columnworkflow_set.splice(i,1)[0]);
                    break;
                }
            }
            insertedAt(action.payload.child_id,"column",action.payload.new_parent,"workflow",action.payload.new_index,"columnworkflow");
            return {
                ...state,
                columnworkflow_set:new_columnworkflow_set
            }
        case 'weekworkflow/movedTo':
            var new_weekworkflow_set = state.weekworkflow_set.slice();
            for(var i=0;i<new_weekworkflow_set.length;i++){
                if(new_weekworkflow_set[i]==action.payload.id){
                    new_weekworkflow_set.splice(action.payload.new_index,0,new_weekworkflow_set.splice(i,1)[0]);
                    break;
                }
            }
            insertedAt(action.payload.child_id,"week",action.payload.new_parent,"workflow",action.payload.new_index,"weekworkflow");
            return {
                ...state,
                weekworkflow_set:new_weekworkflow_set
            }
        case 'outcomeworkflow/movedTo':
            var new_outcomeworkflow_set = state.outcomeworkflow_set.slice();
            for(var i=0;i<new_outcomeworkflow_set.length;i++){
                if(new_outcomeworkflow_set[i]==action.payload.id){
                    new_outcomeworkflow_set.splice(action.payload.new_index,0,new_outcomeworkflow_set.splice(i,1)[0]);
                    break;
                }
            }
            insertedAt(action.payload.child_id,"outcome",action.payload.new_parent,"workflow",action.payload.new_index,"outcomeworkflow");
            return {
                ...state,
                outcomeworkflow_set:new_outcomeworkflow_set
            }
        case 'week/deleteSelf':
            if(state.weekworkflow_set.indexOf(action.payload.parent_id)>=0){
                var new_state = {...state};
                new_state.weekworkflow_set = state.weekworkflow_set.slice();
                new_state.weekworkflow_set.splice(new_state.weekworkflow_set.indexOf(action.payload.parent_id),1);
                return new_state;
            }
            return state;
        case 'week/insertBelow':
            new_state = {...state}
            var new_weekworkflow_set = state.weekworkflow_set.slice();
            new_weekworkflow_set.splice(action.payload.new_through.rank,0,action.payload.new_through.id);
            new_state.weekworkflow_set = new_weekworkflow_set;
            return new_state;
        case 'outcome_base/deleteSelf':
            if(state.outcomeworkflow_set.indexOf(action.payload.parent_id)>=0){
                var new_state = {...state};
                new_state.outcomeworkflow_set = state.outcomeworkflow_set.slice();
                new_state.outcomeworkflow_set.splice(new_state.outcomeworkflow_set.indexOf(action.payload.parent_id),1);
                return new_state;
            }
            return state;
        case 'outcome_base/insertBelow':
        case 'outcome/newOutcome':
            new_state = {...state}
            var new_outcomeworkflow_set = state.outcomeworkflow_set.slice();
            new_outcomeworkflow_set.splice(action.payload.new_through.rank,0,action.payload.new_through.id);
            new_state.outcomeworkflow_set = new_outcomeworkflow_set;
            return new_state;
        case 'strategy/addStrategy':
            new_state = {...state}
            var new_weekworkflow_set = state.weekworkflow_set.slice();
            new_weekworkflow_set.splice(action.payload.index,0,action.payload.new_through.id);
            new_state.weekworkflow_set = new_weekworkflow_set;
            if(action.payload.columnworkflows_added.length>0){
                let new_columnworkflow_set = state.columnworkflow_set.slice();
                new_columnworkflow_set.push(...action.payload.columnworkflows_added.map(columnworkflow=>columnworkflow.id));
                new_state.columnworkflow_set = new_columnworkflow_set;
            }
            return new_state;
        case 'column/deleteSelf':
            if(state.columnworkflow_set.indexOf(action.payload.parent_id)>=0){
                var new_state = {...state};
                new_state.columnworkflow_set = state.columnworkflow_set.slice();
                new_state.columnworkflow_set.splice(new_state.columnworkflow_set.indexOf(action.payload.parent_id),1);
                return new_state;
            }
            return state;
        case 'node/newNode':
            if(state.columnworkflow_set.indexOf(action.payload.columnworkflow.id)>=0)return state;
            new_state = {...state}
            var new_columnworkflow_set = state.columnworkflow_set.slice();
            new_columnworkflow_set.push(action.payload.columnworkflow.id);
            new_state.columnworkflow_set = new_columnworkflow_set;
            return new_state;
        case 'column/insertBelow':
            new_state = {...state}
            var new_columnworkflow_set = state.columnworkflow_set.slice();
            new_columnworkflow_set.splice(action.payload.new_through.rank,0,action.payload.new_through.id);
            new_state.columnworkflow_set = new_columnworkflow_set;
            return new_state;
        case 'workflow/changeField':
            var new_state = {...state};
            new_state[action.payload.field]=action.payload.value;
            let json = {};
            json[action.payload.field]=action.payload.value;
            if(!read_only)updateValue(action.payload.id,"workflow",json);
            return new_state;
        default:
            return state;
    }
}

export function outcomeworkflowReducer(state={},action){
    switch(action.type){
        case 'outcome_base/deleteSelf':
            for(var i=0;i<state.length;i++){
                if(state[i].outcome==action.payload.id){
                    var new_state=state.slice();
                    new_state.splice(i,1);
                    return new_state;
                }
            }
            return state;
        case 'outcome_base/insertBelow':
            new_state = state.slice();
            new_state.push(action.payload.new_through);
            return new_state;
        case 'outcome/newOutcome':
            new_state = state.slice();
            new_state.push(action.payload.new_through);
            return new_state;
        default:
            return state;
    }
}

export function columnworkflowReducer(state={},action){
    switch(action.type){
        case 'column/deleteSelf':
            for(var i=0;i<state.length;i++){
                if(state[i].id==action.payload.parent_id){
                    var new_state=state.slice();
                    new_state.splice(i,1);
                    return new_state;
                }
            }
            return state;
        case 'node/newNode':
            for(var i=0;i<state.length;i++){
                if(state[i].id==action.payload.columnworkflow.id)return state;
            }
            new_state = state.slice();
            new_state.push(action.payload.columnworkflow);
            return new_state;
        case 'column/insertBelow':
            new_state = state.slice();
            new_state.push(action.payload.new_through);
            return new_state;
        case 'strategy/addStrategy':
            if(action.payload.columnworkflows_added.length==0)return state;
            new_state=state.slice();
            new_state.push(...action.payload.columnworkflows_added);
            return new_state;
        default:
            return state;
    }
}

export function columnReducer(state={},action){
    switch(action.type){
        case 'column/deleteSelf':
            for(var i=0;i<state.length;i++){
                if(state[i].id==action.payload.id){
                    var new_state = state.slice();
                    new_state.splice(i,1);
                    deleteSelf(action.payload.id,"column");
                    return new_state;
                }
            }
            return state;
        case 'node/newNode':
            for(var i=0;i<state.length;i++){
                if(state[i].id==action.payload.column.id)return state;
            }
            new_state = state.slice();
            new_state.push(action.payload.column);
            return new_state;
        case 'column/insertBelow':
            new_state = state.slice();
            new_state.push(action.payload.new_model);
            return new_state;
        case 'column/changeField':
            for(var i=0;i<state.length;i++){
                if(state[i].id==action.payload.id){
                    var new_state = state.slice();
                    new_state[i] = {...state[i]};
                    new_state[i][action.payload.field]=action.payload.value;
                    let json = {};
                    json[action.payload.field]=action.payload.value;
                    if(!read_only)updateValue(action.payload.id,"column",json);
                    return new_state;
                }
            }
            return state;
        case 'strategy/addStrategy':
            if(action.payload.columns_added.length==0)return state;
            new_state=state.slice();
            new_state.push(...action.payload.columns_added);
            return new_state;
        default:
            return state;
    }
}

export function weekworkflowReducer(state={},action){
    switch(action.type){
        case 'week/deleteSelf':
            for(var i=0;i<state.length;i++){
                if(state[i].id==action.payload.parent_id){
                    var new_state=state.slice();
                    new_state.splice(i,1);
                    return new_state;
                }
            }
            return state;
        case 'week/insertBelow':
            new_state = state.slice();
            new_state.push(action.payload.new_through);
            return new_state;
        case 'strategy/addStrategy':
            new_state=state.slice();
            new_state.push(action.payload.new_through);
            return new_state;
        default:
            return state;
    }
}
export function weekReducer(state={},action){
    switch(action.type){
        case 'nodeweek/movedTo':
            let old_parent,old_parent_index,new_parent,new_parent_index;
            for(var i=0;i<state.length;i++){
                if(state[i].nodeweek_set.indexOf(action.payload.id)>=0){
                    old_parent_index=i;
                    old_parent={...state[i]};
                }
                if(state[i].id==action.payload.new_parent){
                    new_parent_index=i;
                    new_parent={...state[i]};
                }
            }
            var new_index = action.payload.new_index;
            //Correction for if we are in a term:
            if(action.payload.nodes_by_column){
                for(var col in action.payload.nodes_by_column){
                    if(action.payload.nodes_by_column[col].indexOf(action.payload.id)>=0){
                        let previous = action.payload.nodes_by_column[col][new_index];
                        new_index = new_parent.nodeweek_set.indexOf(previous);
                    }
                }
            }
            
            
            var new_state = state.slice();
            old_parent.nodeweek_set= old_parent.nodeweek_set.slice();
            old_parent.nodeweek_set.splice(old_parent.nodeweek_set.indexOf(action.payload.id),1);
            if(old_parent_index==new_parent_index){
                old_parent.nodeweek_set.splice(new_index,0,action.payload.id);
            }else{
                new_parent.nodeweek_set = new_parent.nodeweek_set.slice();
                new_parent.nodeweek_set.splice(new_index,0,action.payload.id);
                new_state.splice(new_parent_index,1,new_parent);
                
            }
            new_state.splice(old_parent_index,1,old_parent);
            insertedAt(action.payload.child_id,"node",new_parent.id,"week",new_index,"nodeweek");
            return new_state;
        case 'node/deleteSelf':
            for(var i=0;i<state.length;i++){
                if(state[i].nodeweek_set.indexOf(action.payload.parent_id)>=0){
                    var new_state=state.slice();
                    new_state[i] = {...new_state[i]};
                    new_state[i].nodeweek_set = state[i].nodeweek_set.slice();
                    new_state[i].nodeweek_set.splice(new_state[i].nodeweek_set.indexOf(action.payload.parent_id),1);
                    return new_state;
                }
            }
            return state;
        case 'node/insertBelow':
            for(var i=0;i<state.length;i++){
                if(state[i].id==action.payload.parentID){
                    var new_state = state.slice();
                    new_state[i] = {...state[i]}
                    var new_nodeweek_set = state[i].nodeweek_set.slice();
                    new_nodeweek_set.splice(action.payload.new_through.rank,0,action.payload.new_through.id);
                    new_state[i].nodeweek_set = new_nodeweek_set;
                    return new_state;
                }
            }
            return state;
        case 'node/newNode':
            for(var i=0;i<state.length;i++){
                if(state[i].id==action.payload.parentID){
                    var new_state = state.slice();
                    new_state[i] = {...state[i]}
                    var new_nodeweek_set = state[i].nodeweek_set.slice();
                    new_nodeweek_set.splice(action.payload.index,0,action.payload.new_through.id);
                    new_state[i].nodeweek_set = new_nodeweek_set;
                    return new_state;
                }
            }
            return state;
        case 'week/insertBelow':
            new_state = state.slice();
            new_state.push(action.payload.new_model);
            return new_state;
        case 'week/deleteSelf':
            for(var i=0;i<state.length;i++){
                if(state[i].id==action.payload.id){
                    var new_state = state.slice();
                    new_state.splice(i,1);
                    deleteSelf(action.payload.id,"week");
                    return new_state;
                }
            }
            return state;
        case 'week/changeField':
            for(var i=0;i<state.length;i++){
                if(state[i].id==action.payload.id){
                    var new_state = state.slice();
                    new_state[i] = {...state[i]};
                    new_state[i][action.payload.field]=action.payload.value;
                    let json = {};
                    json[action.payload.field]=action.payload.value;
                    if(!read_only)updateValue(action.payload.id,"week",json);
                    return new_state;
                }
            }
            return state;
        case 'strategy/toggleStrategy':
            for(var i=0;i<state.length;i++){
                if(state[i].id==action.payload.id){
                    var new_state = state.slice();
                    new_state[i] = {...state[i]};
                    new_state[i].is_strategy = action.payload.is_strategy;
                    return new_state;
                }
            }
            return state;
        case 'strategy/addStrategy':
            new_state=state.slice();
            new_state.push(action.payload.strategy);
            return new_state;
        default:
            return state;
    }
}
export function nodeweekReducer(state={},action){
    switch(action.type){
        case 'node/deleteSelf':
            for(var i=0;i<state.length;i++){
                if(state[i].id==action.payload.parent_id){
                    var new_state=state.slice();
                    new_state.splice(i,1);
                    return new_state;
                }
            }
            return state;
        case 'nodeweek/movedTo':
            new_state = state.slice();
            for(var i=0;i<state.length;i++){
                if(state[i].id==action.payload.id){
                    new_state[i]={...state[i],week:action.payload.new_parent}
                }
            }
            return new_state;
        case 'week/insertBelow':
            if(!action.payload.children_through)return state;
            new_state = state.slice();
            for(var i=0;i<action.payload.children_through.length;i++){
                new_state.push(action.payload.children_through[i]);
            }
            return new_state;
        case 'node/insertBelow':
        case 'node/newNode':
            new_state = state.slice();
            new_state.push(action.payload.new_through);
            return new_state;
        case 'strategy/addStrategy':
            if(action.payload.nodeweeks_added.length==0)return state;
            new_state=state.slice();
            new_state.push(...action.payload.nodeweeks_added);
            return new_state;
        default:
            return state;
    }
}
export function nodeReducer(state={},action){
    switch(action.type){
        case 'column/deleteSelf':
            var new_state = state.slice();
            var new_column;
            if(action.payload.extra_data){
                new_column = action.payload.extra_data[0];
                if(new_column==action.payload.id)new_column=action.payload.extra_data[1];
            }
            
            for(var i=0;i<state.length;i++){
                if(state[i].column==action.payload.id){
                    new_state[i]={...state[i]};
                    new_state[i].column=new_column;
                }
            }
            return new_state;
        case 'node/movedColumnBy':
            var new_state = state.slice();
            for(var i=0;i<state.length;i++){
                if(state[i].id==action.payload.id){
                    try{
                        let columns = action.payload.columns;
                        let old_column_index = columns.indexOf(state[i].column);
                        let new_column_index = old_column_index+action.payload.delta_x;
                        if(new_column_index<0 || new_column_index>=columns.length)return state;
                        let new_column = columns[new_column_index];
                        var new_nodedata = {
                            ...state[i],
                            column:new_column,
                        };
                        new_state.splice(i,1,new_nodedata);
                        columnChanged(action.payload.id,new_column);
                    }catch(err){console.log("couldn't find new column");return state;}
                    return new_state;
                }
            }
            return state;
        case 'node/deleteSelf':
            for(var i=0;i<state.length;i++){
                if(state[i].id==action.payload.id){
                    var new_state = state.slice();
                    new_state.splice(i,1);
                    deleteSelf(action.payload.id,"node",
                    ()=>{Constants.triggerHandlerEach($(".week .node"),"component-updated")});
                    return new_state;
                }
            }
            return state;
        case 'nodelink/deleteSelf':
            for(var i=0;i<state.length;i++){
                if(state[i].outgoing_links.indexOf(action.payload.id)>=0){
                    var new_state=state.slice();
                    new_state[i] = {...new_state[i]};
                    new_state[i].outgoing_links = state[i].outgoing_links.slice();
                    new_state[i].outgoing_links.splice(new_state[i].outgoing_links.indexOf(action.payload.id),1);
                    return new_state;
                }
            }
            return state;
        case 'outcomenode/deleteSelf':
            for(var i=0;i<state.length;i++){
                if(state[i].outcomenode_set.indexOf(action.payload.id)>=0){
                    var new_state=state.slice();
                    new_state[i] = {...new_state[i]};
                    new_state[i].outcomenode_set = state[i].outcomenode_set.slice();
                    new_state[i].outcomenode_set.splice(new_state[i].outcomenode_set.indexOf(action.payload.id),1);
                    return new_state;
                }
            }
            return state;
        case 'week/insertBelow':
            if(!action.payload.children)return state;
            new_state = state.slice();
            for(var i=0;i<action.payload.children.length;i++){
                new_state.push(action.payload.children[i]);
            }
            return new_state;
        case 'node/insertBelow':
        case 'node/newNode':
            new_state = state.slice();
            new_state.push(action.payload.new_model);
            return new_state;
        case 'node/changeField':
            for(var i=0;i<state.length;i++){
                if(state[i].id==action.payload.id){
                    var new_state = state.slice();
                    new_state[i] = {...state[i]};
                    new_state[i][action.payload.field]=action.payload.value;
                    let json = {};
                    json[action.payload.field]=action.payload.value;
                    if(!read_only)updateValue(action.payload.id,"node",json);
                    return new_state;
                }
            }
            return state;
        case 'node/setLinkedWorkflow':
            for(var i=0;i<state.length;i++){
                if(state[i].id==action.payload.id){
                    var new_state = state.slice();
                    new_state[i] = {...state[i]};
                    new_state[i].linked_workflow=action.payload.linked_workflow;
                    new_state[i].linked_workflow_title = action.payload.linked_workflow_title;
                    new_state[i].linked_workflow_description = action.payload.linked_workflow_description;
                    return new_state;
                }
            }
            return state;
        case 'nodelink/newNodeLink':
            for(var i=0;i<state.length;i++){
                if(state[i].id==action.payload.new_model.source_node){
                    var new_state = state.slice();
                    new_state[i] = {...state[i]}
                    var new_outgoing_links = state[i].outgoing_links.slice();
                    new_outgoing_links.push(action.payload.new_model.id);
                    new_state[i].outgoing_links = new_outgoing_links;
                    return new_state;
                }
            }
            return state;
        case 'outcome/addToNode':
            //Returns -1 if the outcome had already been added to the node
            if(action.payload.outcomenode==-1)return state;
            for(var i=0;i<state.length;i++){
                if(state[i].id==action.payload.outcomenode.node){
                    var new_state=state.slice();
                    new_state[i] = {...new_state[i]};
                    new_state[i].outcomenode_set = new_state[i].outcomenode_set.slice();
                    new_state[i].outcomenode_set.push(action.payload.outcomenode.id);
                    return new_state;
                }
            }
            return state;
        case 'strategy/addStrategy':
            if(action.payload.nodes_added.length==0)return state;
            new_state=state.slice();
            new_state.push(...action.payload.nodes_added);
            return new_state;
        case 'outcome/deleteSelf':
        case 'outcome_base/deleteSelf':
            new_state=state.slice();
            for(var i=0;i<action.payload.extra_data.length;i++){
                console.log("iteration "+i);
                console.log(action.payload.extra_data[i]);
                console.log(action.payload);
                if(action.payload.extra_data[i].outcome==action.payload.id){
                    console.log("found an outcomenode for the deleted outcome");
                    let outcomenode = action.payload.extra_data[i];
                    for(var j=0;j<new_state.length;j++){
                        console.log("sub-iteration "+j);
                        console.log(new_state[j])
                        let outcomenode_index=new_state[j].outcomenode_set.indexOf(outcomenode.id);
                        if(outcomenode_index>=0){
                            console.log("removing outcomenode from state");
                            console.log(new_state[j].outcomenode_set);
                            new_state[j]={...new_state[j]};
                            new_state[j].outcomenode_set=new_state[j].outcomenode_set.slice();
                            new_state[j].outcomenode_set.splice(outcomenode_index,1);
                            console.log(new_state[j].outcomenode_set);
                        }
                    }
                }
            }
            return new_state;
        default:
            return state;
    }
}
export function nodelinkReducer(state={},action){
    switch(action.type){
        case 'node/insertBelow':
        case 'node/newNode':
        case 'node/deleteSelf':
            return state;
        case 'nodelink/newNodeLink':
            new_state = state.slice();
            new_state.push(action.payload.new_model);
            return new_state;
        case 'nodelink/deleteSelf':
            for(var i=0;i<state.length;i++){
                if(state[i].id==action.payload.id){
                    var new_state = state.slice();
                    new_state.splice(i,1);
                    deleteSelf(action.payload.id,"nodelink")
                    return new_state;
                }
            }
            return state;
        case 'strategy/addStrategy':
            if(action.payload.nodelinks_added.length==0)return state;
            new_state=state.slice();
            new_state.push(...action.payload.nodelinks_added);
            return new_state;
        default:
            return state;
    }
}
export function outcomeReducer(state={},action){
    switch(action.type){
        case 'outcomeoutcome/movedTo':
            let old_parent, old_parent_index,new_parent,new_parent_index;
            for(var i=0;i<state.length;i++){
                if(state[i].child_outcome_links.indexOf(action.payload.id)>=0){
                    old_parent_index=i;
                    old_parent={...state[i]};
                }
                if(state[i].id==action.payload.new_parent){
                    new_parent_index=i;
                    new_parent={...state[i]};
                }
            }
            var new_index = action.payload.new_index;
            var new_state = state.slice();
            old_parent.child_outcome_links = old_parent.child_outcome_links.slice();
            old_parent.child_outcome_links.splice(old_parent.child_outcome_links.indexOf(action.payload.id),1);
            if(old_parent_index==new_parent_index){
                old_parent.child_outcome_links.splice(new_index,0,action.payload.id);
            }else{
                new_parent.child_outcome_links = new_parent.child_outcome_links.slice();
                new_parent.child_outcome_links.splice(new_index,0,action.payload.id);
                new_state.splice(new_parent_index,1,new_parent);
            }
            new_state.splice(old_parent_index,1,old_parent);
            insertedAt(action.payload.child_id,"outcome",new_parent.id,"outcome",new_index,"outcomeoutcome");
            return new_state;
        case 'outcome_base/deleteSelf':
            var new_state=state.slice();
            for(var i=0;i<state.length;i++){
                if(state[i].id==action.payload.id){
                    new_state.splice(i,1);
                    deleteSelf(action.payload.id,"outcome");
                    return new_state;
                }
            }
            return state;
        case 'outcome/deleteSelf':
            var new_state=state.slice();
            for(var i=0;i<state.length;i++){
                if(state[i].child_outcome_links.indexOf(action.payload.parent_id)>=0){
                    new_state[i] = {...new_state[i]};
                    new_state[i].child_outcome_links = state[i].child_outcome_links.slice();
                    new_state[i].child_outcome_links.splice(new_state[i].child_outcome_links.indexOf(action.payload.parent_id),1);
                }else if(state[i].id==action.payload.id){
                    new_state.splice(i,1);
                    deleteSelf(action.payload.id,"outcome");
                }
            }
            return new_state;
        case "outcome_base/insertBelow":
        case 'outcome/newOutcome':
            var new_state=state.slice();
            new_state.push(action.payload.new_model);
            if(action.payload.children){
                for(var i=0;i<action.payload.children.length;i++){
                    new_state.push(action.payload.children[i]);
                }
            }
            return new_state;
        case 'outcome/insertChild':
        case 'outcome_base/insertChild':
        case 'outcome/insertBelow':
            for(var i=0;i<state.length;i++){
                if(state[i].id==action.payload.parentID){
                    var new_state = state.slice();
                    new_state[i] = {...state[i]}
                    var new_child_outcome_links = state[i].child_outcome_links.slice();
                    let new_index;
                    new_index= action.payload.new_through.rank;
                    new_child_outcome_links.splice(new_index,0,action.payload.new_through.id);
                    new_state[i].child_outcome_links = new_child_outcome_links;
                    new_state.push(action.payload.new_model);
                    if(action.payload.children){
                        for(var i=0;i<action.payload.children.length;i++){
                            new_state.push(action.payload.children[i]);
                        }
                    }
                    return new_state;
                }
            }
            return state;
        case 'outcome/changeField':
            for(var i=0;i<state.length;i++){
                if(state[i].id==action.payload.id){
                    var new_state = state.slice();
                    new_state[i] = {...state[i]};
                    new_state[i][action.payload.field]=action.payload.value;
                    let json = {};
                    json[action.payload.field]=action.payload.value;
                    if(!read_only)updateValue(action.payload.id,"outcome",json);
                    return new_state;
                }
            }
            return state;
        case 'outcomehorizontallink/deleteSelf':
            console.log("payload")
            console.log(action.payload);
            var new_state = state.slice();
            for(var i=0;i<new_state.length;i++){
                if(new_state[i].outcome_horizontal_links.indexOf(action.payload.id)>=0){
                    new_state[i]={...new_state[i], outcome_horizontal_links:new_state[i].outcome_horizontal_links.slice()};
                    new_state[i].outcome_horizontal_links.splice(new_state[i].outcome_horizontal_links.indexOf(action.payload.id),1);
                }
            }
            return new_state;
        case 'outcome/addParentOutcome':
            //Returns -1 if the outcome had already been added to the node
            if(action.payload.outcomenode==-1)return state;
            for(var i=0;i<state.length;i++){
                if(state[i].id==action.payload.outcomehorizontallink.outcome){
                    var new_state=state.slice();
                    new_state[i] = {...new_state[i]};
                    new_state[i].outcome_horizontal_links = new_state[i].outcome_horizontal_links.slice();
                    new_state[i].outcome_horizontal_links.push(action.payload.outcomehorizontallink.id);
                    return new_state;
                }
            }
            return state;
        default:
            return state;
    }
}
export function outcomeOutcomeReducer(state={},action){
    switch(action.type){
        case 'outcome/deleteSelf':
            for(var i=0;i<state.length;i++){
                if(state[i].id==action.payload.parent_id){
                    var new_state=state.slice();
                    new_state.splice(i,1);
                    return new_state;
                }
            }
            return state;
        case 'outcome_base/insertBelow':
            var new_state = state.slice();
            if(action.payload.children_through){
                for(var i=0;i<action.payload.children_through.length;i++){
                    new_state.push(action.payload.children_through[i]);
                }
            }
            return new_state;
        case 'outcome/insertChild':
        case 'outcome/insertBelow':
            var new_state = state.slice();
            new_state.push(action.payload.new_through);
            if(action.payload.children_through){
                for(var i=0;i<action.payload.children_through.length;i++){
                    new_state.push(action.payload.children_through[i]);
                }
            }
            return new_state;
        default:
            return state;
    }
}
export function outcomeNodeReducer(state={},action){
    switch(action.type){
        case 'outcome/addToNode':
            //Returns -1 if the outcome had already been added to the node
            if(action.payload.outcomenode==-1)return state;
            var new_state = state.slice();
            new_state.push(action.payload.outcomenode);
            return new_state;
        case 'outcomenode/deleteSelf':
            for(var i=0;i<state.length;i++){
                if(state[i].id==action.payload.id){
                    var new_state = state.slice();
                    updateOutcomenodeDegree(state[i].node,state[i].outcome,0)
                    new_state.splice(i,1);
                    return new_state;
                }
            }
            return state;
        case 'outcomenode/changeField':
            for(var i=0;i<state.length;i++){
                if(state[i].id==action.payload.id){
                    var new_state = state.slice();
                    new_state[i] = {...state[i]};
                    new_state[i][action.payload.field]=action.payload.value;
                    let json = {};
                    json[action.payload.field]=action.payload.value;
                    if(!read_only)updateOutcomenodeDegree(new_state[i].node,new_state[i].outcome,action.payload.value);
                    return new_state;
                }
            }
            return state;
        case 'outcome/deleteSelf':
        case 'outcome_base/deleteSelf':
            new_state=state.slice();
            for(var i=0;i<new_state.length;i++){
                if(new_state[i].outcome==action.payload.id){
                    new_state.splice(i,1);
                    i--;
                }
            }
            return new_state;
        default:
            return state;
    }
}
export function parentOutcomeReducer(state={},action){
    return state;
}
export function parentOutcomeoutcomeReducer(state={},action){
    return state;
}
export function parentOutcomeworkflowReducer(state={},action){
    return state;
}
export function parentOutcomenodeReducer(state={},action){
    return state;
}
export function outcomeHorizontalLinkReducer(state={},action){
    switch(action.type){
        case 'outcome/addParentOutcome':
            //Returns -1 if the outcome had already been added to the outcome
            if(action.payload.outcomehorizontallink==-1)return state;
            var new_state = state.slice();
            new_state.push(action.payload.outcomehorizontallink);
            return new_state;
        case 'outcomehorizontallink/deleteSelf':
            for(var i=0;i<state.length;i++){
                if(state[i].id==action.payload.id){
                    var new_state = state.slice();
                    deleteSelf(action.payload.id,"outcomehorizontallink");
                    new_state.splice(i,1);
                    return new_state;
                }
            }
            return state;
        default:
        return state;
    }
}
export function parentWorkflowReducer(state={},action){
    return state;
}
export function outcomeProjectReducer(state={},action){
    switch(action.type){
        default:
            return state;
    }
}
export function strategyReducer(state={},action){
    switch(action.type){
        case 'strategy/toggleStrategy':
            if(!action.payload.is_strategy)return state;
            let new_state=state.slice();
            new_state.push(action.payload.strategy);
            return new_state;
        default:
            return state;
    }
}
export function saltiseStrategyReducer(state={},action){
    switch(action.type){
        default:
            return state;
    }
}

export function gridMenuReducer(state={},action){
    switch(action.type){
        case 'gridmenu/itemAdded':
            var new_state = {...state}
            if(action.payload.type!="project"){
                new_state.owned_strategies = {...new_state.owned_strategies };
                new_state.owned_strategies.sections = new_state.owned_strategies.sections.slice();
                for(var i=0;i<new_state.owned_projects.sections.length;i++){
                    if(new_state.owned_strategies.sections[i].object_type==action.payload.type){
                        new_state.owned_strategies.sections[i].objects=new_state.owned_strategies.sections[i].objects.slice()
                        new_state.owned_strategies.sections[i].objects.push(action.payload.new_item);
                    }
                }
            }else{
                new_state.owned_projects = {...new_state.owned_projects};
                new_state.owned_projects.sections = new_state.owned_projects.sections.slice();
                for(var i=0;i<new_state.owned_projects.sections.length;i++){
                    if(new_state.owned_projects.sections[i].object_type==action.payload.type){
                        new_state.owned_projects.sections[i].objects=new_state.owned_projects.sections[i].objects.slice()
                        new_state.owned_projects.sections[i].objects.push(action.payload.new_item);
                    }
                }
            }
            return new_state;
        default:
            return state;
    }
}
export function projectMenuReducer(state={},action){
    switch(action.type){
        case 'gridmenu/itemAdded':
            var new_state = {...state}
            console.log("item has been added");
            console.log("the old state is:")
            console.log(state);
            new_state.current_project = {...new_state.current_project};
            new_state.current_project.sections = new_state.current_project.sections.slice();
            console.log("we are looking to add:");
            console.log(action.payload);
            for(var i=0;i<new_state.current_project.sections.length;i++){
                console.log(new_state.current_project.sections[i].object_type);
                if(new_state.current_project.sections[i].object_type==action.payload.type){
                    new_state.current_project.sections[i].objects=new_state.current_project.sections[i].objects.slice()
                    new_state.current_project.sections[i].objects.push(action.payload.new_item);
                }
            }
            return new_state;
        default:
            return state;
    }
}


export const rootWorkflowReducer = Redux.combineReducers({
    workflow:workflowReducer,
    outcomeworkflow:outcomeworkflowReducer,
    columnworkflow:columnworkflowReducer,
    column:columnReducer,
    weekworkflow:weekworkflowReducer,
    week:weekReducer,
    nodeweek:nodeweekReducer,
    node:nodeReducer,
    nodelink:nodelinkReducer,
    outcome:outcomeReducer,
    outcomeoutcome:outcomeOutcomeReducer,
    outcomenode:outcomeNodeReducer,
    parent_outcome:parentOutcomeReducer,
    parent_outcomeoutcome:parentOutcomeoutcomeReducer,
    parent_outcomeworkflow:parentOutcomeworkflowReducer,
    parent_outcomenode:parentOutcomenodeReducer,
    parent_workflow:parentWorkflowReducer,
    outcomehorizontallink:outcomeHorizontalLinkReducer,
    outcomeproject:outcomeProjectReducer,
    strategy:strategyReducer,
    saltise_strategy:saltiseStrategyReducer,
});

export const rootOutcomeReducer = Redux.combineReducers({
    outcome:outcomeReducer,
    outcomeoutcome:outcomeOutcomeReducer,
});
