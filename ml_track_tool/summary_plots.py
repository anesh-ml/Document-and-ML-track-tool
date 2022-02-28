#!/usr/bin/env python
# coding: utf-8

# In[1]:


import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import json
import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score,accuracy_score,f1_score,precision_score,recall_score
import glob


# In[2]:


def get_exp_folders(exp_path):
    experiments=glob.glob(exp_path+"/*")
    experiments=list(map(lambda x:x.replace("\\","/"),experiments))
    experiments_list=list(map(lambda x:x.split("/")[-1],experiments))
    experiments_list_=[]
    experiments=[]
    for e in experiments_list:
        if not("." in e):
            experiments.append(f"{exp_path}/{e}")
            experiments_list_.append(e)
    return experiments,experiments_list_


# In[64]:


def get_metrics(exp_path):
    metrics_exp={}
    experiments,experiments_list_=get_exp_folders(exp_path)
    for i,exp in enumerate(experiments):
        prediction_path=f"{exp}/prediction/prediction.json"
        if os.path.exists(prediction_path):
            metrics_exp[experiments_list_[i]]={}
            pred_file = open(prediction_path, "r")
            pred_dict=json.load(pred_file)
            pred_file.close()
            y_true=np.array(pred_dict['y_true'])
            y_pred_proba=np.array(pred_dict['y_pred'])
            if(np.ndim(y_true)>1):
                y_true=np.argmax(y_true,axis=1)
                y_pred=np.argmax(y_pred_proba,axis=1)
                accuracy=accuracy_score(y_true,y_pred)*100
                f1score=f1_score(y_true,y_pred)*100
                precision=precision_score(y_true,y_pred)*100
                recall=recall_score(y_true,y_pred)*100
                metrics=['accuracy','f1score','precision','recall']
                for metric in metrics:
                    metrics_exp[experiments_list_[i]][metric]=round(eval(metric),3)
            else:
                y_pred=np.round(y_pred_proba)
                accuracy=accuracy_score(y_true,y_pred)
                f1score=f1_score(y_true,y_pred)
                precision=precision_score(y_true,y_pred)
                recall=recall_score(y_true,y_pred)
                metrics=['accuracy','f1score','precision','recall']
                for metric in metrics:
                    metrics_exp[experiments_list_[i]]['accuracy']=round(eval(metric),3)
    return metrics_exp    


# In[65]:


def get_memory(exp_path):
    memory_exp={}
    experiments,experiments_list_=get_exp_folders(exp_path)
    for i,exp in enumerate(experiments):
        memory_path=f"{exp}/memory_info/memory_metrics.json"
        if os.path.exists(memory_path):
            memory_exp[experiments_list_[i]]={}
            memory_file = open(memory_path, "r")
            memory_dict=json.load(memory_file)
            memory_exp[experiments_list_[i]]['ram']=memory_dict["max_ram_consumption"]
            memory_exp[experiments_list_[i]]['gpu']=memory_dict["max_gpu_consumption"]
            memory_exp[experiments_list_[i]]['execution_time']=memory_dict["execution_time"]
            memory_file.close()
    return memory_exp


# In[66]:


def plot_summary(exp_path):
    metrics_exp=get_metrics(exp_path)
    memory_exp=get_memory(exp_path)
    experiment_names_metrics = list(metrics_exp.keys())
    figs=[]
    if len(experiment_names_metrics)>0:
        fig1 = go.Figure()

        fig1.add_trace(go.Scatter(
            x=[metrics_exp[exp]['accuracy'] for exp in experiment_names_metrics],
            y=experiment_names_metrics,
            marker=dict(color="crimson", size=12),
            mode="markers",
            name="accuracy",
        ))

        fig1.add_trace(go.Scatter(
            x=[metrics_exp[exp]['f1score'] for exp in experiment_names_metrics],
            y=experiment_names_metrics,
            marker=dict(color="gold", size=12),
            mode="markers",
            name="f1 score"
        ))
        fig1.add_trace(go.Scatter(
            x=[metrics_exp[exp]['precision'] for exp in experiment_names_metrics],
            y=experiment_names_metrics,
            marker=dict(color="blue", size=12),
            mode="markers",
            name="precision"
        ))
        fig1.add_trace(go.Scatter(
            x=[metrics_exp[exp]['recall'] for exp in experiment_names_metrics],
            y=experiment_names_metrics,
            marker=dict(color="purple", size=12),
            mode="markers",
            name="recall"
        ))
        update_layout_(fig1,"Performance comparison","Percentage","Experiments")
        figs.append(fig1)
    experiment_names_memory = list(memory_exp.keys())
    if len(experiment_names_memory)>0:
        fig2 = go.Figure(data=[
            go.Bar(name='gpu', x=[memory_exp[exp]['gpu'] for exp in experiment_names_memory], y=experiment_names_memory,orientation='h'),
            go.Bar(name='ram', x=[memory_exp[exp]['ram'] for exp in experiment_names_memory], y=experiment_names_memory,orientation='h'),    
        ])
        fig3 = go.Figure(data=[
                go.Bar(name='execution time', x=[memory_exp[exp]['execution_time'] for exp in experiment_names_memory], y=experiment_names_memory,orientation='h')

        ])
        # Change the bar mode
        fig2.update_layout(barmode='group')
        update_layout_(fig2,"Memory Consumption","memory(MB)","Experiments")
        update_layout_(fig3,"Total execution time","time(seconds)","Experiments")
        figs.append(fig2)
        figs.append(fig3)
    return figs

def update_layout_(fig_,title,xaxis_title,yaxis_title):
    fig_.update_layout(
    title=title,
    xaxis_title=xaxis_title,
    yaxis_title=yaxis_title,
    font=dict(
        family="times new roman",
        size=16,
        color="black"
    )
)

