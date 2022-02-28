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
import imagesize

#from ml_track_tool.flask_app import create_application


# In[2]:


pd.set_option('colheader_justify', 'center')


# In[3]:


def create_application(path):
    app=Flask(__name__,static_folder=f"{path}/plots")
    
    path=path.replace("\\","/")
    path="/".join(path.split("/")[:-1])
    #current_path=pathlib.Path(__file__).parent.resolve()
    current_path="./"
    my_loader = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.FileSystemLoader(['/flaskapp/userdata',
                                 "./templates"]),
    ])
    app.jinja_loader = my_loader
    @app.route('/',methods=["POST","GET"])
    def home():   
        if request.method=='POST':
            if request.form['submit_btn']=="Show experiment":
                experiment_folder=request.form['experiment'] 
                return redirect(url_for("experiment_page",experiment=experiment_folder))
            elif request.form['submit_btn']=="Show Summary":
                figs=plot_summary(path)
                graphJSONs=[]
                if figs:
                    for i,fig in enumerate(figs):
                        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
                        graphJSONs.append((f"chart_{i}",graphJSON))
                    return render_template('summary.html', graphJSONs=graphJSONs)
                else:
                    return "<h1> No Info available</h1>"
        
        else:
            folders=os.listdir(path)

            return render_template("experiment_page.html",folders=folders)
        
    @app.route('/experiment_page/<experiment>',methods=["POST","GET"])
    def experiment_page(experiment):
        if request.method=='POST':
            download_files_txt=f"{Path.home()}/Downloads/*_docu.txt"
            download_files_json=f"{Path.home()}/Downloads/*_docu.json"
            doc_files_txt=glob.glob(download_files_txt)
            doc_files_json=glob.glob(download_files_json)
            doc_files_txt=list(map(lambda x:x.replace("\\","/"),doc_files_txt))
            doc_files_json=list(map(lambda x:x.replace("\\","/"),doc_files_json))
            if download_files_txt:
                for file in doc_files_txt:
                    file_name=file.split("/")[-1][:-9]
                    print(file_name)
                    renamed_file=f"{Path.home()}/Downloads/{file_name}.txt"
                    os.rename(file,renamed_file)
                    shutil.move(renamed_file,f"{path+'/'+experiment}/plots/{file_name}.txt")
            if download_files_json:
                for file in doc_files_json:
                    file_name=file.split("/")[-1]
                    shutil.move(f"{Path.home()}/Downloads/{file_name}",f"{path+'/'+experiment}/document/{file_name}")

            notes=request.form.get("text_area_txt")
            text_file = open(f"{path}/team_notes/notes.txt", "w")
            text_file.write(notes)
            text_file.close()
            return redirect(url_for("experiment_page",experiment=experiment))
        else:
            exp_folder=experiment
            table_path=f"table_{exp_folder}.html"
            
            if not os.path.exists(f"{current_path}/templates/{table_path}"):
                table_path="none"
            
            memory_path=f"{path+'/'+exp_folder}/memory_info/memory_metrics.json"
            history_path=f"{path+'/'+exp_folder}/performance/performance.json"
            prediction_path=f"{path+'/'+exp_folder}/prediction/prediction.json"
            plots_path=f"{path+'/'+exp_folder}/plots/"
            note_doc_path=f"{path+'/'+exp_folder}/document/*_docu.json"
            note_doc_files=glob.glob(note_doc_path)
            note_doc_files=list(map(lambda x:x.replace("\\","/"),note_doc_files))
            plot_files=glob.glob(f"{plots_path}/*")
            
            memory_file_path_exists=False
            history_file_path_exists=False
            prediction_file_path_exists=False
            plots_exists=False
            memory_dict={}
            history_dict={}
            pred_dict={}
            plot_lists=[]
            doc_contents=[]
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
            if (note_doc_files):
                for file in note_doc_files:
                    doc_id=file.split("/")[-1]
                    doc_file = open(file, "r")
                    doc_dict=json.load(doc_file)
                    doc_dict['id_']=doc_id
                    doc_contents.append(doc_dict)
                
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
                width,height=800,550
                for file in plots_file_name:
                    file_id=file.split(".")[0]
                    if (f"{file_id}.txt" in plots_file_name):
                        with open(f"{plots_path}/{file_id}.txt", "r+") as file1:
                            notes_str=file1.read()
                            notes_str=notes_str.strip().split("{title}:")
                            
                            if len(notes_str)==2:
                                print(notes_str[1])
                                notes_str,title=notes_str[0],notes_str[1]
                            else:
                                notes_str,title=notes_str[0]," "
                    else:
                            notes_str=""
                    if not file.endswith(".txt"):
                            if file.endswith('json'):
                                with open(f"{plots_path}/{file}", "r+") as file1:
                                    img_file = json.load(file1)
                                    file_type="plotly"
                            else:
                                width, height = imagesize.get(f"{path+'/'+exp_folder}/plots/{file}")
                                img_file="/plots/"+file
                                file_type="image"
                    else:
                        continue
                    plot_lists.append((img_file,notes_str,file_id,width,f"save_note_{file_id}_txt",file_type,title))
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
            return render_template('visualization.html', graphJSON=graphJSON,user_notes=contents,table_path=table_path,show_metrics_graph=show_metrics_graph,img_list=plot_lists,plots_exist=plots_exists,page_title=experiment,doc_contents=doc_contents)
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
        pattern=r'notes_docu\(?'
        list_of_files = glob.glob(download_path)
        csv_files=list(map(lambda x:x.split("\\")[1],list_of_files))
        matched_files=list(filter(re.compile(pattern).match, csv_files))
        list_of_files=list(map(lambda x:f"{Path.home()}/Downloads/"+x,list(matched_files)))
        if list_of_files:
            latest_file = max(list_of_files, key=os.path.getctime)
        else:
            latest_file=""
        return latest_file


    app.run()


# In[4]:


path=os.path.abspath("../")
create_application("D:\demo_folder\experiment2")


# In[ ]:


get_ipython().run_line_magic('tb', '')


# In[ ]:




