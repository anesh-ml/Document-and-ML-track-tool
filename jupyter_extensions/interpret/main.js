'use strict';
define([
    'base/js/namespace',
    'base/js/events'
], function (Jupyter, events) {

    // Adds a cell above current cell (will be top if no cells)

    var interpret_func = function () {

        // getting variable and file
        let input_cell = Jupyter.notebook.get_selected_cell();
        let user_input = input_cell.get_text();

        Jupyter.notebook.insert_cell_below('code');
        Jupyter.notebook.select_next();
        let open_sheet_cell = Jupyter.notebook.get_selected_cell();
        open_sheet_cell.set_text(`lime_explainer(${user_input})`);
        open_sheet_cell.execute();
        open_sheet_cell.set_text("");

    }
    // Button to add default cell
    var defaultCellButton = function () {
        Jupyter.toolbar.add_buttons_group([
            Jupyter.keyboard_manager.actions.register({
                'help': 'open a sheet',
                'icon': 'fa-flask',
                'handler': interpret_func
            }, 'add-default-cell', 'Default cell')
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