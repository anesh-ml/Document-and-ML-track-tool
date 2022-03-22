<h1 style="text-align:center"> Documenting and ML tracking tool</h1> 

## Purpose of the app

- This application is created to do some of the data science development work like documentation, compare supervised ML algorithms using jupyter notebook.

- Users can **document their findings on the fly** as they work in their jupyter notebook. 

- User can also **compare** the different performance metrics of the **supervised ML algorithm** of all the experiments.

- **Visualize** computation power(GPU and RAM),time taken 

- Users can **share their experiments and analysis** with their team via a shared folder or they could copy the entire experiment older in their local. Their team needs to pip install the application and mention the absolute path of the experiment folder.

- Since the application runs in the local, it is **more secure**.


## What this app can do

- This application is created to **document findings in analysis**, **ML experiments and track supervised ML experiments**.

- The documentation can be done easily from the jupyter notebook while working on it without having to cleaning/creating a notebook for **documenting the analysis/findings**. Users can document their findings on the fly and can later add more points from the flask app.

- All the above could be done by a single click using jupyter extensions.

- Compare the performance metrics **(accuracy,recall.precision,f1 score)** of the different supervised ML algorithms

- **Compare** the **computation power** and **execution time** of each alorithms used in the experiments.

- **Download** the each document separately. 

## What this app can't do

- Unlike other tools like weights and biases, MLflow etc this app can't track all the metrics of a ML algorithm.


## Who can use this app

- Data scientist,data analyst and machine learning engineer.


- Users can record the memory consumption, save the performance metrics for each experiment. A comparison chart is created like below so that users can see and know what's best for them. These info are displayed in the **Summary page**


- In the experiment page,**memory consumption over time**, **training performance**,**confusion matrix** and **documents** are displayed.


<h1 style="text-align:center;">How to use it</h1>

- Users need to define the **absolute path of the folder** that would contain all the experiments. The path must be stored in a variable named **EXP_PATH**.

`Eg: EXP_PATH="D:/experiment_folder/experiment2"`

- Then, click the **create experiment** button to create the experiment directory.

- The above steps are necessary for the application to work.

# Extensions

## Monitor memory consumption and execution time

- To start recording the memory consumption of an algorithm, just click **record memory** button.To stop recording the memory consumption, insert **monitor.stop()** where the algorithm ends.

`Eg: train_NN():
        .......
        .......
        return model
     model=train_NN()
     monitor.stop()`

- Along with memory recording, **time** is also started. Hence, it is better to start recording the memory when the code is ready to execute.


--------------------------------------------------------------------------------------------------------------------------------

## Save dictionary

- Save predictions as json. Users needs to store the y_true and y_pred_proba as dictionary.

**Command**: dict variable,file_type,file_path_to_store

   - Eg: `pred_dict,prediction,./experiment2/`

--------------------------------------------------------------------------------------------------------------------------------

# Note taking features

## Open note

- When users click **open note** button, a text editor is created in the jupyter notebook to add notes about the plots or about anything.

- User needs to manually save the plot to the **plots** folder.Since the **EXP_PATH** is already defined, we can use f string

`Eg: f"{EXP_PATH}/plots/plot_img.jpg"`

### Save note

- Click **save note** when users wants to save a note about a plot. Users can save plots and their interpretation about the plots to the flask app.

- User needs to define the file name a empty cell and the click **save note**. The file name should be same as the file name of the plot image so that the note can be tagged to the plot image.

`Eg:plot_img.txt`.

### Add to app

- This is used to add notes from jupyter notebook to the document in the flask application.

- Open a note. Write your thoughts in the text editor. Click **add to app** button only when you need to add notes to the document.



--------------------------------------------------------------------------------------------------------------------------------

## Experiment application

- All the results saved are displayed in the application. Click the **experiment app** to open the application that has all the documents and tracked metrics. 

- Users can **create many number of documents** in the flask application and **download** them as html.

