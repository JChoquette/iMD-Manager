import * as React from "react";
import {Provider, connect} from "react-redux";
import {ComponentJSON} from "./ComponentJSON.js";
import WeekView from "./WeekView.js";
import TermView from "./TermView.js";
import {getWeekWorkflowByID} from "./FindState.js";
import {} from "./Reducers.js";

//Basic weekworkflow component
class WeekWorkflowView extends ComponentJSON{
    constructor(props){
        super(props);
        this.objectType="weekworkflow";
        this.objectClass=".week-workflow";
    }
    
    render(){
        let data = this.props.data;
        var week;
        if(data.week_type==2)week = (
                <TermView objectID={data.week} rank={this.props.order.indexOf(data.id)} parentID={this.props.parentID} throughParentID={data.id} renderer={this.props.renderer}/>
        );
        else week = (
            <WeekView objectID={data.week} rank={this.props.order.indexOf(data.id)} parentID={this.props.parentID} throughParentID={data.id} renderer={this.props.renderer}/>
        );
        return (
            <div class="week-workflow" id={data.id} ref={this.maindiv} data-child-id={data.week}>
                {week}
            </div>
        );
    }
}
const mapWeekWorkflowStateToProps = (state,own_props)=>(
    getWeekWorkflowByID(state,own_props.objectID)
)
const mapWeekWorkflowDispatchToProps = {};
export default connect(
    mapWeekWorkflowStateToProps,
    null
)(WeekWorkflowView)


class NodeBarWeekWorkflowUnconnected extends ComponentJSON{
    render(){
        let data = this.props.data;
        return null;
    }
}
export const NodeBarWeekWorkflow = connect(
    mapWeekWorkflowStateToProps,
    null
)(NodeBarWeekWorkflowUnconnected)