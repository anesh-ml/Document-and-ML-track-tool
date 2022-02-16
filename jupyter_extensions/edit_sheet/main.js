'use strict';
define([
    'base/js/namespace',
    'base/js/events'
], function (Jupyter, events) {

    // Adds a cell above current cell (will be top if no cells)

    var edit_func = function () {

        // getting variable and file
        let input_cell = Jupyter.notebook.get_selected_cell();
        let user_input = input_cell.get_text();
        input_cell.set_text(``);
        //Jupyter.notebook.insert_cell_below('code');
        //Jupyter.notebook.select_next();
        //let edit_cell = Jupyter.notebook.get_selected_cell();
        let op = user_input.split(" ")[0]
        let arg_ = user_input.split(" ")[1]
        if (op == "filter") {
            input_cell.set_text(`from ml_track_tool.edit_sheet import filter_
filtered_sheet=filter_(sheet,${arg_})
filtered_sheet`);
        }
        else if (op == "create_col") {
            input_cell.set_text(`from ml_track_tool.edit_sheet import create_column
sheet=create_column(${arg_},sheet)
sheet`);
        }

        input_cell.execute();
        input_cell.set_text(`${user_input}`);

    }
    // Button to add default cell
    var defaultCellButton = function () {
        Jupyter.toolbar.add_buttons_group([
            Jupyter.keyboard_manager.actions.register({
                'help': 'edit sheet',
                'icon': 'fa-pencil-square-o',
                'handler': edit_func
            }, 'edit-cell', 'edit cell')
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