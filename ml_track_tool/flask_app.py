
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
from pathlib import Path
import shutil
import pathlib
import glob
import re
from ml_track_tool.summary_plots import plot_summary
import imagesize
import seaborn as sns
import matplotlib.pyplot as plt
import base64
import io



def create_application(path):
    app=Flask(__name__,static_folder=f"{path}/plots")
    path=path.replace("\\","/")
    current_path=pathlib.Path(__file__).parent.resolve()
    if not os.path.exists(f"{path}/plots/logo"):
        os.makedirs(f"{path}/plots/logo")
    shutil.copy(f"{current_path}/logo.jpg",f"{path}/plots/logo")
    path="/".join(path.split("/")[:-1])
    current_path=pathlib.Path(__file__).parent.resolve()
    my_loader = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.FileSystemLoader(['/flaskapp/userdata',
                                 f"{current_path}/templates"]),
    ])
    app.jinja_loader = my_loader
    sns.set_theme()
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
                    renamed_file=f"{Path.home()}/Downloads/{file_name}.txt"
                    os.rename(file,renamed_file)
                    shutil.move(renamed_file,f"{path+'/'+experiment}/plots/{file_name}.txt")
            if download_files_json:
                if not os.path.exists(f"{path+'/'+experiment}/document"):
                    os.makedirs(f"{path+'/'+experiment}/document")
                for file in doc_files_json:
                    file_name=file.split("/")[-1]
                    shutil.move(f"{Path.home()}/Downloads/{file_name}",f"{path+'/'+experiment}/document/{file_name}")

            notes=request.form.get("text_area_txt")
            text_file = open(f"{path}/{experiment}/team_notes/notes.txt", "w")
            text_file.write(notes)
            text_file.close()
            return redirect(url_for("experiment_page",experiment=experiment))
        else:
            exp_folder=experiment
            memory_path=f"{path+'/'+exp_folder}/memory_info/memory_metrics.json"
            history_path=f"{path+'/'+exp_folder}/performance/performance.json"
            prediction_path=f"{path+'/'+exp_folder}/prediction/prediction.json"
            plots_path=f"{path+'/'+exp_folder}/plots/"
            note_doc_path=f"{path+'/'+exp_folder}/document/*_docu.json"
            note_doc_files=glob.glob(note_doc_path)
            note_doc_files=list(map(lambda x:x.replace("\\","/"),note_doc_files))
            plot_files=glob.glob(f"{plots_path}/*.*")
            memory_file_path_exists=False
            history_file_path_exists=False
            prediction_file_path_exists=False
            plots_exists=False
            memory_dict={}
            history_dict={}
            pred_dict={}
            plot_lists=[]
            doc_contents=[]
            prev_num_doc=0
            docs_exists=False
            note_doc_exists=False
            plots_dict={}
            note_doc_dict={}
            if os.path.exists(memory_path):
                memory_file = open(memory_path, "r")
                memory_dict=json.load(memory_file)
                memory_file.close()
                fig, axes = plt.subplots(1, 2,figsize=(18,5))
                sns.lineplot(x=np.arange(len(memory_dict['gpu'])),y=memory_dict['gpu'],ax=axes[0])
                sns.lineplot(x=np.arange(len(memory_dict['ram'])),y=memory_dict['ram'],ax=axes[1])
                axes[0].set_title("GPU Consumption")
                axes[1].set_title("RAM Consumption")
                axes[0].set_ylabel("consumption (MB)")
                axes[0].set_xlabel("Time (s)")
                axes[1].set_ylabel("consumption (MB)")
                axes[1].set_xlabel("Time (s)")
                base64_plt=to_base64(plt)
                plots_dict['memory']=base64_plt.decode("utf-8")
                plots_dict['memory_exists']=True
            else:
                plots_dict['memory_exists']=False
            if os.path.exists(history_path):
                history_file = open(history_path, "r")
                history_dict=json.load(history_file)
                history_file.close()
                fig, axes = plt.subplots(1, 2,figsize=(18,5))
                sns.lineplot(x=np.arange(len(history_dict['val_categorical_accuracy'])),y=history_dict['val_categorical_accuracy'],ax=axes[0])
                sns.lineplot(x=np.arange(len(history_dict['categorical_accuracy'])),y=history_dict['categorical_accuracy'],ax=axes[0])
                sns.lineplot(x=np.arange(len(history_dict['loss'])),y=history_dict['loss'],ax=axes[1])
                sns.lineplot(x=np.arange(len(history_dict['val_loss'])),y=history_dict['val_loss'],ax=axes[1])
                axes[0].set_title("Accuracy")
                axes[0].set_ylabel("accuracy")
                axes[0].set_xlabel("Epochs")
                axes[1].set_ylabel("loss")
                axes[1].set_xlabel("epochs")
                base64_plt=to_base64(plt)
                plots_dict['history']=base64_plt.decode("utf-8")
                plots_dict['history_exists']=True
            else:
                plots_dict['history_exists']=False
            if os.path.exists(prediction_path):
                pred_file = open(prediction_path, "r")
                pred_dict=json.load(pred_file)
                pred_file.close()
                fig, axes = plt.subplots(1, 1,figsize=(9,5))
                y_true=np.argmax(pred_dict['y_true'],axis=1)
                y_pred=np.argmax(pred_dict['y_pred'],axis=1)
                cf=confusion_matrix(y_true,y_pred)
                sns.heatmap(cf,cbar=False,annot=True,ax=axes,fmt='g')
                axes.set_xlabel("Predicted")
                axes.set_ylabel("True labels")
                base64_plt=to_base64(plt)
                plots_dict['prediction']=base64_plt.decode("utf-8")
                plots_dict['prediction_exists']=True
            else:
                plots_dict['prediction_exists']=False
            if (note_doc_files):
                for file in note_doc_files:
                    if 'doc_notes_docu' not in file:
                        doc_id="_".join(file.split("/")[-1].split("_")[:2])
                        doc_file = open(file, "r")
                        doc_dict=json.load(doc_file)
                        doc_dict['id_']=doc_id
                        doc_contents.append(doc_dict)
                        docs_exists=True
                        doc_file.close()
                    else:
                        note_doc = open(file, "r")
                        note_doc_dict=json.load(note_doc)
                        note_doc_exists=True
                        note_doc.close()
                num_doc=list(map(lambda x:x.split("/")[-1][:-5].split("_")[1],note_doc_files))
                try:
                    prev_num_doc=int(max(x for x in num_doc if x.isdigit()))+1
                except Exception as e:
                    pass
            if not os.path.exists(f"{path}/{exp_folder}/team_notes/"):
                os.makedirs(f"{path}/{exp_folder}/team_notes/")
                text_file = open(f"{path}/{exp_folder}/team_notes/notes.txt", "w")
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
                            notes_str_list=notes_str.split("{title}:")
                            notes_str=notes_str_list[0]
                            title=notes_str_list[-1] if len(notes_str_list)>1 else "Title" 
                            
                    else:
                            notes_str=""
                            title="Title"
                    if not file.endswith(".txt"):
                        with open(f"{path+'/'+exp_folder}/plots/{file}", "rb") as image_file:
                                encoded_img = base64.b64encode(image_file.read()).decode("utf-8")
                        width, height = imagesize.get(f"{path+'/'+exp_folder}/plots/{file}")
                    else:
                        continue
                    plot_lists.append((encoded_img,notes_str,file_id,width,f"save_note_{file_id}_txt",title))
            notes_path=f"{path}/{exp_folder}/team_notes/notes.txt"
            with open(notes_path) as f:
                team_notes = f.read()
            return render_template('visualization.html',img_list=plot_lists,plots_exist=plots_exists,page_title=experiment,doc_contents=doc_contents,note_doc=note_doc_dict,prev_num_doc=prev_num_doc,plots_dict=plots_dict,docs_exists=docs_exists,note_doc_exists=note_doc_exists,team_notes=team_notes)
    
    
    def to_base64(plt):
        my_stringIObytes = io.BytesIO()
        plt.savefig(my_stringIObytes, format='jpg')
        my_stringIObytes.seek(0)
        my_base64_jpgData = base64.b64encode(my_stringIObytes.read())
        return my_base64_jpgData
    
    app.run()
    
    