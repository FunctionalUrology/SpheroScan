#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 16:43:35 2022

@author: akshay
"""

import pandas as pd
import numpy as np
import scipy
from scipy import stats
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#from stack overflow
def add_p_value_annotation(fig, array_columns, subplot=None, _format=dict(interline=0.07, text_height=1.07, color='black')):
    # Specify in what y_range to plot for each pair of columns
    y_range = np.zeros([len(array_columns), 2])
    for i in range(len(array_columns)):
        y_range[i] = [1.01+i*_format['interline'], 1.02+i*_format['interline']]

    # Get values from figure
    fig_dict = fig.to_dict()

    # Get indices if working with subplots
    if subplot:
        if subplot == 1:
            subplot_str = ''
        else:
            subplot_str =str(subplot)
        indices = [] #Change the box index to the indices of the data for that subplot
        for index, data in enumerate(fig_dict['data']):
            #print(index, data['xaxis'], 'x' + subplot_str)
            if data['xaxis'] == 'x' + subplot_str:
                indices = np.append(indices, index)
        indices = [int(i) for i in indices]
        
        
    else:
        subplot_str = ''

    # Print the p-values
    for index, column_pair in enumerate(array_columns):
        if subplot:
            data_pair = [indices[column_pair[0]], indices[column_pair[1]]]
        else:
            data_pair = column_pair

        # Mare sure it is selecting the data and subplot you want
        #print('0:', fig_dict['data'][data_pair[0]]['name'], fig_dict['data'][data_pair[0]]['xaxis'])
        #print('1:', fig_dict['data'][data_pair[1]]['name'], fig_dict['data'][data_pair[1]]['xaxis'])

        # Get the p-value
        pvalue = stats.ttest_ind(
            fig_dict['data'][data_pair[0]]['y'],
            fig_dict['data'][data_pair[1]]['y'],
            equal_var=False,
        )[1]
        if pvalue >= 0.05:
            symbol = 'ns'
        elif pvalue >= 0.01: 
            symbol = '*'
        elif pvalue >= 0.001:
            symbol = '**'
        else:
            symbol = '***'
        # Vertical line
        fig.add_shape(type="line",
            xref="x"+subplot_str, yref="y"+subplot_str+" domain",
            x0=column_pair[0], y0=y_range[index][0], 
            x1=column_pair[0], y1=y_range[index][1],
            line=dict(color=_format['color'], width=2,)
        )
        # Horizontal line
        fig.add_shape(type="line",
            xref="x"+subplot_str, yref="y"+subplot_str+" domain",
            x0=column_pair[0], y0=y_range[index][1], 
            x1=column_pair[1], y1=y_range[index][1],
            line=dict(color=_format['color'], width=2,)
        )
        # Vertical line
        fig.add_shape(type="line",
            xref="x"+subplot_str, yref="y"+subplot_str+" domain",
            x0=column_pair[1], y0=y_range[index][0], 
            x1=column_pair[1], y1=y_range[index][1],
            line=dict(color=_format['color'], width=2,)
        )
        ## add text at the correct x, y coordinates
        ## for bars, there is a direct mapping from the bar number to 0, 1, 2...
        fig.add_annotation(dict(font=dict(color=_format['color'],size=12),
            x=(column_pair[0] + column_pair[1])/2,
            y=y_range[index][1],#*_format['text_height'],
            showarrow=False,
            text=symbol,
            textangle=0,
            xref="x"+subplot_str,
            yref="y"+subplot_str+" domain"
        ))
    return fig

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def getCheckData(area,meta):
    if meta.isnull().values.any():
        return "Metadata has NA values. Pleas recheck!"
        
    if area.isnull().values.any():
        return "Area has NA values. Pleas recheck!"
        
    fileNameCheck=area['filename'].apply(lambda x: any([k in x for k in meta['filename'].tolist()]))

    if np.all(fileNameCheck):
        print("")
    else:
        
        return "Following filenames are missing in metadat file: "+' '.join(str(e) for e in list(area.loc[np.where(fileNameCheck==False),"filename"]))
    
    #append meta info with area file
    grouptypes=list(meta.columns)[1:]
    
    temp=[]
    
    for item in area['filename'].tolist():
        temp.append(meta.loc[meta['filename']==item,grouptypes].values.flatten().tolist()[:len(grouptypes)])
        #group.append(str(temp[0]))
        #subgroup.append(str(temp[1]))
    
    #area['group']=group
    #area['subgroup']=subgroup
    area_up = pd.concat([area,  pd.DataFrame(temp,columns=grouptypes).astype(str)], axis=1)
    
    
    return area_up



import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
from itertools import combinations
from plotly.subplots import make_subplots
from bokeh.palettes import all_palettes
from dash import dcc,html

pio.renderers.default = 'browser'

config={'displaylogo': False,
           'toImageButtonOptions': {'format': 'png','scale':5}}

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def getBarPlot(area,xAxis,yAxis,pal,color,xAxisOrder):

      
    grouptypes=list(area.columns)[5:]
    
    area_melt=pd.melt(area, id_vars=grouptypes, value_vars=[yAxis],var_name='filename', value_name=yAxis)

    #get colors from pal
    groupColorPal=all_palettes[pal]
            #if no of model is larger than the second largest available color list of corr pallete, use last list that is longest one.
    models=set(area_melt[color])
    if len(groupColorPal)<len(models):
        groupColor=groupColorPal[list(groupColorPal.keys())[-1]]
    else:
        #else choose the one with no of color equal to no of models
        if len(models)<3:
            groupColor=groupColorPal[3]
        else:
            groupColor=groupColorPal[len(models)]
            
    fig = px.box(area_melt, x=xAxis, y=yAxis, color=color,  
                 color_discrete_sequence=groupColor, 
                 category_orders={color: sorted(models)}
                 )
    
    fig.update_traces(quartilemethod="inclusive") # or "inclusive", or "linear" by default
    fig.update_layout(font=dict(family="Times New Roman",size=14,),
                      dragmode='drawopenpath',
                         newshape_line_color='#B32900',template="plotly_white",
                         modebar_add=['drawline','drawopenpath','drawclosedpath','drawcircle','drawrect', 'eraseshape'],
                        )
    
    fig.update_xaxes(categoryorder='array', categoryarray= xAxisOrder)


    #fig.show()
    return dcc.Graph(figure=fig,config=config)
    


 #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!   
def getBarPlotStat(area,xAxis,yAxis,group,pal,color,xAxisOrder):
    grouptypes=list(area.columns)[5:]
    
    area_melt=pd.melt(area, id_vars=grouptypes, value_vars=[yAxis],var_name='filename', value_name=yAxis)
    area_melt_sub=area_melt.loc[area_melt[xAxis].apply(str)==group]
    
    #get colors from pal
    groupColorPal=all_palettes[pal]
            #if no of model is larger than the second largest available color list of corr pallete, use last list that is longest one.
    models=set(area_melt_sub[color])
    if len(groupColorPal)<len(models):
        groupColor=groupColorPal[list(groupColorPal.keys())[-1]]
    else:
        #else choose the one with no of color equal to no of models
        if len(models)<3:
            groupColor=groupColorPal[3]
        else:
            groupColor=groupColorPal[len(models)]
            
    
    #draw figure
    fig = px.box(area_melt_sub, x=color, y=yAxis, color=color,color_discrete_sequence=groupColor, 
                 
                 category_orders={color: sorted(models)},
                 title="<b>"+xAxis.upper()+": "+group+"</b>")
    fig.update_traces(quartilemethod="inclusive") # or "inclusive", or "linear" by default
    
    #stat anno
    totalGroups=list(range(len(set(area_melt_sub[color].tolist()))))
    statAnno=list(combinations(totalGroups, 2))
    
    fig = add_p_value_annotation(fig, statAnno)
    fig.update_layout(  font=dict(family="Times New Roman",size=14,),
                        dragmode='drawopenpath',showlegend=False,
                         newshape_line_color='#B32900',template="plotly_white",
                         modebar_add=['drawline','drawopenpath','drawclosedpath','drawcircle','drawrect', 'eraseshape'],
                         margin=dict(t=len(totalGroups)*40, b=20))
    
    fig.update_xaxes(categoryorder='array', categoryarray= xAxisOrder)

    
    #fig.show()
    return dcc.Graph(figure=fig,config=config)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def getLinePlot(area_up,xAxis,yAxis,barPlotColor,xAxisOrder):
    groups=list(area_up.columns)[5:]
    groups.remove(xAxis)
    
    #xLabel=list(set(area_up[xAxis].tolist()))
    xLabel=xAxisOrder
    meanValues={}
    for item in xLabel:
        

        fig = go.Figure()
        for subgroups in groups:
            for subgroups_types in list(set(area_up[subgroups].tolist())):
                temp=area_up.loc[(area_up[xAxis].apply(str)==item) & (area_up[subgroups].apply(str)==subgroups_types)]
                
                key=subgroups+":"+subgroups_types
                if key not in meanValues.keys():
                    meanValues[key]=[temp[yAxis].mean()]
                else:
                   meanValues[key].append(temp[yAxis].mean()) 
                

                
            
    fig = go.Figure()
    temp=""
    dashes=[None,'dash',  'dashdot','dot']
    dc=0
    cc=0
    #get colors from pal
    groupColorPal=all_palettes[barPlotColor]
            #if no of model is larger than the second largest available color list of corr pallete, use last list that is longest one.
    models=list(meanValues.keys())


    if len(groupColorPal)<len(models):
        groupColor=groupColorPal[list(groupColorPal.keys())[-1]]
    else:
        #else choose the one with no of color equal to no of models
        if len(models)<3:
            groupColor=groupColorPal[3]
        else:
            groupColor=groupColorPal[len(models)]
    
    if len(groupColor)<len(models):
        groupColor=groupColor*3
        
    for key in meanValues.keys():
        subtype=key.split(":")[0]

        
        if temp=="":
            temp=subtype
            #color=groupColor[cc]
            #cc+=1
            dash=dashes[dc]
            dc+=1
            
        elif temp!=subtype:
            temp=subtype
            dash=dashes[dc]
            dc+=1
            
        color=groupColor[cc]
        cc+=1
        
        #if len(groupColor)==cc+1:
         #   cc=0
        if len(dashes)==dc+1:
            dc=0
            
        fig.add_trace(go.Scatter(x=xLabel, y=meanValues[key], name=key,
                                 line=dict(color=color, width=4,dash=dash,)))
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25),template="plotly_white",
                      )
    fig.update_layout(font=dict(family="Times New Roman",size=14,),
                      dragmode='drawopenpath',
                         newshape_line_color='#B32900',template="plotly_white",
                         modebar_add=['drawline','drawopenpath','drawclosedpath','drawcircle','drawrect', 'eraseshape'],
                        )
    fig.update_xaxes(type='category')
    #fig.update_xaxes(categoryorder="category ascending")
    fig.update_layout(xaxis_title=xAxis,yaxis_title=yAxis)
    #fig.show()
    return dcc.Graph(figure=fig,config=config)


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def getScatterPlot(area_up,barPlotColor,colorSP,colfacetSP,colRowSP):
    if colRowSP=="None":
        colRowSP=None
    if colfacetSP=="None":
        colfacetSP=None
    
    #get colors from pal
    groupColorPal=all_palettes[barPlotColor]
            #if no of model is larger than the second largest available color list of corr pallete, use last list that is longest one.
    models=list(set(area_up[colorSP].tolist()))
    if len(groupColorPal)<len(models):
        groupColor=groupColorPal[list(groupColorPal.keys())[-1]]
    else:
        #else choose the one with no of color equal to no of models
        if len(models)<3:
            groupColor=groupColorPal[3]
        else: 
            groupColor=groupColorPal[len(models)]
            
    fig = px.scatter(area_up, x='area (in pixels)', y="intensity", 
                     color_discrete_sequence=groupColor,
                     category_orders={colorSP: sorted(models)},
                     color=colorSP, facet_col=colfacetSP, facet_row=colRowSP)

    #width and height
    width=1000
    height=500
    if colfacetSP!=None:
        if len(set(area_up[colfacetSP].tolist()))>10:
            width=len(set(area_up[colfacetSP].tolist()))*150
        else:
            width=width
            
    if colRowSP!=None:
        if len(set(area_up[colRowSP].tolist()))>10:
            width=len(set(area_up[colRowSP].tolist()))*150
        else:
            width=width
        
    #print(set(area_up[colfacetSP].tolist()))
    #print(set(area_up[colRowSP].tolist())) 

    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25), width=width,
                      height=height)
    
    fig.update_layout(font=dict(family="Times New Roman",size=14,),
                      dragmode='drawopenpath',
                         newshape_line_color='#B32900',template="plotly_white",
                         modebar_add=['drawline','drawopenpath','drawclosedpath','drawcircle','drawrect', 'eraseshape'],
                        )
    
    #fig.show()
    return dcc.Graph(figure=fig,config=config)


def getRelScatterPlot(area_up,xAxis,yAxisType,baseline_temp,colorSP,colfacetSP,colRowSP,barPlotColor,xAxisOrder):
    

    #baseline
    baseline=()
    print(baseline_temp)
    a_0=baseline_temp.split(" -- ")  
    print(a_0)
 
    for item in a_0:
        baseline=baseline+(item.split(": ")[1],)
    print(baseline)  
        
    #facet
    groups=list(area_up.columns)[5:]
    yAxis='area (in pixels)'
    if colRowSP=="None":
        colRowSP=None
    if colfacetSP=="None":
        colfacetSP=None
        
    #color
    groupColorPal=all_palettes[barPlotColor]
    #if no of model is larger than the second largest available color list of corr pallete, use last list that is longest one.
    models=list(set(area_up[colorSP].tolist()))
    if len(groupColorPal)<len(models):
        groupColor=groupColorPal[list(groupColorPal.keys())[-1]]
    else:
        #else choose the one with no of color equal to no of models
        if len(models)<3:
            groupColor=groupColorPal[3]
        else: 
            groupColor=groupColorPal[len(models)]
        

    area_up_mean=pd.DataFrame(area_up.groupby(groups)[yAxis].mean())
    area_up_mean = pd.concat([area_up_mean, area_up_mean.index.to_frame(index=True)], axis = 1,ignore_index=True)
    area_up_mean.columns =[yAxis]+groups

    relArea_colName="Realtive "+yAxis+" compare to baseline<br>("+ baseline_temp+")"
    contr_colName="Contraction in "+yAxis+" compare to baseline<br>("+ baseline_temp+")"

   
    area_up_mean[relArea_colName]=(area_up_mean.loc[:,yAxis]/area_up_mean.loc[baseline,yAxis])*100
    area_up_mean[contr_colName]=area_up_mean.loc[baseline,relArea_colName]-area_up_mean.loc[:,relArea_colName]
    
    if yAxisType=="relArea":
        y=relArea_colName
    else:
        y=contr_colName

    symbols=[]
    
    i=0
    for index, row in area_up_mean.iterrows():  
        i+=1 
        if index==baseline:
            symbols.append("baseline") 
            if i>1:
                symbol_sequence=["circle","star"]
            else:
                symbol_sequence=["star","circle"]
            
        else:
            symbols.append("")



        
    area_up_mean["Baseline"]=symbols
    fig = px.scatter(area_up_mean, x=xAxis, y=y,symbol=area_up_mean["Baseline"],symbol_sequence=symbol_sequence,
                     facet_col=colfacetSP,facet_row=colRowSP,
    	         size=relArea_colName, color=colorSP,
                 category_orders={colorSP: sorted(models)},
                 color_discrete_sequence=groupColor)
    
    #fig.update_traces(marker_symbol=symbols,)
    fig.update_layout(yaxis=dict(ticksuffix="%")) 
    #fig.add_traces( px.scatter(area_up_mean.loc[[baseline]], x=xAxis, y=y,            
    #	         size=relArea_colName).update_traces(marker_symbol="star",marker_size=10).data)
    
    
    #width and height
    width=1000
    height=600
    if colfacetSP!=None:
        if len(set(area_up[colfacetSP].tolist()))>10:
            width=len(set(area_up[colfacetSP].tolist()))*150
        else:
            width=width
            
    if colRowSP!=None:
        if len(set(area_up[colRowSP].tolist()))>10:
            width=len(set(area_up[colRowSP].tolist()))*150
        else:
            width=width
        

    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25), 
                      width=width,
                      height=height
                      )
    
    fig.update_layout(font=dict(family="Times New Roman",size=14,),
                      dragmode='drawopenpath',
                         newshape_line_color='#B32900',template="plotly_white",
                         modebar_add=['drawline','drawopenpath','drawclosedpath','drawcircle','drawrect', 'eraseshape'],
                        )
    
    fig.update_xaxes(categoryorder='array', categoryarray= xAxisOrder)
    
    #fig.show()
    return dcc.Graph(figure=fig,config=config)

        
    
    
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
import dash_bootstrap_components as dbc
def getPlots(plotType,area_up,xAxis,yAxis,barPlotColor,updateOrder,xAxisOrder,colorSP,colfacetSP,colRowSP,
             baseline,colorSP_rel,colfacetSP_rel,colRowSP_rel):
    
    #set order for x-axis
    if updateOrder is None: 
        xAxisOrder=list(set(area_up[xAxis].tolist()))

           
    groups=list(area_up.columns)[5:] 
    groups.remove(xAxis)
    

    if plotType=="bar":
        div_row=[]
        col=1
        
        for i in range(len(groups)):
            
            color=groups[i]
            if col==1:
                div_col=[]
                div_col.append(dbc.Col(getBarPlot(area_up,xAxis,yAxis,barPlotColor,color,xAxisOrder)))
                col+=1
                if len(groups)==i+1:
                    div_row.append(dbc.Row(div_col))
                    div_row.append(dbc.Row(html.Hr(style={"borderTop": "dashed black"})))
                    
                
            else:
                
                col=1
                div_col.append(dbc.Col(getBarPlot(area_up,xAxis,yAxis,barPlotColor,color,xAxisOrder)))
                div_row.append(dbc.Row(div_col))
                div_row.append(dbc.Row(html.Hr(style={"borderTop": "dashed black"})))

                
        return html.Div(div_row)
    
    elif plotType=="treemap":
        grouptypes=list(area_up.columns)[5:]
        area_melt=pd.melt(area_up, id_vars=grouptypes, value_vars=[yAxis],var_name='filename', value_name=yAxis)
        fig = px.treemap(area_melt, path=[px.Constant("All Groups")]+grouptypes, values=yAxis,
                          color=yAxis,
                          color_continuous_scale=barPlotColor
                          )
        fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
        fig.update_layout(font=dict(family="Times New Roman",size=14,),
                          dragmode='drawopenpath',
                             newshape_line_color='#B32900',template="plotly_white",
                             modebar_add=['drawline','drawopenpath','drawclosedpath','drawcircle','drawrect', 'eraseshape'],
                            )
        
        #fig.show()
        return dcc.Graph(figure=fig,config=config)
    
    elif plotType=="scatter":
        return getScatterPlot(area_up,barPlotColor,colorSP,colfacetSP,colRowSP)
    
    elif plotType=="bubblePlot":
        return getRelScatterPlot(area_up,xAxis,yAxis,baseline,colorSP_rel,
                                 colfacetSP_rel,colRowSP_rel,barPlotColor,xAxisOrder)
    
    elif plotType=="line":

        return getLinePlot(area_up,xAxis,yAxis,barPlotColor,xAxisOrder)
    
    else:
        temp=xAxis
        div_row=[]
        for color in groups:
            xAxis=color
            color=temp
            
            col=1
            
            groupType=list(set(area_up[xAxis].tolist()))
            for i in range(len(groupType)):
                group=groupType[i]
                if col==1:
                    div_col=[]
                    div_col.append(dbc.Col(getBarPlotStat(area_up,xAxis,yAxis,group,barPlotColor,color,xAxisOrder)))
                    col+=1
                    if len(groupType)==i+1:
                        div_row.append(dbc.Row(div_col))
                        div_row.append(dbc.Row(html.Hr(style={"borderTop": "dashed black"})))
                    
                else:
                    
                    col=1
                    div_col.append(dbc.Col(getBarPlotStat(area_up,xAxis,yAxis,group,barPlotColor,color,xAxisOrder)))
                    div_row.append(dbc.Row(div_col))
                    div_row.append(dbc.Row(html.Hr(style={"borderTop": "dashed black"})))
                
        return html.Div(div_row)

