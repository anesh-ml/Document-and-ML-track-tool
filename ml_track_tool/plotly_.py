import plotly
import plotly.express as px
import plotly.subplots as sp


class px_utils():
    def __init__(self,fig):
        self.fig=fig if type(fig)=='list' else fig
        
    def make_subplot(self,subplots_titles,rows,cols,axis_titles,plot_title,legend_names,showlegend=True,width=None,height=None):
        '''
        Function to create subplots in plotly express
        input: 
            self.fig (iterables)
            subplot_title (iterables)
            rows (num of rows in subplot)
            cols (num of columns in subplot)
            axis_titles (iterables)
            plot_title: Title of the subplot
            width,height: width and height of the subplot

        usage example:
            subplot_px([fig,fig2],("temp","poll count"),1,2,[["temp","time"]],"Subplot express",900,600)
        '''
        if type(self.fig)!='list':
            fig_dict={}
            row=1
            col=1
            for i,f in enumerate(self.fig):
                for trace in range(len(f["data"])):
                    f['data'][0]['name']=legend_names[i]
                    f['data'][0]['showlegend']=showlegend
                    fig_dict[f"fig_{i}"]=f["data"][trace]
            this_figure = sp.make_subplots(rows=rows, cols=cols,subplot_titles=subplots_titles) 
            for traces in fig_dict.values():
                if (rows*cols>len(self.fig)):
                    this_figure.append_trace(traces, row=row, col=col)
                    '''
                    Assigns row and column for each plot.
                    '''
                    if col==cols:
                        row+=1
                        col=1
                        continue
                    col+=1
                else:
                    raise ValueError("number of subplot grids created is less than total figures.Check the row and col")
            '''
            setting axis titles
            '''
            i=1
            for ax_title in axis_titles:
                if i==1:
                    this_figure.layout[f'xaxis']['title']['text']=ax_title[0]
                    this_figure.layout[f'yaxis']['title']['text']=ax_title[1]
                else:
                    this_figure.layout[f'xaxis{i}']['title']['text']=ax_title[0]
                    this_figure.layout[f'yaxis{i}']['title']['text']=ax_title[1]
                i+=1
            this_figure.layout['title']['text']=plot_title
            if((height is not None)&(width is not None)):
                this_figure.update_layout(autosize=False,width=width,height=height)
        else:
            raise ValueError("input is not list of figures.")
        return this_figure

    def set_axis_title(self,axis_title):
        if(type(axis_title)!='list'):
            self.fig.layout['xaxis']['title']['text']=axis_title[0]
            self.fig.layout['yaxis']['title']['text']=axis_title[1]
        else:
            raise ValueError("input is not list of axis titles")
        return self.fig

    def set_plot_title(self,title):
        self.fig.layout.legend.title.text=title
        return self.fig
    
    def set_legend_name(self,legend_name):
        self.fig['data'][0]['name']=legend_name
        return self.fig