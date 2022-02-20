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
from summary_plots import plot_summary
#from ml_track_tool.flask_app import create_application




pd.set_option('colheader_justify', 'center')




def create_application(path):
    app=Flask(__name__)
    
    path=path.replace("\\","/")
    path="/".join(path.split("/")[:-1])
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
            if request.form['submit_btn']=="Show experiment":
                experiment_folder=request.form['experiment']
                files=glob.glob(f"{path}/{experiment_folder}/plots/*")
                if files:
                    for file in files:
                        shutil.copy(file,f"{current_path}/static/")  
                try:
                    shutil.copy(f"{path}/{experiment_folder}/notes/table_{experiment_folder}.html",f"{current_path}/templates/")

                except Exception as e:
                    pass
                return redirect(url_for("home2",experiment=experiment_folder))
            elif request.form['submit_btn']=="Show Summary":
                fig=plot_summary(path)
                print(len(fig))
                graphJSON=[]
                if(len(fig)==2):
                    graphJSON1 = json.dumps(fig[0], cls=plotly.utils.PlotlyJSONEncoder)
                    graphJSON.append(graphJSON1)
                    graphJSON2 = json.dumps(fig[1], cls=plotly.utils.PlotlyJSONEncoder)
                    graphJSON.append(graphJSON2)
                    num_graph=2
                    return render_template('summary.html', graphJSON=graphJSON,num_graph=num_graph)

                elif(len(fig)==1):
                    graphJSON1 = json.dumps(fig[0], cls=plotly.utils.PlotlyJSONEncoder)
                    graphJSON.append(graphJSON1)
                    num_graph=1
                    return render_template('summary.html', graphJSON=graphJSON,num_graph=num_graph)
                else:
                    return "<h1> No Info available</h1>"
        
        else:
            folders=os.listdir(path)

            return render_template("experiment_page.html",folders=folders)
        
    @app.route('/home2/<experiment>',methods=["POST","GET"])
    def home2(experiment):
        if request.method=='POST':
        
            notes=request.form['text_area']
            print(request)
            text_file = open(f"{path}/team_notes/notes.txt", "w")
            text_file.write(notes)
            text_file.close()
            '''
            get the latest downloaded table in the "download" folder
            and write it as html to experiment notes folder
            '''
            download_path=f"{Path.home()}/Downloads/*.html".replace("\\","/")
            latest_file=get_latest_file(download_path)
            if latest_file:
                shutil.copy(latest_file,"./templates/edited_templates/")
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
            plots_path=f"{path+'/'+exp_folder}/plots/"
            plot_files=glob.glob(f"{plots_path}/*")
            memory_file_path_exists=False
            history_file_path_exists=False
            prediction_file_path_exists=False
            plots_exists=False
            memory_dict={}
            history_dict={}
            pred_dict={}
            plot_lists=[]
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
            if plot_files:
                plots_exists=True
                plot_files=sorted(plot_files,key=os.path.getctime)
                plot_files=list(map(lambda x:x.replace("\\","/"),plot_files))
                plots_file_name=list(map(lambda x:x.split("/")[-1],plot_files))
                plot_lists=[]
                for file in plots_file_name:
                    file_id=file.split(".")[0]
                    if (f"{file_id}.txt" in plots_file_name):
                        with open(f"{plots_path}/{file_id}.txt", "r+") as file1:
                            notes_str=file1.read()
                    else:
                            notes_str=""
                    if not file.endswith(".txt"):
                            img_file="/static/"+file
                    else:
                        continue
                    plot_lists.append((img_file,notes_str,file_id))
            notes_path=f"{path}/team_notes/notes.txt"
            with open(notes_path) as f:
                contents = f.read()
            if ((memory_file_path_exists)or(history_file_path_exists)or(prediction_file_path_exists)):
                fig=plots(memory_dict,history_dict,pred_dict,memory_file_path_exists,history_file_path_exists,prediction_file_path_exists)
                graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
                show_metrics_graph=True
            else:
                fig = make_subplots(rows=1, cols=1)
                graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
                show_metrics_graph=False
                
            return render_template('visualization.html', graphJSON=graphJSON,user_notes=contents,table_path=table_path,show_metrics_graph=show_metrics_graph,img_list=plot_lists,plots_exist=plots_exists)
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
        ),row=row,col=col)
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
            plot_helper(fig,"Memory info unavailable",1,1)
            plot_helper(fig,"Memory info unavailable",1,2)
            
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
            plot_helper(fig,"Performance metrics info unavailable",2,1)
            plot_helper(fig,"Performance metrics info unavailable",2,2)
        
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
                y_true=np.argmax(y_true_val,axis=1)
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
            plot_helper(fig,"Prediction info unavailable",3,1)
            plot_helper(fig,"Prediction info unavailable",3,2)
            plot_helper(fig,"Prediction info unavailable",4,1)
           
        titles=[('Seconds','GPU Consumption (MB)'),('epochs','Loss'),('epochs','Accuracy'),('False Positive Rate','True Positive Rate'),('Recall','Precision')]
        i=2
        for title in titles:
            fig['layout'][f'xaxis{i}']['title']=title[0]
            fig['layout'][f'yaxis{i}']['title']=title[1]
            i+=1
        fig['layout']['xaxis']['title']='Seconds'
        fig['layout']['yaxis']['title']='RAM Consumption (MB)'
        fig.update_layout(autosize=False,width=1300,height=1500)
        return fig
    
    def get_latest_file(download_path):
        pattern=r'edited_page\(?'
        list_of_files = glob.glob(download_path)
        print(list_of_files)
        csv_files=list(map(lambda x:x.split("\\")[1],list_of_files))
        matched_files=list(filter(re.compile(pattern).match, csv_files))
        list_of_files=list(map(lambda x:f"{Path.home()}/Downloads/"+x,list(matched_files)))
        latest_file = max(list_of_files, key=os.path.getctime)
        return latest_file


    app.run()
