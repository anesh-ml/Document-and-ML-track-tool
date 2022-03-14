from pydoc import doc
import ipywidgets as widgets # Loads the Widget framework.
from IPython.core.magics.namespace import NamespaceMagics # Used to query namespace.
import os
import shutil
import re
import psutil
import subprocess as sp
import os
from threading import Thread , Timer
import sched, time
import json
from ipysheet import from_dataframe
import ipysheet
from timeit import default_timer as timer



class Monitor(Thread):
    def __init__(self,delay,path):
        super(Monitor,self).__init__()
        self.stopped=False
        self.delay=delay
        self.path=path
        self.memory={'gpu':[],'ram':[]}
        self.base_ram=self.get_ram_usage()
        self.base_gpu=self.get_gpu_memory()
        self.start_time=timer()
        self.start()
    
    def run(self):
        
        
        while not self.stopped:
            gpu=self.get_gpu_memory()
            ram=self.get_ram_usage()
            abs_gpu=0 if gpu-self.base_gpu<0 else gpu-self.base_gpu
            abs_ram=0 if ram-self.base_ram<0 else ram-self.base_ram
            self.memory['gpu'].append(abs_gpu)
            self.memory['ram'].append(abs_ram)
            time.sleep(self.delay)
            
    def get_ram_usage(self):
        
        """
        Obtains the absolute number of RAM bytes currently in use by the system.
        :returns: System RAM usage in bytes.
        :rtype: int

        """
        return int(int(psutil.virtual_memory().total - psutil.virtual_memory().available) / 1024 / 1024)


    def get_gpu_memory(self):
        
        output_to_list = lambda x: x.decode('ascii').split('\n')[:-1]
        ACCEPTABLE_AVAILABLE_MEMORY = 1024
        COMMAND = "nvidia-smi --query-gpu=memory.used --format=csv"
        try:
            memory_use_info = output_to_list(sp.check_output(COMMAND.split(),stderr=sp.STDOUT))[1:]
        except sp.CalledProcessError as e:
            raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
        memory_use_values = [int(x.split()[0]) for i, x in enumerate(memory_use_info)]

        return memory_use_values[0]
    
    def stop(self):
        total_time=timer()-self.start_time
        self.stopped=True
        total_ram_consumption=max(self.memory['ram'])-min(self.memory['ram'])
        total_gpu_consumption=max(self.memory['gpu'])-min(self.memory['gpu'])
        self.memory['max_gpu_consumption']=total_gpu_consumption
        self.memory['max_ram_consumption']=total_ram_consumption
        self.memory['execution_time']=total_time
        if not os.path.exists(f"{self.path}/memory_info/"):
            os.makedirs(f"{self.path}/memory_info/")
        a_file = open(f"{self.path}/memory_info/memory_metrics.json", "w")
        a_file = json.dump(self.memory, a_file)
        
        
def copy(src,dst):
    path="/".join(dst.split("/")[:-1])
    if re.search('[a-zA-Z]',path):
        if not os.path.exists(path):
            os.makedirs(path)
    shutil.copy(src,dst)

def save_dict(dict_,file_type,file_path):
    #path="/".join(file_path.split("/")[:-1])
    #file_name=file_path.split("/")[-1]
    file_path=file_path.replace("\\","/")
    file_type=file_type.lower()
    types=["performance","prediction"]
    if file_type in types:
        file_path_type=file_path+"/"+file_type
        if not os.path.exists(file_path_type):
            os.makedirs(file_path_type)
        a_file = open(file_path_type+f"/{file_type}.json", "w")
        a_file = json.dump(dict_, a_file)
    elif(file_type=="none"):
        a_file = open(file_path, "w")
        a_file = json.dump(dict_, a_file)
    else:
        print("file type not one of [performance,prediction,none]")

def add2doc(EXP_PATH,input_):
    input_type=type(input_).__module__+" "+type(input_).__name__
    if input_type=='ipysheet.sheet Sheet':
        df=ipysheet.to_dataframe(input_)
        html=df.to_html()
        html=html.replace('<table border="1" class="dataframe">','<table border="1" width="100%" contenteditable=true')
        with open(f"{EXP_PATH}/document/doc_notes_docu.txt", 'a') as file:
            file.write(html+"\n")
    else:
        if not os.path.exists(f"{EXP_PATH}/document/"):
            os.mkdir(f"{EXP_PATH}/document/")  
            with open(f"{EXP_PATH}/document/doc_notes_docu.json", "w") as file1:
                json.dump({"contents":"","title":"Title"}, file1)
        elif not os.path.exists(f"{EXP_PATH}/document/doc_notes_docu.json"):
            with open(f"{EXP_PATH}/document/doc_notes_docu.json", "w") as file1:
                json.dump({"contents":"","title":"Title"}, file1)
        
        with open(f"{EXP_PATH}/document/doc_notes_docu.json", 'r') as file:
            doc_=json.load(file)
            contents=f"{doc_['contents']}<br>{input_}"
            doc_["contents"]=contents
        with open(f"{EXP_PATH}/document/doc_notes_docu.json", 'w') as file:
            json.dump(doc_, file)