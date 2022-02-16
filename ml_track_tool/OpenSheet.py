import pandas as pd
from ipysheet import from_dataframe
import re
import ipysheet
import os
import pathlib

def open_sheet(source,rows=None,columns=None):
    type_=type(source).__name__
    
    if type_=='DataFrame':
        if rows:
            source=source.iloc[:rows,:]
        sheet=from_dataframe(source)
        sheet.column_width=[10]*len(source.columns)
        return sheet
    
    elif(".csv" in source):
        df=pd.read_csv(source)
        sheet=from_dataframe(df)
        return sheet
    
    elif(source=="new sheet"):
        rows=["" for _ in range(rows)]
        data={i:rows for i in list(map(chr, range(65, 65+columns)))}
        df=pd.DataFrame(data)
        sheet=ipysheet.from_dataframe(df)
        sheet.column_width=[10]*len(df.columns)
        return sheet
    
def download_sheet(sheet,file):
    
    path="/".join(file.split("/")[:-1])
    file_name=file.split("/")[-1].split(".")[0]
    experiment_name=file.split('/')[-2]
    if re.search('[a-zA-Z]',path):
        if not os.path.exists(path):
            os.makedirs(path)
    df=ipysheet.to_dataframe(sheet)
    if(file.endswith(".csv")):
        df.to_csv(file,index=False)
    elif(file.endswith(".xls")):
        html=df.to_html()
        html=html.replace('<table border="1" class="dataframe">','<table border="1" width="100%" contenteditable=true  class="dataframe" id="table_">')
        #if re.search('[a-zA-Z]',path):
        if not os.path.exists(path+f"/notes/"):
            os.makedirs(path+f"/notes/")
        with open(path+f"/notes/table_{experiment_name}.html", 'w') as f:
                f.write(html)
        with pd.ExcelWriter(file,mode='w') as writer:
                df.to_excel(writer,sheet_name="notes",index=False,header=True)
                
                
    