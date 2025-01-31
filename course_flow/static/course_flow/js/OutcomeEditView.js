import * as React from "react";
import * as reactDom from "react-dom";
import {Provider, connect} from "react-redux";
import {EditableComponentWithSorting, OutcomeTitle} from "./ComponentJSON";
import OutcomeWorkflowView from "./OutcomeWorkflowView";
import {OutcomeBarOutcomeView, OutcomeBarOutcomeViewUnconnected} from "./OutcomeView";
import OutcomeView from "./OutcomeView";
import {getParentWorkflowByID,getOutcomeNodeByID, getOutcomeByID, getOutcomeOutcomeByID, getSortedOutcomesFromOutcomeWorkflowSet,getSortedOutcomeNodesFromNodes} from "./FindState";
import {moveOutcomeWorkflow} from "./Reducers";
import {renderMessageBox, closeMessageBox} from './MenuComponents';
import {newOutcome, insertedAt} from "./PostFunctions";
import * as Constants from "./Constants";

//Basic component representing the outcome view
export class OutcomeEditViewUnconnected extends EditableComponentWithSorting{
    
    constructor(props){
        super(props);
        this.objectType="workflow";
    }
    
    render(){
        let data = this.props.data;
        var selector = this;
        let outcomes = data.map(category=>
            <div class="outcome-category">
                <h4>{category.objectset.title+":"}</h4>
                <div class="outcome-category-block">
                    {category.outcomes.map(outcome=>{
                        let my_class = "outcome-workflow";
                        if(outcome.through_no_drag)my_class+=" no-drag";
                        return (<div class={my_class} data-child-id={outcome.id} id={outcome.outcomeworkflow} key={outcome.outcomeworkflow}>
                            <OutcomeView key={outcome.id} objectID={outcome.id} parentID={this.props.workflow.id} renderer={this.props.renderer} show_horizontal={true}/>
                        </div>);
                    })}
                    {this.getAddNew(category.objectset)}
                </div>
            </div>
        );
        if(outcomes.length==0)outcomes=(
            [<div class="emptytext">{gettext("Here you can add and edit outcomes for the current workflow. They will then be available in the Workflow view to tag nodes in the Outcomes tab of the sidebar.")}</div>,
            this.getAddNew({})]
        );
        
        return(
            <div id={"#workflow-"+this.props.workflow.id} class="workflow-details">
                <div class="outcome-edit" ref={this.maindiv}>
                    {outcomes}
                    {this.getParentOutcomeBar()}
                </div>
            </div>
        );
    }

    getAddNew(objectset){
        let add_new_outcome;
        if(!this.props.renderer.read_only)add_new_outcome=(
            <div id="add-new-outcome" class="menu-create hover-shade" onClick={this.addNew.bind(this,objectset)}>
                <img class="create-button" src={iconpath+"add_new_white.svg"}/>
                <div>{gettext("Add new")}</div>
            </div>
        );
        return add_new_outcome;
    }

    getParentOutcomeBar(){
        return <ParentOutcomeBar renderer={this.props.renderer}/>
    }

    componentDidMount(){
        this.makeDragAndDrop();
    }
    componentDidUpdate(){
        this.makeDragAndDrop();
    }
    stopSortFunction(){
        
    }
    makeDragAndDrop(){
        this.makeSortableNode($(this.maindiv.current).find(".outcome-workflow").not("ui-draggable"),this.props.objectID,"outcomeworkflow",".outcome-workflow");
        if(this.props.data.depth==0)this.makeDroppable();
    }
    
    sortableMovedFunction(id,new_position,type,new_parent,child_id){
        this.props.renderer.micro_update(moveOutcomeWorkflow(id,new_position,this.props.workflow.id,child_id));
        insertedAt(this.props.renderer,child_id,"outcome",this.props.workflow.id,"workflow",new_position,"outcomeworkflow");
    }
    
    addNew(objectset){
        newOutcome(this.props.workflow.id,objectset.id);
    }
    
}
const mapEditViewStateToProps = state=>({
    data:getSortedOutcomesFromOutcomeWorkflowSet(state,state.workflow.outcomeworkflow_set),
    workflow:state.workflow
})
export default connect(
    mapEditViewStateToProps,
    null
)(OutcomeEditViewUnconnected)


class ParentOutcomeNodeViewUnconnected extends React.Component{
    render(){
        let data = this.props.data;
        
        return(
            <div class="parent-outcome-node">
                {this.getContents(data.degree)}
                <ParentOutcomeView objectID={data.outcome} renderer={this.props.renderer}/>
            </div>
        )
        
    }
    
    getContents(completion_status){
        if(this.props.outcomes_type==0 || completion_status & 1){
            return (
                <img class="self-completed" src={iconpath+'solid_check.svg'}/>
            )
        }
        let contents=[];
        if(completion_status & 2){
            let divclass="";
            contents.push(
                <div class={"outcome-introduced outcome-degree"+divclass}>I</div>
            );
        }
        if(completion_status & 4){
            let divclass="";
            contents.push(
                <div class={"outcome-developed outcome-degree"+divclass}>D</div>
            );
        }
        if(completion_status & 8){
            let divclass="";
            contents.push(
                <div class={"outcome-advanced outcome-degree"+divclass}>A</div>
            );
        }
        return contents;
        
    }
}
const mapParentOutcomeNodeStateToProps = (state,own_props)=>(
    getOutcomeNodeByID(state,own_props.objectID)
)
export const ParentOutcomeNodeView = connect(
    mapParentOutcomeNodeStateToProps,
    null
)(ParentOutcomeNodeViewUnconnected)


class ParentOutcomeViewUnconnected extends OutcomeBarOutcomeViewUnconnected{
    render(){
        let data = this.props.data;
        let children = data.child_outcome_links.map((outcomeoutcome)=>
            <ParentOutcomeOutcomeView key={outcomeoutcome} objectID={outcomeoutcome} parentID={data.id} renderer={this.props.renderer} />
        );
                
        let dropIcon;
        if(this.state.is_dropped)dropIcon = "droptriangleup";
        else dropIcon = "droptriangledown";
        
        let droptext;
        if(this.state.is_dropped)droptext=gettext("hide");
        else droptext = gettext("show ")+children.length+" "+ngettext("descendant","descendants",children.length);
        
        
        return(
            <div
            class={
                "outcome"+((this.state.is_dropped && " dropped")||"")+" outcome-"+data.id
            }
            
            ref={this.maindiv}>
                <div class="outcome-title">
                    <OutcomeTitle data={this.props.data} prefix={this.props.prefix} hovertext={this.props.hovertext}/>
                </div>
                <input class="outcome-toggle-checkbox" type="checkbox" title="Toggle highlighting" onChange={this.clickFunction.bind(this)}/>
                {data.depth < 2 && data.child_outcome_links.length>0 && 
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
        )
    }
    
    
}
const mapOutcomeBarOutcomeStateToProps = (state,own_props)=>(
    {
        ...getOutcomeByID(state,own_props.objectID),
        nodes:state.outcomenode.filter(outcomenode=>outcomenode.outcome==own_props.objectID).map((outcomenode)=>outcomenode.node),
        horizontaloutcomes:state.outcomehorizontallink.filter(ochl=>ochl.parent_outcome==own_props.objectID).map((ochl)=>ochl.outcome)
    }
)
export const ParentOutcomeView = connect(
    mapOutcomeBarOutcomeStateToProps,
    null
)(ParentOutcomeViewUnconnected)

class ParentOutcomeOutcomeViewUnconnected extends React.Component{
    render(){
        let data = this.props.data;
        
        return (
            <div class="outcome-outcome" id={data.id} ref={this.maindiv}>
                <ParentOutcomeView objectID={data.child} parentID={this.props.parentID} throughParentID={data.id} renderer={this.props.renderer}/>
            </div>
        );
    }
}
const mapParentOutcomeOutcomeStateToProps = (state,own_props)=>(
    getOutcomeOutcomeByID(state,own_props.objectID,"parent")
)
export const ParentOutcomeOutcomeView = connect(
    mapParentOutcomeOutcomeStateToProps,
    null
)(ParentOutcomeOutcomeViewUnconnected)





class OutcomeBarUnconnected extends React.Component{
    render(){
        let data = this.props.data;
        var outcomebaroutcomes = data.map((category)=>[
            <hr/>,
            <div>
                <h4>{category.objectset.title}</h4>
                {category.outcomes.map(outcome=>
                    <OutcomeBarOutcomeView key={outcome.id} objectID={outcome.id} renderer={this.props.renderer}/>
                )}
            </div>
            ]
        );
        
        if(outcomebaroutcomes.length==0){
            outcomebaroutcomes=gettext("Add outcomes to this workflow in by clicking the button below.");
        }
        let edittext=Constants.capWords(gettext("Edit")+" "+gettext(this.props.workflow_type+" outcomes"));
        return reactDom.createPortal(
            <div id="outcome-bar-workflow" class="right-panel-inner">
                <h3 class="drag-and-drop">{gettext("Outcomes")}</h3>
                <div class="outcome-bar-outcome-block">
                    {outcomebaroutcomes}
                </div>
                {!this.props.renderer.read_only &&
                    <button class="primary-button" id="edit-outcomes-button" onClick={this.editOutcomesClick.bind(this)}>{edittext}</button>
                }
                <hr/>
            </div>
        ,$("#outcome-bar")[0]);
    }
    
    editOutcomesClick(){
        this.props.renderer.render($("#container"),"outcomeedit");
    }
    
}
const mapOutcomeBarStateToProps = state =>(
    {data:getSortedOutcomesFromOutcomeWorkflowSet(state,state.workflow.outcomeworkflow_set),workflow_type:state.workflow.type}
)
export const OutcomeBar = connect(
    mapOutcomeBarStateToProps,
    null
)(OutcomeBarUnconnected)


class ParentOutcomeBarUnconnected extends React.Component{
    render(){
        let data = this.props.data;
        var outcomebaroutcomes = data.map((category)=>
            [<hr/>,
            <div>
                <h4>{category.objectset.title}</h4>
                {category.outcomes.map(outcome=>
                    <div class="parent-outcome-node">
                        {Constants.getCompletionImg(outcome.degree,1)}
                        <ParentOutcomeView key={outcome.id} objectID={outcome.id} renderer={this.props.renderer}/>
                    </div>
                )}
            </div>]
        );
        
        
        if(outcomebaroutcomes.length==0){
            outcomebaroutcomes=gettext("Here you can find outcomes from the workflows that contain a node linked to this workflow. This allows you to create relationships between the outcomes at different levels (ex. program to course), called 'alignment'. Link this workflow to a node in another to do so.");
        }

        let multiple_parent_warning;
        if(this.props.parent_nodes.length>1){
            multiple_parent_warning = <div><span class="material-symbols-rounded filled small-inline red">error</span>{gettext("Warning: you have linked this workflow to multiple nodes. This is not recommended. You may see outcomes from different parent workflows, or duplicates of outcomes.")}</div>
        }
        
        return reactDom.createPortal(
            <div id="outcome-bar-workflow" class="right-panel-inner">
                <h3 class="drag-and-drop">{gettext("Outcomes from Parent Workflow")}</h3>
                <div class="outcome-bar-outcome-block">
                    {multiple_parent_warning}
                    {outcomebaroutcomes}
                </div>
            </div>
        ,$("#outcome-bar")[0]);
    }
    
}
const mapParentOutcomeBarStateToProps = state =>{
    return {data:getSortedOutcomeNodesFromNodes(state,state.parent_node),workflow:state.workflow,parent_nodes:state.parent_node}
}
export const ParentOutcomeBar = connect(
    mapParentOutcomeBarStateToProps,
    null
)(ParentOutcomeBarUnconnected)