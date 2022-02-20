import lime
from lime import lime_text
from lime.lime_text import LimeTextExplainer
import ipysheet

def lime_explainer(class_names,text,predict_proba):
    explainer = LimeTextExplainer(class_names = class_names) 
    if type(text)==list:
        for i in range(len(text)):
            exp = explainer.explain_instance(text[i], predict_proba)
            exp.show_in_notebook(text=text[i])
            
    elif type(text)==str:
        exp = explainer.explain_instance(text, predict_proba)
        exp.show_in_notebook(text=text)
        
    elif type(text).__name__=='Sheet':
        df=ipysheet.to_dataframe(text)
        cols=df.columns.tolist()
        text=df[df[cols[-1]]=="y"][cols[0]].values.tolist()
        for i in range(len(text)):
            exp = explainer.explain_instance(text[i], predict_proba)
            exp.show_in_notebook(text=text[i])