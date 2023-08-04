#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 14:32:49 2022

@author: akshay
"""
from dash import dcc,html,dash_table
import dash_bootstrap_components as dbc
from app import app
from dash.dependencies import Input, Output,State
import dash_uploader as du
import dash
from plots import *
from bokeh.palettes import all_palettes
du.configure_upload(app, 'uploads',use_upload_id=True)


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
uploadResult=dbc.Card([dbc.CardBody([
                    html.Div(dbc.Label("Area file",style={"font-weight": "bold","font-size": "15px"})),
                    du.Upload(
                        id='uploadResult',
                        text='Select a File!',
                        text_completed='Uploaded: ',
                        text_disabled='The uploader is disabled.',
                        cancel_button=True,
                        pause_button=False,
                        disabled=False,
                        filetypes=['csv'],
                        chunk_size=50,
                        max_file_size=10240,
                        default_style={'lineHeight': '1','minHeight': '1',},
                        upload_id=None,
                        max_files=1,),
                    
                    html.Hr(style={"background-color": "white"}),
                    
                    html.Div(dbc.Label("Metadata",style={"font-weight": "bold","font-size": "15px"})),
                   du.Upload(
                       id='uploadMeta',
                       text='Select a File!',
                       text_completed='Uploaded: ',
                       text_disabled='The uploader is disabled.',
                       cancel_button=True,
                       pause_button=False,
                       disabled=False,
                       filetypes=['csv'],
                       chunk_size=50,
                       max_file_size=10240,
                       default_style={'lineHeight': '1','minHeight': '1',},
                       upload_id=None,
                       max_files=1,),
                   
                   
                   
                    ])],className="mt-3",color="dark", outline=True) 

 

sideOptions=dbc.Card([dbc.CardBody([
                        dbc.Row([
                        
                            dbc.Col([html.Div(dbc.Label("Plot Type",style={"font-weight": "bold","font-size": "14px"})),
                            dcc.Dropdown(clearable=False,style={"font-size": "12px","color":"black"},
                            id="plotType",persistence=True,persistence_type="memory")]),
                            
                                                    
                            dbc.Col([html.Div(dbc.Label("Y-Axis",style={"font-weight": "bold","font-size": "14px"})),
                            dcc.Dropdown(options=[
                                {"label": "Area", "value": "area (in pixels)"},
                                {"label": "Intensity", "value": "intensity"},
                                {"label": "Circularity", "value": "circularity"},
                                {"label": "Realtive Area", "value": "relArea"},
                                {"label": "Contraction", "value": "contraction"}],value="area (in pixels)",clearable=False,style={"font-size": "12px","color":"black"},
                            id="yAxis",persistence=True,persistence_type="memory")]),
                            
                            dbc.Col([html.Div(dbc.Label("X-Axis",style={"font-weight": "bold","font-size": "14px"})),
                            dcc.Dropdown(clearable=False,style={"font-size": "12px","color":"black"},
                            id="xAxis",persistence=True,persistence_type="memory")]),
                            
                            dbc.Col([html.Div(dbc.Label("Color",style={"font-weight": "bold","font-size": "14px"})),
                            dcc.Dropdown(clearable=False,style={"font-size": "12px","color":"black"},
                            id="barPlotColor",persistence=True,persistence_type="memory")])
                       
                        ]),
                        
                        dbc.Row([
                                         
                            dbc.Col([html.Div(dbc.Label("X-axis Order",style={"font-weight": "bold","font-size": "14px","margin-top": "16px"})),
                            
                                dbc.Row([
                                    dcc.Dropdown(clearable=False, multi=True,style={"font-size": "12px","color":"black"},
                                                 id="xAxisOrder",persistence=True,persistence_type="memory"),
                                    
                                    html.Div(dbc.Button(html.I("  Update Order", className="fa fa-solid fa-refresh"), color="primary",id='updateOrder', className="me-1", 
                                             disabled=False,n_clicks=None,style={"font-size": "12px"}),className="d-grid gap-2 d-md-flex justify-content-md-end")
                                     
                                    ])
                            
                            ],width=3),
                            
                       
                        ])
                        

                        
                   ])],className="mt-3",color="dark", outline=True,style={"margin-right": "12px"})

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
sideOptions_scatterPlot=dbc.Card([dbc.CardBody([
                        dbc.Col([
                        
                            dbc.Row([html.Div(dbc.Label("Color Column",style={"font-weight": "bold","font-size": "14px"})),
                            dcc.Dropdown(clearable=False,style={"font-size": "12px","color":"black"},
                            id="colorSP",persistence=True,persistence_type="memory")]),
                            
                            dbc.Row([html.Div(dbc.Label("Facet Column",style={"font-weight": "bold","font-size": "14px"})),
                            dcc.Dropdown(clearable=False,style={"font-size": "12px","color":"black"},
                            id="colfacetSP",persistence=True,persistence_type="memory")]),
                            
                            dbc.Row([html.Div(dbc.Label("Facet Row",style={"font-weight": "bold","font-size": "14px"})),
                            dcc.Dropdown(clearable=False,style={"font-size": "12px","color":"black"},
                            id="colRowSP",persistence=True,persistence_type="memory")]),
                            
                       
                        ]),
                        
                   ])],className="mt-3",color="dark", outline=True,style={"margin-right": "12px"})


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
sideOptions_RelScatterPlot=dbc.Card([dbc.CardBody([
                        dbc.Col([
                     
                            
                            dbc.Row([html.Div(dbc.Label("Baseline",style={"font-weight": "bold","font-size": "14px"})),
                            dcc.Dropdown(clearable=False,style={"font-size": "12px","color":"black"},
                            id="baseline",persistence=True,persistence_type="memory")]),
                            
                            dbc.Row([html.Div(dbc.Label("Color Column",style={"font-weight": "bold","font-size": "14px"})),
                            dcc.Dropdown(clearable=False,style={"font-size": "12px","color":"black"},
                            id="colorSP_rel",persistence=True,persistence_type="memory")]),
                            
                            dbc.Row([html.Div(dbc.Label("Facet Column",style={"font-weight": "bold","font-size": "14px"})),
                            dcc.Dropdown(clearable=False,style={"font-size": "12px","color":"black"},
                            id="colfacetSP_rel",persistence=True,persistence_type="memory")]),
                            
                            dbc.Row([html.Div(dbc.Label("Facet Row",style={"font-weight": "bold","font-size": "14px"})),
                            dcc.Dropdown(clearable=False,style={"font-size": "12px","color":"black"},
                            id="colRowSP_rel",persistence=True,persistence_type="memory")]),
                            
                       
                        ]),
                        
                   ])],className="mt-3",color="dark", outline=True,style={"margin-right": "12px"})



import dash_loading_spinners as dls
sideOptionsHidden=html.Div(sideOptions,id="hidden9",style={'display': 'none'})

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
resultPanel=dbc.Card([dbc.CardBody([ 
                dbc.Col([dls.Hash(html.Div(id='uploadResult_plots',style={"margin-top": "12px"}),size=50,color="black"),
                                         dbc.Row(html.Div(id="hidden1")),                  
                                         dbc.Row(html.Div(id="hidden2")), 
                                         ])                
                ])],className="mt-3",color="dark", outline=True,style={"margin-right": "12px"}) 


uploadPanel=dbc.Col([                    
                    dbc.Row(dbc.Col(uploadResult)),
                    html.Div(dbc.Button(html.I("  Submit", className="fa fa-solid fa-play-circle-o"), color="primary",id='submitData', className="me-1", 
                                 style={"margin-top": "15px","font-weight": "bold","font-size": "18px"}),
                                 className="d-grid gap-2 d-md-flex justify-content-md-end",),
                    dbc.Row(html.Div(sideOptions,id="hidden6",style={'display': 'none'})),
                    dbc.Row(html.Div(sideOptions_scatterPlot,id="hidden7",style={'display': 'none'})),
                    dbc.Row(html.Div(sideOptions_RelScatterPlot,id="hidden17",style={'display': 'none'})),

                    dbc.Row(html.Div(id="hidden8")),
                    dbc.Row(html.Div(id="hidden18")),

                    
                    
                    html.Hr(style={"background-color": "white","width": "0px"}),
                    ],style={"margin-left": "12px"})


#style={'display': 'none'}
visualization=dbc.Card(
        dbc.Row([ 
                dbc.Col(uploadPanel,width=3),
                dbc.Col([dbc.Row(html.Div(id="hidden3")),
                         dbc.Row(html.Div(resultPanel))],width=9),
                html.Hr(style={"background-color": "white","width": "0px"}),
                    ])
        ,style={"margin-left": "5px","margin-right": "15px","margin-top": "10px"}) 

from datetime import datetime

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
uploadImg=dbc.Card([dbc.CardBody([
                    html.Div(dbc.Label("Upload Images",style={"font-weight": "bold","font-size": "15px"})),

                    du.Upload(
                        id='uploadImg',
                        text='Please select a .zip file (a compressed folder) of images!',
                        text_completed='Uploaded: ',
                        text_disabled='The uploader is disabled.',
                        cancel_button=True,
                        pause_button=False,
                        disabled=False,
                        filetypes=['zip'],
                        chunk_size=50,
                        max_file_size=10240,
                        default_style={'lineHeight': '1','minHeight': '1',},
                        upload_id=None,#datetime.now().strftime("%H_%M_%S"),
                        max_files=1,),
         
                    html.Hr(style={"background-color": "white"}),
                    html.Div(dbc.Label("Platform",style={"margin-top": "12px","font-weight": "bold","font-size": "15px"})),
                    dcc.Dropdown(options=[
                        {"label": "Incucyte", "value": "incucyte"},
                        {"label": "Microscope", "value": "other"},],value="incucyte",clearable=False,style={"font-size": "12px","color":"black"},
                    id="imageType",persistence=True,persistence_type="memory"),
                    
                    
                    html.Hr(style={"background-color": "white"}),
                    html.Div(dbc.Label("Prediction Threshold",style={"margin-top": "16px","font-weight": "bold","font-size": "15px"})),
                    dbc.Input(type="number",min=0,max=1,value=0.7,placeholder="range: 0 to 1.",id="Thre",persistence=True,persistence_type="memory"),
                    
                    html.Div(dbc.Button(html.I("  Predict", className="fa fa-solid fa-play-circle-o"), 
                                        disabled=True,color="primary",id='predBtnn', className="me-1", 
                                 style={"margin-top": "15px","font-weight": "bold","font-size": "18px"}),
                                 className="d-grid gap-2 d-md-flex justify-content-md-end",)
                   
                    ])],className="mt-3",color="dark", outline=True,style={"margin-left": "12px"}) 

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!   
downPredRes=dbc.Card([dbc.CardBody([ 
    dbc.Col([html.Label(html.Strong("Download Masked images and excel sheet with area and intensity values."),style={"text-align": "Justify"}),
                         html.Div(dbc.Button(html.I("  Download", className="fa fa-solid fa-download"), 
                                             color="success",id='downPredResBtnn', className="me-1", 
                                      style={"margin-top": "15px","font-weight": "bold","font-size": "18px"})),
                         dcc.Download(id="downloadMaskedImages"),
                         ])      
])],className="mt-3",color="dark", outline=True)      



 #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!   
pred=dbc.Card(
        dbc.Row([ 
                dbc.Col(uploadImg,width=3),
                dbc.Col(dls.Hash(html.Div(id='hidden5',style={"margin-top": "12px"}),size=100,color="black")),                
                html.Hr(style={"background-color": "white","width": "0px"}),
                    ])
        ,style={"margin-left": "5px","margin-right": "15px","margin-top": "10px"}) 




#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
import shutil
import os
@du.callback(
    Output("filepath_init", 'data'),
    id="uploadImg"
)
def getFilenames(filenames):                    
    #global filePath
    if filenames!=None:        
        try:                     
            filePath="/".join(filenames[0].split("/")[:-1])
            
            #del other files if user has selected more than one files and keep last one
            currentFile=filenames[0].split("/")[-1]
            
            filelist = [ f for f in os.listdir(filePath) if not f.startswith('.')]
            filelist.remove(currentFile)
            if len(filelist)>0:                 
                for f in filelist:
                    os.remove(os.getcwd()+"/"+filePath+ "/"+f)
            #time.sleep(3)


            return filePath
        except Exception as e:
            plot=html.Label([html.Strong("Following exception occurred  during area/image data read:"),html.Br(),str(e)],style={"text-align": "Justify"})
            return {}
        
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
@app.callback( 
    Output("predBtnn","disabled"),     
    [Input("filepath_init", 'data'),
    Input("filepath_data", 'data')]
     
)
def enablePredBtn(filepath_init,filepath_data): 

    if filepath_init==None:
        return True
    elif filepath_data!="":
        return True
    else:
        return False
    
         
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  
 

from prediction import predict
import zipfile
import time
from zipfile import ZipFile
 
@app.callback( 
    [Output("hidden5","children"),
    Output("filepath_data", 'data')],
    [Input("Thre","value"),
    Input("predBtnn","n_clicks"),
    Input("imageType", "value"),
    State("filepath_init", 'data')]
    
)
def predictMask(Thre,n_clicks,imageType,filePath):
   
    #return html.Label([html.Strong("This is a demonstration server and the prediction module is not available for use. To utilize the prediction functionality, please run SpheroScan on your local machine.")],style={"text-align": "Justify"}),None
    if filePath!={} and n_clicks:   
        try: 
            zippedFolder = [ f for f in os.listdir(filePath) if f.endswith('.zip')][0] 
            with zipfile.ZipFile(filePath+"/"+zippedFolder, 'r') as zip_ref:
                zip_ref.extractall(filePath)
            zip_ref.close()
            
            os.remove(filePath+"/"+zippedFolder)
            filePath=filePath+"/"+[ f for f in os.listdir(filePath) if not f.startswith(('.',"_"))][0]

            predict(filePath,Thre,imageType) 
            time.sleep(4)

            return  downPredRes,filePath
              
        except Exception as e:
            plot=html.Label([html.Strong("Following exception occurred  during prediction:"),html.Br(),str(e)],style={"text-align": "Justify"})
            return plot,None
    return "",""
   
        
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 

@app.callback(
    Output("downloadMaskedImages","data"),
    Input("downPredResBtnn","n_clicks"),
    [State("filepath_data", 'data')]
    
)
def downloadPred(n_clicks,filepath):
    if n_clicks:  
        filepath="/".join(filepath.split("/")[:-1])

        #del all folders from upload loc if there are too much
        filelist = [ f for f in os.listdir("./uploads/") if not f.startswith('.')]
        filelist.remove(filepath.split("/")[1])
        if len(filelist)>1: 
            for f in filelist:
            
                shutil.rmtree(os.getcwd()+"/uploads/"+ f)
               

                   
        return dcc.send_file(filepath+"/results.zip") 
    

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
area,meta,area_up={},{},{}
import pandas as pd
@du.callback(
    Output("hidden1","children"),

    id="uploadResult"
)
def readArea(filenames):
    if filenames!=None:
        global area
        
        try:
            area = pd.read_csv(filenames[0])
            return ""
        except Exception as e:
            plot=html.Label([html.Strong("Following exception occurred  during area/image data read:"),html.Br(),str(e)],style={"text-align": "Justify"})
            return plot
 
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
@du.callback(
   
    Output("hidden2", "children"),

    id="uploadMeta"
)
def readMeta(filenames):
    
    if filenames!=None:
        global meta
        
        try:
            meta = pd.read_csv(filenames[0])
            if len(list(meta.columns))<3:
                plot=html.Label([html.Strong("There is only one group column in the given metafile. At least two group columns should be provided. Adding the same group column twice (copy-pasting the same column) in your metafile is an option if there are no possible two groups."),html.Br(),html.Strong("Note: You will not be able to use the bar plot with statistics if you choose the second option.")],style={"text-align": "Justify"})
                return plot
            else:
                return ""
        except Exception as e:
            plot=html.Label([html.Strong("Following exception occurred  during  metadata read:"),html.Br(),str(e)],style={"text-align": "Justify"})
            return plot


  
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
import plotly.express as px

@app.callback(

    [Output("xAxisOrder", "options"),
     Output("updateOrder", "disabled"),
    ],
    [
     Input("plotType","value"),
     Input("xAxisOrder", "value"),
     Input("xAxis","value"),
     ]
) 
def changeAxisOrder(plotType,xAxisOrder,xAxis):
    if (plotType!="treemap" or plotType!="scatter")and isinstance(area_up, pd.DataFrame)==True:
        options_xAxis= [{'label': i, 'value': i} for i in list(set(area_up[xAxis].tolist()))]
        disabled=True 
        if xAxisOrder!=None and len(xAxisOrder)==len(options_xAxis):
            disabled=False
        
        return options_xAxis,disabled
    return [],False



#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
@app.callback(

    [Output("hidden8", "children"),
     Output("colorSP", "options"),
     Output("colfacetSP", "options"),
     Output("colRowSP", "options"),
     ],
    [Input("plotType","value"),
     Input("colorSP", "value"),
     Input("colfacetSP", "value"),
     Input("colRowSP", "value")]
     
) 
def spOptions(plotType,colorSP,colfacetSP,colRowSP):
    if plotType=="scatter" and isinstance(area_up, pd.DataFrame)==True:
        
        groups=list(area_up.columns)[6:] #change
        options= [{'label': i, 'value': i} for i in groups]+[{'label': "None", 'value': "None"}]
        if colorSP==[]:
            colorSP=groups[0]
        
        if colfacetSP==[]:
            colfacetSP=groups[0]
            
        if colRowSP==[]:
            colRowSP=groups[0]
       
        
        return [sideOptions_scatterPlot],options[:-1],options,options #,colRowSP
    return html.Div(sideOptions_scatterPlot,id="hidden7",style={'display': 'none'}),[],[],[]#,[],[],[]


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
@app.callback(

    [Output("hidden18", "children"),
     Output("colorSP_rel", "options"),
     Output("colfacetSP_rel", "options"),
     Output("colRowSP_rel", "options"),
     Output("baseline", "options"),
     Output("baseline", "value"),

     ],
    [Input("yAxis","value"),
     Input("colorSP_rel","value"),
     Input("colfacetSP_rel", "value"),
     Input("colRowSP_rel", "value"),
     Input("baseline", "options"),
     Input("baseline", "value")
]
     
) 
def spOptions_relArea(yAxis,colorSP,colfacetSP,colRowSP,baseline,baseline_value):
    if (yAxis=="relArea" or yAxis=="contraction")  and isinstance(area_up, pd.DataFrame)==True:
        
        groups=list(area_up.columns)[6:] #change
        options= [{'label': i, 'value': i} for i in groups]+[{'label': "None", 'value': "None"}]       

        #baseline options
        area_up_mean=pd.DataFrame(area_up.groupby(groups)['area (in pixels)'].mean())
        area_up_mean = pd.concat([area_up_mean, area_up_mean.index.to_frame(index=True)], axis = 1,ignore_index=True)

        baseline_list=[]
        for item in area_up_mean.index.tolist():
            temp=[]
            for groupName,groupType in zip(groups,item):
                temp.append(groupName+": "+groupType)
            baseline_list.append(' -- '.join(temp))
                     
        options_baseline= [{'label': i, 'value': i} for i in baseline_list] 

        
        if baseline_value==None:
            baseline_value=options_baseline[0].get('value')
            
        return [sideOptions_RelScatterPlot],options[:-1],options,options,options_baseline,baseline_value #,colRowSP
    return html.Div(sideOptions_RelScatterPlot,id="hidden17",style={'display': 'none'}),[],[],[],[],None#,[],[],[]



        
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
@app.callback(

    Output("uploadResult_plots", "children"), 
    Output("hidden3", "children"), 
    Output("xAxis","options"),
    Output("xAxis","value"),
    Output("barPlotColor", "options"),
    Output("barPlotColor", "value"),
    Output("plotType", "options"),
    Output("plotType", "value"),

    

    Input("submitData","n_clicks"),
    Input("plotType","value"),
    Input("yAxis","value"),
    Input("xAxis","value"),
    Input("barPlotColor","value"), 
    Input('updateOrder', 'n_clicks'),
    State("xAxisOrder", "value"),
    Input("colorSP", "value"),
    Input("colfacetSP", "value"),
    Input("colRowSP", "value"),
    
    Input("baseline", "value"),
    Input("colorSP_rel", "value"),
    Input("colfacetSP_rel", "value"),
    Input("colRowSP_rel", "value"),

) 
def readData(n_clicks,plotType,yAxis,xAxis,barPlotColor,updateOrder,xAxisOrder,colorSP,colfacetSP,colRowSP,
             baseline,colorSP_rel,colfacetSP_rel,colRowSP_rel):

    if n_clicks:
        if isinstance(meta, pd.DataFrame)==False:
            plot=html.Label([html.Strong("Please upload Metadata!")],style={"text-align": "Justify"})
            return plot,sideOptionsHidden,[],"",[],"",[],""
        
        elif isinstance(area, pd.DataFrame)==False:
            plot=html.Label([html.Strong("Please upload Area file!")],style={"text-align": "Justify"})
            return plot,sideOptionsHidden,[],"",[],"",[],""
        else:
            try:
                global area_up
                area_up=getCheckData(area,meta)
                if isinstance(area_up, pd.DataFrame)==False:
                    plot=html.Label([html.Strong("Following exception occurred:"),html.Br(),area_up],style={"text-align": "Justify"})
                    return plot,sideOptionsHidden,[],"",[],"",[],""
                else:
                    #set group drop down options
                    if xAxis not in list(meta.columns)[1:]:
                        xAxis=list(meta.columns)[1]
                        
                    options= [{'label': i, 'value': i} for i in list(meta.columns)[1:]]
                    
                    #set color pallete
                    if plotType=="treemap": 
                        bpV_options=list(px.colors.named_colorscales()) 
                        if barPlotColor not in bpV_options:
                            barPlotColor="matter"
                    else:
                        bpV_options=list(all_palettes.keys())
                        if barPlotColor not in bpV_options:
                            barPlotColor="Viridis" 
                            
                    #set plottype option
                    if yAxis=="relArea" or yAxis=="contraction":   
                        options_Plottype=[{"label": "Bubble Plot", "value": "bubblePlot"}]
                        value_Plottype="bubblePlot"
                        
                        #handle first time entry of plottype
                        plotType="bubblePlot"
                        
                    else:
                        options_Plottype=[
                            {"label": "Bar", "value": "bar"},
                            {"label": "Bar with statistics", "value": "statBar"},
                            {"label": "Treemap", "value": "treemap"},
                            {"label": "Lineplot", "value": "line"},
                            {"label": "Scatterplot", "value": "scatter"}]
                        
                        if plotType==None or plotType=="" or plotType=="bubblePlot":
                            value_Plottype="bar"
                            plotType="bar"
                        else:
                            value_Plottype=plotType
                    
                    #handle first enrty of scatter plot relative
                    if colorSP_rel==None or colorSP_rel==[]:
                        colorSP_rel=list(area_up.columns)[6]
                    
                    #handle first enrty of sp
                    if colorSP==None or colorSP==[]:
                        colorSP=list(area_up.columns)[6]
                                            
                    return getPlots(plotType,area_up,xAxis,yAxis,barPlotColor,updateOrder,
                                    xAxisOrder,colorSP,colfacetSP,colRowSP,
                                baseline,colorSP_rel,colfacetSP_rel,
                                    colRowSP_rel),sideOptions,options,xAxis,bpV_options,barPlotColor,options_Plottype,value_Plottype
            
            except Exception as e:
                plot=html.Label([html.Strong("Following exception occurred:"),html.Br(),str(e)],style={"text-align": "Justify"})
                return plot,sideOptionsHidden,[],"",[],"",[],""
    else:
        return "",sideOptionsHidden,[],"",[],"",[],""
            
