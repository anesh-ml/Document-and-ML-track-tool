import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix,precision_score,recall_score,f1_score,accuracy_score
from matplotlib.pyplot import figure
import scikitplot as skplt
import tensorflow as tf



def plot_metric(y_true,y_pred_proba):
    ''' y_true shape:(n_samples)
    
        y_pred shape: (n_samples,n_classes)
    '''
    y_pred=tf.argmax(y_pred_proba,axis=1)
    precision=precision_score(y_true,y_pred,average='binary')
    recall=recall_score(y_true,y_pred,average='binary')
    f1score=f1_score(y_true,y_pred)
    accuracy=accuracy_score(y_true,y_pred)

    metrics=f'''
            accuracy:{round(accuracy,2)}% 

            F1_score:{round(f1score,2)}%

            Precision:{round(precision,2)}%

            Recall: {round(recall,2)}%'''

    fig, ax = plt.subplots(1, 2, sharex='col', sharey='row',figsize=(16,7))

    ax[0].text(0.15,0.3,metrics,clip_on=True,fontdict={"size":20})
    ax[0].axis('off')


    skplt.metrics.plot_roc(y_true, y_pred_proba,ax=ax[1])
    plt.show()