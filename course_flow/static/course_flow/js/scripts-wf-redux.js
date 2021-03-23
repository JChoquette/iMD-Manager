import {Component, createRef} from "react";
import * as reactDom from "react-dom";
import * as Redux from "redux";
import * as React from "react";
import {Provider, connect} from 'react-redux';
import {configureStore, createStore} from '@reduxjs/toolkit';
import {ComponentJSON} from "./ComponentJSON.js";
import WorkflowView from"./WorkflowView.js";
import {ProjectMenu, HomeMenu, ExploreMenu, renderMessageBox} from"./MenuComponents.js";
import {WorkflowView_Outcome} from"./WorkflowView.js";
import * as Constants from "./Constants.js";
import * as Reducers from "./Reducers.js";
import {WorkflowRenderer} from "./Renderers";

export {Loader} from './Constants';
export {fail_function} from './PostFunctions';

//Manages the current selection, ensuring we only have one at a time
export class SelectionManager{
    constructor(){
        this.currentSelection;
        this.mouse_isclick=false;
        var selector = this;
        $(document).on("mousedown",()=>{
            selector.mouse_isclick=true;
            setTimeout(()=>{selector.mouse_isclick=false;},500);
        });
        $(document).on("mousemove",()=>{
            selector.mouse_isclick=false;
        });
        $(document).on("mouseup",(evt,newSelection)=>{
            if(selector.mouse_isclick){
                selector.changeSelection(evt,null);
            }
        });
        this.last_sidebar_tab = $("#sidebar").tabs( "option", "active");
    }
    
    changeSelection(evt,newSelection){
        if(read_only)return;
        evt.stopPropagation();
        if(this.currentSelection)this.currentSelection.setState({selected:false});
        this.currentSelection=newSelection;
        if(this.currentSelection){
            if($("#sidebar").tabs("option","active")!==0)this.last_sidebar_tab = $("#sidebar").tabs( "option", "active");
            $("#sidebar").tabs("enable",0);
            $("#sidebar").tabs( "option", "active", 0 );
            this.currentSelection.setState({selected:true});
        }else{
            if($("#sidebar").tabs( "option", "active" )===0)$("#sidebar").tabs( "option", "active", this.last_sidebar_tab );
            $("#sidebar").tabs("disable",0);
        }
    }
}





var store;



export function renderWorkflowView(container,data_package,outcome_view){
    var workflow_renderer = new WorkflowRenderer(data_package);
    workflow_renderer.render(container,outcome_view);
}


export function renderHomeMenu(data_package){
    if(!store)store = createStore(Reducers.homeMenuReducer,data_package);
    reactDom.render(
        <Provider store = {store}>
            <HomeMenu/>
        </Provider>,
        $("#content-container")[0]
    );
}

export function renderExploreMenu(data_package,disciplines){
    reactDom.render(
        <ExploreMenu data_package={data_package} disciplines={disciplines} pages={pages}/>,
        $("#content-container")[0]
    );
}



export function renderProjectMenu(data_package,project){
    if(!store)store = createStore(Reducers.projectMenuReducer,data_package);
    reactDom.render(
        <Provider store = {store}>
            <ProjectMenu project={project}/>
        </Provider>,
        $("#content-container")[0]
    );
}

export class TinyLoader{
    constructor(identifier){
        this.identifier = identifier; 
        this.loadings = 0;
    }
    
    startLoad(){
        $(this.identifier).addClass('waiting');
        this.loadings++;
    }
        
    endLoad(){
        if(this.loadings>0)this.loadings--;
        if(this.loadings<=0)$(this.identifier).removeClass('waiting');
    }
}

