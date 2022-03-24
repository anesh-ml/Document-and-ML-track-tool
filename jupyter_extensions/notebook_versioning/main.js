'use strict';
define([
    'base/js/namespace',
    'base/js/events'
], function (Jupyter, events) {

    // Adds a cell above current cell (will be top if no cells)

    var copy_notebook_func = function () {

        // getting variable and file
        let input_cell = Jupyter.notebook.get_selected_cell();
        let user_input = input_cell.get_text();
        input_cell.set_text("");
        let notebook_name = Jupyter.notebook.notebook_name
        //Jupyter.notebook.insert_cell_below('code');
        //Jupyter.notebook.select_next();
        //let open_sheet_cell = Jupyter.notebook.get_selected_cell();
        //console.log(`sheet=open_sheet(${user_input}) sheet`)
        input_cell.set_text(`from ml_track_tool.utils import copy
copy("${notebook_name}",${user_input})`);
        input_cell.execute();
        input_cell.set_text(`${user_input}`);

    }
    // Button to add default cell
    var defaultCellButton = function () {
        Jupyter.toolbar.add_buttons_group([
            Jupyter.keyboard_manager.actions.register({
                'help': 'Version notebook',
                'icon': 'fa-cloud-download',
                'handler': copy_notebook_func
            }, 'copy-notebook', 'copy notebook')
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