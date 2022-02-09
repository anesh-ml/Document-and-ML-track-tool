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

class Variable_data(object):
    instance = None

    def __init__(self, ipython):
        """Public constructor."""
        if Variable_data.instance is not None:
            raise Exception("""Only one instance of the Variable Inspector can exist at a 
                time.  Call close() on the active instance before creating a new instance.
                If you have lost the handle to the active instance, you can re-obtain it
                via `VariableInspectorWindow.instance`.""")
        
        Variable_data.instance = self
        self.closed = False
        self.namespace = NamespaceMagics()
        ipython.user_ns_hidden['widgets'] = widgets
        ipython.user_ns_hidden['NamespaceMagics'] = NamespaceMagics
        self.namespace.shell = ipython.kernel.shell

    def close(self):
        """Close and remove hooks."""
        if not self.closed:
            #self._ipython.events.unregister('post_run_cell', self.get_value)
            #self._box.close()
            self.closed = True
            Variable_data.instance = None

    def get_value(self):
        
        values = self.namespace.who_ls()
        return values
    
    def save_data(self,data,file_name):
        if not os.path.exists('experiment'):
            os.makedirs('experiment')
        data.to_csv(f"experiment/{file_name}.csv",index=False)
        
def copy(src,dst):
    path="/".join(dst.split("/")[:-1])
    if re.search('[a-zA-Z]',path):
        if not os.path.exists(path):
            os.makedirs(path)
    shutil.copy(src,dst)

def get_ram_usage():
    """
    Obtains the absolute number of RAM bytes currently in use by the system.
    :returns: System RAM usage in bytes.
    :rtype: int
    """
    return int(int(psutil.virtual_memory().total - psutil.virtual_memory().available) / 1024 / 1024)


def get_gpu_memory():
    output_to_list = lambda x: x.decode('ascii').split('\n')[:-1]
    ACCEPTABLE_AVAILABLE_MEMORY = 1024
    COMMAND = "nvidia-smi --query-gpu=memory.used --format=csv"
    try:
        memory_use_info = output_to_list(sp.check_output(COMMAND.split(),stderr=sp.STDOUT))[1:]
    except sp.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
    memory_use_values = [int(x.split()[0]) for i, x in enumerate(memory_use_info)]
    # print(memory_use_values)
    return memory_use_values[0]