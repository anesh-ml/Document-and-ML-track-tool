'use strict';
define([
    'base/js/namespace',
    'base/js/events'
], function (Jupyter, events) {

    // Adds a cell above current cell (will be top if no cells)

    var download_sheet_func = function () {

        // getting variable and file
        let input_cell = Jupyter.notebook.get_selected_cell();
        let user_input = input_cell.get_text();

        //Jupyter.notebook.insert_cell_below('code');
        //Jupyter.notebook.select_next();
        //let download_sheet_cell = Jupyter.notebook.get_selected_cell();
        input_cell.set_text(`from ml_track_tool.utils import Variable_data
import ipysheet
from ml_track_tool.OpenSheet import download_sheet
import ml_track_tool
var_data=Variable_data(get_ipython())
all_var=var_data.get_value()
df=ipysheet.to_dataframe(sheet)
variables=[x for col in df.columns for x in df[col].str.findall(r"\@(.*)").values.tolist()  if len(x)!=0 ]
var_sheet=[x[0] for x in variables if len(x)!=0]
if any(list(set(var_sheet).intersection(all_var))):
    
    df.replace({f"@{x}":eval(x) for x in all_var if x in var_sheet},inplace=True)
    sheet=ipysheet.from_dataframe(df)
    download_sheet(sheet,${user_input},os.path.dirname(ml_track_tool.__file__))
else:
    download_sheet(sheet,${user_input},os.path.dirname(ml_track_tool.__file__))
var_data.close()`);
        input_cell.execute();
        input_cell.set_text(`${user_input}`);

    }
    // Button to add default cell
    var defaultCellButton = function () {
        Jupyter.toolbar.add_buttons_group([
            Jupyter.keyboard_manager.actions.register({
                'help': 'download the sheet',
                'icon': 'fa-download',
                'handler': download_sheet_func
            }, 'download-sheet-cell', 'download-sheet')
        ])
    }
    // Run on start
    function load_ipython_extension() {
        // Add a default cell if there are no cells

        defaultCellButton();
    }
    return {
        load_ipython_extension: load_ipython_extension
    };
});