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
            <OutcomeOutcomeView key={outcomeoutcome} objectID={outcomeoutcome} parentID={data.id} renderer={this.props.renderer} />
        );
        
        let actions=[];
        if(!read_only && data.depth<2)actions.push(this.addInsertChild(data));
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
            onClick={(evt)=>this.props.renderer.selection_manager.changeSelection(evt,this)}>
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
                <ol class="children-block" id={this.props.objectID+"-children-block"} ref={this.children_block}>
                    {children}
                </ol>
                {(!read_only && data.depth < 2) && <div class="outcome-create-child" onClick = {this.insertChild.bind(this,data)}>+ Add New</div>
                }
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
        this.state={is_dropped:(props.data.depth<1)};
    }
    
    render(){
        let data = this.props.data;
        
        var children = data.child_outcome_links.map((outcomeoutcome)=>
            <OutcomeBarOutcomeOutcomeView key={outcomeoutcome} objectID={outcomeoutcome} parentID={data.id} renderer={this.props.renderer}/>
        );
                
        let dropIcon;
        if(this.state.is_dropped)dropIcon = "droptriangleup";
        else dropIcon = "droptriangledown";
        
        let droptext;
        if(this.state.is_dropped)droptext="hide";
        else droptext = "show "+children.length+" descendant"+((children.length>1&&"s")||"")
        
        return(
            <div
            class={
                "outcome"+((this.state.is_dropped && " dropped")||"")+" outcome-"+data.id
            }
            
            ref={this.maindiv}>
                <div class="outcome-title" >
                    <TitleText text={data.title} defaultText={"Click to edit"}/>
                </div>
                <input class="outcome-toggle-checkbox" type="checkbox" title="Toggle highlighting" onChange={this.clickFunction.bind(this)}/>
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
       
        this.setState({is_dropped:(!this.state.is_dropped)});
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

    clickFunction(evt){
        if(evt.target.checked){
            this.toggleCSS(true,"toggle");
        }else{
            this.toggleCSS(false,"toggle");
        }
    }

    toggleCSS(is_toggled,type){
        if(is_toggled){
            $(".outcome-"+this.props.data.id).addClass("outcome-"+type);
            $(".outcome-"+this.props.data.id).parents(".node").addClass("outcome-"+type);
        }else{
            $(".outcome-"+this.props.data.id).removeClass("outcome-"+type);
            $(".outcome-"+this.props.data.id).parents(".node").removeClass("outcome-"+type);
        }
    }
    
    postMountFunction(){
        this.makeDraggable();
        $(this.maindiv.current)[0].dataDraggable={outcome:this.props.data.id}
        $(this.maindiv.current).mouseenter((evt)=>{
            this.toggleCSS(true,"hover");
        });
        $(this.maindiv.current).mouseleave((evt)=>{
            this.toggleCSS(false,"hover");
        });
        $(this.children_block.current).mouseleave((evt)=>{
            this.toggleCSS(true,"hover");
        });
        $(this.children_block.current).mouseenter((evt)=>{
            this.toggleCSS(false,"hover");
        });
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
        this.state={is_dropped:false};
    }
    
    render(){
        let data = this.props.data;
        
        var children = data.child_outcome_links.map((outcomeoutcome)=>
            <NodeOutcomeOutcomeView key={outcomeoutcome} objectID={outcomeoutcome} parentID={data.id} renderer={this.props.renderer}/>
        );
                
        let dropIcon;
        if(this.state.is_dropped)dropIcon = "droptriangleup";
        else dropIcon = "droptriangledown";
        
        let droptext;
        if(this.state.is_dropped)droptext="hide";
        else droptext = "show "+children.length+" descendant"+((children.length>1&&"s")||"")
        
        return(
            <div
            class={
                "outcome"+((this.state.is_dropped && " dropped")||"")+" outcome-"+data.id
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
        this.setState({is_dropped:(!this.state.is_dropped)});
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
            <TableOutcomeOutcomeView renderer={this.props.renderer} key={outcomeoutcome} objectID={outcomeoutcome} parentID={data.id} nodecategory={this.props.nodecategory} updateParentCompletion={this.childUpdatedFunction.bind(this,outcomeoutcome)} completion_status_from_parents={completion_status_to_pass} outcomes_type={this.props.outcomes_type}/>
        );

        let outcomeGroups = this.props.nodecategory.map((nodecategory)=>
            <TableOutcomeGroup renderer={this.props.renderer} nodes={nodecategory.nodes} outcomeID={this.props.data.id} updateParentCompletion={this.props.updateParentCompletion} updateSelfCompletion={this.selfUpdatedFunction.bind(this)} completion_status_from_children={this.child_completion_status} completion_status_from_parents={this.props.completion_status_from_parents} completion_status_from_self = {this.state.completion_status_from_self} outcomes_type={this.props.outcomes_type}/>
                                                        
                                                         
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
        console.log("Calculating the total completion");
        console.log(this.props.outcomeID);
        console.log(this.props.child_completion_status);
        let childnodes=0;
        let sub_outcomes_completion;
        for(let node_id in this.child_completion_status){
            if(sub_outcomes_completion==null)sub_outcomes_completion = this.child_completion_status[node_id].slice();
            else for(let i=0;i<this.child_completion_status[node_id].length;i++){
                sub_outcomes_completion[i]|=this.child_completion_status[node_id][i];
            }
            if(this.child_completion_status[node_id].reduce((accumulator, current_value)=>{if(current_value===null && accumulator==null)return accumulator; else return accumulator & current_value;})!==null)childnodes++;
        }
        if(sub_outcomes_completion)completion_status|=sub_outcomes_completion.reduce((accumulator, current_value)=>{if(current_value===null && accumulator==null)return accumulator; else return accumulator & current_value;});
        for(let node_id in this.state.completion_status_from_self){
            completion_status|=this.state.completion_status_from_self[node_id];
        }
        if(completion_status==0&&childnodes==0)completion_status=null;

        
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
        console.log("A child has been updated");
        console.log(node_id);
        console.log(value);
        let index = this.props.data.child_outcome_links.indexOf(through_id);
        if(!this.child_completion_status[node_id]){
            if(value!==null){
                this.child_completion_status[node_id]=this.props.data.child_outcome_links.map((outcome_link)=>null);
            }else{
                return;
            }
        }
        if(this.child_completion_status[node_id][index]!==value){
            this.child_completion_status[node_id][index]=value;
            console.log("calling update completion with node "+node_id+" at index "+index+" and value "+value);
            console.log(this.child_completion_status);
            this.updateCompletion(node_id);
        }
    }

    selfUpdatedFunction(node_id,value){
        console.log("received a node update");
        console.log(node_id);
        console.log(value);
        if(this.state.completion_status_from_self[node_id]!=value){
            
            
            this.setState(function(state,props){
                let new_completion_status_from_self={...state.completion_status_from_self};
                new_completion_status_from_self[node_id]=value;
                return {completion_status_from_self:new_completion_status_from_self};
            });
        }
    }

    updateCompletion(node_id){
        let new_child_completion = this.child_completion_status[node_id].reduce((accumulator, current_value)=>{if(current_value===null && accumulator==null)return accumulator; else return accumulator & current_value;});
        console.log("updating completion");
        console.log(node_id);
        console.log(new_child_completion);
        if(this.state.completion_status_from_children[node_id]!==new_child_completion){
            this.setState(function(state,props){
                let new_completion_status_from_children = {...state.completion_status_from_children};
                new_completion_status_from_children[node_id]=new_child_completion;
                return {completion_status_from_children:new_completion_status_from_children}
            });
            if(this.props.updateParentCompletion){
                let self_completion = this.state.completion_status_from_self[node_id];
                if(!self_completion && new_child_completion ===null )
                    this.props.updateParentCompletion(node_id,null);
                else 
                    this.props.updateParentCompletion(node_id,new_child_completion|this.state.completion_status_from_self[node_id]);
            }
        }
    }


}
export const TableOutcomeView = connect(
    mapOutcomeStateToProps,
    null
)(TableOutcomeViewUnconnected)