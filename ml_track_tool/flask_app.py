#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask,render_template,url_for,request,redirect
import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import json
import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, roc_auc_score,precision_recall_curve,confusion_matrix
import jinja2
import plotly.figure_factory as ff
from pathlib import Path
import shutil
import pathlib
import glob
import re

pd.set_option('colheader_justify', 'center')



def create_application(path):
    app=Flask(__name__)
    path=path.replace("\\","/")
    current_path=pathlib.Path(__file__).parent.resolve()
    my_loader = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.FileSystemLoader(['/flaskapp/userdata',
                                 f"{current_path}/templates"]),
    ])
    app.jinja_loader = my_loader
    @app.route('/',methods=["POST","GET"])
    def home():   
        if request.method=='POST':
            experiment_folder=request.form['experiment']
            try:
                shutil.copy(f"{path}/{experiment_folder}/notes/table_{experiment_folder}.html",f"{current_path}/templates/")
            except Exception as e:
                pass
            return redirect(url_for("home2",experiment=experiment_folder))
        
        else:
            folders=os.listdir(path)

            return render_template("experiment_page.html",folders=folders)
        
    @app.route('/home2/<experiment>',methods=["POST","GET"])
    def home2(experiment):
        if request.method=='POST':
        
            notes=request.form['text']
            text_file = open(f"{path}/team_notes/notes.txt", "w")
            text_file.write(notes)
            text_file.close()
            download_path=f"{Path.home()}/Downloads/*.csv".replace("\\","/")
            latest_file=get_latest_file(download_path)
            if latest_file:
                df=pd.read_csv(latest_file).iloc[:,1:]
                df=df.replace(np.nan,"")
                html=df.to_html()
                html=html.replace('<table border="1" class="dataframe">','<table border="1" width="100%" contenteditable=true  class="dataframe" id="table_">')
                with open(f"{path}/{experiment}/notes/table_{experiment}.html", 'w') as f:
                    f.write(html)
                os.remove(latest_file)
            return redirect(url_for("home2",experiment=experiment))
        else:
            exp_folder=experiment
            table_path=f"table_{exp_folder}.html"
            
            if not os.path.exists(f"{current_path}/templates/{table_path}"):
                table_path="none"
            
            memory_path=f"{path+'/'+exp_folder}/memory_info/memory_metrics.json"
            history_path=f"{path+'/'+exp_folder}/performance/performance.json"
            prediction_path=f"{path+'/'+exp_folder}/prediction/prediction.json"

            memory_file_path_exists=False
            history_file_path_exists=False
            prediction_file_path_exists=False
            memory_dict={}
            history_dict={}
            pred_dict={}
            if os.path.exists(memory_path):
                memory_file = open(memory_path, "r")
                memory_dict=json.load(memory_file)
                memory_file_path_exists=True
            if os.path.exists(history_path):
                history_file = open(history_path, "r")
                history_dict=json.load(history_file)
                history_file_path_exists=True
            if os.path.exists(prediction_path):
                
                pred_file = open(prediction_path, "r")
                pred_dict=json.load(pred_file)
                prediction_file_path_exists=True
            if not os.path.exists(f"{path}/team_notes/"):
                os.mkdir(f"{path}/team_notes/")
                text_file = open(f"{path}/team_notes/notes.txt", "w")
                text_file.write("")
                text_file.close()
            notes_path=f"{path}/team_notes/notes.txt"
            with open(notes_path) as f:
                contents = f.read()
                
            fig=plots(memory_dict,history_dict,pred_dict,memory_file_path_exists,history_file_path_exists,prediction_file_path_exists)
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('visualization.html', graphJSON=graphJSON,user_notes=contents,table_path=table_path)
    def plot_helper(fig,text,row,col):
            fig.add_trace(go.Scatter(
            x=[0],
            y=[0],
            mode="lines+markers+text",showlegend=False,
            text=[text],
            textposition="bottom center",
            textfont=dict(
                family="sans serif",
                size=20,
                color="crimson"
            ),
        ),row=row[0],col=col[0])
            fig.add_trace(go.Scatter(
            x=[0],
            y=[0],
            mode="lines+markers+text",showlegend=False,
            text=[text],
            textposition="bottom center",
            textfont=dict(
                family="sans serif",
                size=20,
                color="crimson"
            ),
        ),row=row[1], col=col[1])
    def plot_confusion_matrix(fig,y_true,y_pred,x,y,row,col,labels):
        confusion_matrix_=confusion_matrix(y_true,y_pred)
        trace1 = ff.create_annotated_heatmap(z = confusion_matrix_,
                                 x = labels,
                                 y = labels,
                                 showscale  = False,name = "matrix")
        fig.add_trace(go.Heatmap(trace1.data[0]),row=row,col=col)
        
    def plots(memory_dict,history_dict,pred_dict,memory_file_path_exists,history_file_path_exists,prediction_file_path_exists):
             
        fig = make_subplots(rows=4, cols=2,subplot_titles=("RAM Consumption","GPU Consumption","Train & Validation loss","Train & Validation accuracy","ROC Curve","Precision-Recall Curve","Confusion matrix"))
        if(memory_file_path_exists):
            fig.add_trace(
            go.Scatter(y=memory_dict['ram'],name="RAM"),
            row=1, col=1)

            fig.add_trace(
                go.Scatter(y=memory_dict['gpu'],name="GPU"),
                row=1, col=2)
        else:
            plot_helper(fig,"Memory info unavailable",[1,1],[1,2])
            
        if(history_file_path_exists):
            keys=list(history_dict.keys())
            x3=[i for i in range(len(history_dict[keys[0]]))]
            fig.add_trace(
                go.Scatter(x=x3,y=history_dict[keys[0]],name=keys[0]),
                row=2, col=1)
            fig.add_trace(
                go.Scatter(x=x3,y=history_dict[keys[2]],name=keys[2]),
                row=2, col=1)
            fig.add_trace(
                go.Scatter(x=x3,y=history_dict[keys[1]],name=keys[1]),
                row=2, col=2)
            fig.add_trace(
                go.Scatter(x=x3,y=history_dict[keys[3]],name=keys[3]),
                row=2, col=2)
        else:
            plot_helper(fig,"Performance metrics info unavailable",[2,2],[1,2])        
        
        if prediction_file_path_exists:
            
            y_true_val=np.array(pred_dict['y_true'])
            y_pred_proba=np.array(pred_dict['y_pred'])
            
            if np.ndim(y_pred_proba)>1:
                y_pred=np.argmax(y_pred_proba,axis=1)
                labels_id=[i for i in range(y_pred_proba.shape[1])]
                for i in range(y_true_val.shape[1]):
                    y_true = y_true_val[:, i]
                    y_score = y_pred_proba[:, i]

                    fpr, tpr, _ = roc_curve(y_true, y_score)
                    auc_score = roc_auc_score(y_true, y_score)
                    precision, recall, thresholds = precision_recall_curve(y_true, y_score)
                    name = f"{i} (AUC={auc_score:.2f})"
                    fig.add_trace(go.Scatter(x=fpr, y=tpr, name=name, mode='lines'),row=3,col=1)
                    fig.add_trace(go.Scatter(x=[0,1], y=[0,1], line = dict(color='royalblue', dash='dash'),showlegend=False),row=3,col=1)
                    fig.add_trace(go.Scatter(x=recall, y=precision, fill='tozeroy',name=f"Precision-Recall Curve:{i}"),row=3,col=2)
                    fig.add_trace(go.Scatter(x=[1,0], y=[0,1], line = dict(color='royalblue', dash='dash'),showlegend=False),row=3,col=2)
                
                plot_confusion_matrix(fig,y_true,y_pred,[0,1],[0,1],4,1,labels_id)
            else:
                y_pred=np.round(y_pred_proba)
                labels_id=[0,1]
                fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
                auc_score = roc_auc_score(y_true, y_pred_proba)
                precision, recall, thresholds = precision_recall_curve(y_true, y_score)
                fig.add_trace(go.Scatter(x=fpr, y=tpr, fill='tozeroy'),row=3,col=2) # fill down to xaxis
                fig.add_trace(go.Scatter(x=[0,1], y=[0,1], line = dict(color='royalblue', dash='dash'),showlegend=False),row=3,col=2)
                fig.add_trace(go.Scatter(x=recall, y=precision, fill='tozeroy',name=f"Precision-Recall Curve"),row=3,col=2) # fill down to xaxis
                fig.add_trace(go.Scatter(x=[1,0], y=[0,1], line = dict(color='royalblue', dash='dash'),showlegend=False),row=3,col=2)
                plot_confusion_matrix(fig,y_true,y_pred,[0,1],[0,1],4,1,labels_id)
        
        else:
            plot_helper(fig,"Prediction info unavailable",[3,3],[1,2])
           
        
        fig['layout']['xaxis']['title']='Seconds'
        fig['layout']['yaxis']['title']='RAM Consumption (MB)'
        fig['layout']['xaxis2']['title']='Seconds'
        fig['layout']['yaxis2']['title']='GPU Consumption (MB)'
        fig['layout']['xaxis3']['title']='epochs'
        fig['layout']['yaxis3']['title']='Loss'
        fig['layout']['xaxis4']['title']='epochs'
        fig['layout']['yaxis4']['title']='Accuracy'
        fig['layout']['xaxis5']['title']='False Positive Rate'
        fig['layout']['yaxis5']['title']='True Positive Rate'
        fig['layout']['xaxis6']['title']='Recall'
        fig['layout']['yaxis6']['title']='Precision'
        fig.update_layout(autosize=False,width=1300,height=1500)
        return fig
    
    def get_latest_file(download_path):
        pattern=r'export_table_\(?'
        list_of_files = glob.glob(download_path)
        csv_files=list(map(lambda x:x.split("\\")[1],list_of_files))
        matched_files=list(filter(re.compile(pattern).match, csv_files))
        list_of_files=list(map(lambda x:f"{Path.home()}/Downloads/"+x,list(matched_files)))
        latest_file = max(list_of_files, key=os.path.getctime)
        return latest_file


    app.run()




