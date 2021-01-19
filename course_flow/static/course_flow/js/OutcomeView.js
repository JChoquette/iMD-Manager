import * as React from "react";
import * as reactDom from "react-dom";
import {Provider, connect} from "react-redux";
import {ComponentJSON, TitleText} from "./ComponentJSON.js";
import OutcomeOutcomeView from "./OutcomeOutcomeView.js";
import {OutcomeBarOutcomeOutcomeView, NodeOutcomeOutcomeView, TableOutcomeOutcomeView} from "./OutcomeOutcomeView.js";
import {TableOutcomeGroup, TableTotalCell} from "./OutcomeNode.js";
import {getOutcomeByID} from "./FindState.js";
import {changeField, moveOutcomeOutcome} from "./Reducers.js";

//Basic component representing an outcome
class OutcomeView extends ComponentJSON{
    
    constructor(props){
        super(props);
        this.objectType="outcome";
        this.children_block = React.createRef();
    }
    
    render(){
        let data = this.props.data;
        
        var children = data.child_outcome_links.map((outcomeoutcome)=>
            <OutcomeOutcomeView key={outcomeoutcome} objectID={outcomeoutcome} parentID={data.id} selection_manager={this.props.selection_manager} />
        );
        
        let actions=[];
        if(!read_only)actions.push(this.addInsertChild(data));
        if(!read_only && data.depth>0){
            actions.push(this.addInsertSibling(data));
            actions.push(this.addDuplicateSelf(data));
            actions.push(this.addDeleteSelf(data));
        }
        
        let dropIcon;
        if(data.is_dropped)dropIcon = "droptriangleup";
        else dropIcon = "droptriangledown";
        
        let droptext;
        if(data.is_dropped)droptext="hide";
        else droptext = "show "+children.length+" descendant"+((children.length>1&&"s")||"")
        
        return(
            <div
            class={
                "outcome"+((this.state.selected && " selected")||"")+((data.is_dropped && " dropped")||"")
            }
            ref={this.maindiv} 
            onClick={(evt)=>this.props.selection_manager.changeSelection(evt,this)}>
                <div class="outcome-title">
                    <TitleText text={data.title} defaultText={"Click to edit"}/>
                </div>
                {children.length>0 && 
                    <div class="outcome-drop" onClick={this.toggleDrop.bind(this)}>
                        <div class = "outcome-drop-img">
                            <img src={iconpath+dropIcon+".svg"}/>
                        </div>
                        <div class = "outcome-drop-text">
                            {droptext}
                        </div>
                    </div>
                }
                <div class="children-block" id={this.props.objectID+"-children-block"} ref={this.children_block}>
                    {children}
                </div>
                {!read_only && <div class="mouseover-actions">
                    {actions}
                </div>
                }
                {this.addEditable(data)}
            </div>
            
        );
    }
    
    postMountFunction(){
        
        this.makeSortable($(this.children_block.current),this.props.objectID,"outcomeoutcome",".outcomeoutcome",false,false,".children-block",false);
    }


    toggleDrop(){
        this.props.dispatch(changeField(this.props.objectID,this.objectType,"is_dropped",!this.props.data.is_dropped));
    }

    sortableMovedFunction(id,new_position,type,new_parent){
        this.props.dispatch(moveOutcomeOutcome(id,new_position,new_parent));
    }

    stopSortFunction(){
        
    }
    
    
}
const mapOutcomeStateToProps = (state,own_props)=>(
    getOutcomeByID(state,own_props.objectID)
)
export default connect(
    mapOutcomeStateToProps,
    null
)(OutcomeView)


//Basic component representing an outcome in the outcome bar
class OutcomeBarOutcomeViewUnconnected extends ComponentJSON{
    
    constructor(props){
        super(props);
        this.objectType="outcome";
        this.children_block = React.createRef();
    }
    
    render(){
        let data = this.props.data;
        
        var children = data.child_outcome_links.map((outcomeoutcome)=>
            <OutcomeBarOutcomeOutcomeView key={outcomeoutcome} objectID={outcomeoutcome} parentID={data.id} selection_manager={this.props.selection_manager}/>
        );
                
        let dropIcon;
        if(data.is_dropped)dropIcon = "droptriangleup";
        else dropIcon = "droptriangledown";
        
        let droptext;
        if(data.is_dropped)droptext="hide";
        else droptext = "show "+children.length+" descendant"+((children.length>1&&"s")||"")
        
        return(
            <div
            class={
                "outcome"+((data.is_dropped && " dropped")||"")
            }
            ref={this.maindiv}>
                <div class="outcome-title">
                    <TitleText text={data.title} defaultText={"Click to edit"}/>
                </div>
                {children.length>0 && 
                    <div class="outcome-drop" onClick={this.toggleDrop.bind(this)}>
                        <div class = "outcome-drop-img">
                            <img src={iconpath+dropIcon+".svg"}/>
                        </div>
                        <div class = "outcome-drop-text">
                            {droptext}
                        </div>
                    </div>
                }
                <div class="children-block" id={this.props.objectID+"-children-block"} ref={this.children_block}>
                    {children}
                </div>
            </div>
            
        );
    }
    
    toggleDrop(){
        this.props.dispatch(changeField(this.props.objectID,this.objectType,"is_dropped",!this.props.data.is_dropped));
    }


    makeDraggable(){
        let draggable_selector = "outcome"
        let draggable_type = "outcome"
        $(this.maindiv.current).draggable({
            helper:(e,item)=>{
                var helper = $(document.createElement('div'));
                helper.addClass("outcome-ghost");
                helper.appendTo(document.body);
                return helper;
            },
            cursor:"move",
            cursorAt:{top:20,left:100},
            distance:10,
            start:(e,ui)=>{
                $(".workflow-canvas").addClass("dragging-"+draggable_type);
                $(draggable_selector).addClass("dragging");
            },
            stop:(e,ui)=>{
                $(".workflow-canvas").removeClass("dragging-"+draggable_type);
                $(draggable_selector).removeClass("dragging");
            }
        });
    }
    
    postMountFunction(){
        this.makeDraggable();
        $(this.maindiv.current)[0].dataDraggable={outcome:this.props.data.id}
    }

}
export const OutcomeBarOutcomeView = connect(
    mapOutcomeStateToProps,
    null
)(OutcomeBarOutcomeViewUnconnected)


//Basic component representing an outcome in a node
class NodeOutcomeViewUnconnected extends ComponentJSON{
    
    constructor(props){
        super(props);
        this.objectType="outcome";
        this.children_block = React.createRef();
    }
    
    render(){
        let data = this.props.data;
        
        var children = data.child_outcome_links.map((outcomeoutcome)=>
            <NodeOutcomeOutcomeView key={outcomeoutcome} objectID={outcomeoutcome} parentID={data.id} selection_manager={this.props.selection_manager}/>
        );
                
        let dropIcon;
        if(data.is_dropped)dropIcon = "droptriangleup";
        else dropIcon = "droptriangledown";
        
        let droptext;
        if(data.is_dropped)droptext="hide";
        else droptext = "show "+children.length+" descendant"+((children.length>1&&"s")||"")
        
        return(
            <div
            class={
                "outcome"+((data.is_dropped && " dropped")||"")
            }
            ref={this.maindiv}>
                <div class="outcome-title">
                    <TitleText text={data.title} defaultText={"Click to edit"}/>
                </div>
                {children.length>0 && 
                    <div class="outcome-drop" onClick={this.toggleDrop.bind(this)}>
                        <div class = "outcome-drop-img">
                            <img src={iconpath+dropIcon+".svg"}/>
                        </div>
                        <div class = "outcome-drop-text">
                            {droptext}
                        </div>
                    </div>
                }
                <div class="children-block" id={this.props.objectID+"-children-block"} ref={this.children_block}>
                    {children}
                </div>
            </div>
            
        );
    }
    
    toggleDrop(){
        this.props.dispatch(changeField(this.props.objectID,this.objectType,"is_dropped",!this.props.data.is_dropped));
    }

}
export const NodeOutcomeView = connect(
    mapOutcomeStateToProps,
    null
)(NodeOutcomeViewUnconnected)

//Basic component representing an outcome inside a table
class TableOutcomeViewUnconnected extends ComponentJSON{
    
    constructor(props){
        super(props);
        this.objectType="outcome";
        this.children_block = React.createRef();
        this.child_completion_status={};
        this.state={completion_status_from_children:{},completion_status_from_self:{}};
    }
    
    render(){
        let data = this.props.data;
        let completion_status_to_pass = {...this.props.completion_status_from_parents};
        for(let node_id in this.state.completion_status_from_self){
            completion_status_to_pass[node_id] |= this.state.completion_status_from_self[node_id];
        }
        
        var children = data.child_outcome_links.map((outcomeoutcome)=>
            <TableOutcomeOutcomeView key={outcomeoutcome} objectID={outcomeoutcome} parentID={data.id} selection_manager={this.props.selection_manager} nodecategory={this.props.nodecategory} updateParentCompletion={this.childUpdatedFunction.bind(this,outcomeoutcome)} completion_status_from_parents={completion_status_to_pass} outcomes_type={this.props.outcomes_type}/>
        );

        let outcomeGroups = this.props.nodecategory.map((nodecategory)=>
            <TableOutcomeGroup nodes={nodecategory.nodes} outcomeID={this.props.data.id} updateParentCompletion={this.props.updateParentCompletion} updateSelfCompletion={this.selfUpdatedFunction.bind(this)} completion_status_from_children={this.state.completion_status_from_children} completion_status_from_parents={this.props.completion_status_from_parents} completion_status_from_self = {this.state.completion_status_from_self} outcomes_type={this.props.outcomes_type}/>
                                                        
                                                         
        );
                
        let dropIcon;
        if(data.is_dropped)dropIcon = "droptriangleup";
        else dropIcon = "droptriangledown";
        
        let droptext;
        if(data.is_dropped)droptext="hide";
        else droptext = "show "+children.length+" descendant"+((children.length>1&&"s")||"")
        

        let completion_status=0;
        for(let node_id in this.props.completion_status_from_parents){
            completion_status|=this.props.completion_status_from_parents[node_id];
        }
        for(let node_id in this.state.completion_status_from_children){
            completion_status|=this.state.completion_status_from_children[node_id];
        }
        for(let node_id in this.state.completion_status_from_self){
            completion_status|=this.state.completion_status_from_self[node_id];
        }
        if(completion_status==0&&this.state.completion_status_from_children)completion_status=null;

        
        return(
            <div
            class={
                "outcome"+((data.is_dropped && " dropped")||"")
            }
            ref={this.maindiv}>
                <div class = "outcome-row">
                    <div class="outcome-head" style={{width:400-data.depth*44}}>
                        <div class="outcome-title">
                            <TitleText text={data.title} defaultText={"Click to edit"}/>
                        </div>
                        {children.length>0 && 
                            <div class="outcome-drop" onClick={this.toggleDrop.bind(this)}>
                                <div class = "outcome-drop-img">
                                    <img src={iconpath+dropIcon+".svg"}/>
                                </div>
                                <div class = "outcome-drop-text">
                                    {droptext}
                                </div>
                            </div>
                        }
                    </div>
                    <div class="outcome-cells">
                        {outcomeGroups}
                        <div class="table-cell blank-cell"></div>
                        <TableTotalCell grand_total={true} completion_status={completion_status} outcomes_type={this.props.outcomes_type}/>
                    </div>
                </div>
                <div class="children-block" id={this.props.objectID+"-children-block"} ref={this.children_block}>
                    {children}
                </div>
            </div>
            
        );
    }
    
    
    toggleDrop(){
        this.props.dispatch(changeField(this.props.objectID,this.objectType,"is_dropped",!this.props.data.is_dropped));
    }

    childUpdatedFunction(through_id,node_id,value){
        let index = this.props.data.child_outcome_links.indexOf(through_id);
        if(!this.child_completion_status[node_id]){
            if(value!==null){
                this.child_completion_status[node_id]=this.props.data.child_outcome_links.map((outcome_link)=>null);
            }else{
                return;
            }
        }
        if(this.child_completion_status[node_id][index]!==value){
            console.log("changing child completion status");
            this.child_completion_status[node_id][index]=value;
            this.updateCompletion(node_id);
        }
    }

    selfUpdatedFunction(node_id,value){
        if(this.state.completion_status_from_self[node_id]!=value){
            
            
            this.setState(function(state,props){
                let new_completion_status_from_self={...state.completion_status_from_self};
                new_completion_status_from_self[node_id]=value;
                return {completion_status_from_self:new_completion_status_from_self};
            });
        }
    }

    updateCompletion(node_id){
        console.log("updating completion");
        console.log(this.child_completion_status);
        let new_completion = this.child_completion_status[node_id].reduce((accumulator, current_value)=>{if(current_value===null && accumulator==null)return accumulator; else return accumulator & current_value;});
        console.log(new_completion);
        console.log(this.state.completion_status_from_children);
        if(this.state.completion_status_from_children[node_id]!==new_completion){
            console.log("setting state");
            this.setState(function(state,props){
                let new_completion_status_from_children = {...state.completion_status_from_children};
                new_completion_status_from_children[node_id]=new_completion;
                return {completion_status_from_children:new_completion_status_from_children}
            });
            
            if(this.props.updateParentCompletion)this.props.updateParentCompletion(node_id,new_completion);
        }
    }


}
export const TableOutcomeView = connect(
    mapOutcomeStateToProps,
    null
)(TableOutcomeViewUnconnected)