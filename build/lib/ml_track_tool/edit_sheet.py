
import pandas as pd
import ipywidgets as widgets # Loads the Widget framework.
from ipysheet import from_dataframe
import ipysheet

def filter_(sheet,query):
    
    df=ipysheet.to_dataframe(sheet)
    condition=query.split("&")
    value=list(map(lambda x:x.split("==")[1].strip(),condition))
    col=list(map(lambda x:x.split("==")[0].strip(),condition))[0]
    
    value=[int(val) if val.isdigit() else val for val in value ]

    df=df[df[col].isin(value)]
   
    sheet=from_dataframe(df)
    sheet.column_width=[10]*len(df.columns)
    return sheet

def create_column(n_cols,sheet):
    df=ipysheet.to_dataframe(sheet)
    for i in range(n_cols):
        df[f"col{i}"]=""
    sheet=from_dataframe(df)
    sheet.column_width=[10]*len(df.columns)
    return sheet