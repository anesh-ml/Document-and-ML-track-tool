# ML tracking tool 

- This is still a prototype and some features are yet to be developed

- Users can for now,

    - DO **data versioning** and **notebook versioning**
    - Open a spreadsheet(not excel spreadsheet) from a **dataframe, file and create a new spreadsheet**
    - **Interpret ML models** using LIME and Shapley. Analyze the model output and then may be curate/edit the data based on the interpretation
    - **Plot metrics** such as accuracy, precision, recall and ROC curve. With a click, users can know these metrics and then maybe jot down these metrics in a spreadsheet and download it.
    - Users can **write down notes, metrics** in the spreadsheet and **download** to a folder.

- All these can be done with a button click. Users just need to type the arguments in a cell and click the appropriate button.

## Open spreadsheet

- Create a spreadsheet from dataframe,file or a new spreadsheet


### If opening from **dataframe**:

   **Command**: $ \textit{DataFrame}$ `rows`
    
        Eg: df 10 or df
        
    - rows is given if you want to return only top n_rows
    
    
### If opening a sheet from a **file**

 **Command**: `FileName`
 
         Eg: "sample_data.csv"
         
### Opening a **new spreadsheet**

   **Command**: `"new sheet",n_rows,n_cols`

-------------------------------------------------------------------------------------------------------------------------------

## Edit sheet

- Operations supported are **creating columns** and **filter**

### Create columns

**Command**: `create_col n_col`

        Eg: create_col 3
        
### Filter sheet

- Only **==** and multiple **AND** conditions are supported now. 

**Command**: `filter  condition`

        Eg: filter "col==question&col==request"
        


-------------------------------------------------------------------------------------------------------------------------------

## Interpret Model

- Currently, interpretation for NLP model is supported. Will be extending it to computer vision model.

**Command**: `class_name(list), sheet/text, inference code`

- **class_name** can be like ["positive","negative"]. 

- input can be a **sheet, list of texts or just a single sentence**.

- **inference code** is the prediction code which take in **raw string** and **output probabilities**.

      Eg: ['postive','negative'], ["movie is good", 'waste of money'], inference_code
      
          ["positive","negative"],sheet,inference_code
            
          ["positive","negative"],"movie is good",inference_code

--------------------------------------------------------------------------------------------------------------------------------

## Download sheet

- Download the filled sheet. It will download the latest created and edited sheet.

**Command**: `"./folder/sheet.xls"`

-------------------------------------------------------------------------------------------------------------------------------

## Notebook Versioning

- Save the notebook with different to a folder and keep working in the same notebook.

- With a single click, make a version of your notebook.

**Command**: file path

    eg: "./experiment1/notebook_v1.ipynb"

--------------------------------------------------------------------------------------------------------------------------------

## Plot metrics

- Plot ROC curve along the accuracy, F1 score, precision, recall.

- User needs to get the probability of the prediction and true labels.

        Eg: y_true,y_pred_proba
