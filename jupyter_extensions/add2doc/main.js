'use strict';
define([
    'base/js/namespace',
    'base/js/events'
], function (Jupyter, events) {

    // Adds a cell above current cell (will be top if no cells)

    var add2doc = function () {

        // getting variable and file
        let input_cell = Jupyter.notebook.get_selected_cell();
        let user_input = input_cell.get_text();
        input_cell.set_text("")
        //Jupyter.notebook.insert_cell_below('code');
        //Jupyter.notebook.select_next();
        //let open_sheet_cell = Jupyter.notebook.get_selected_cell();
        input_cell.set_text(`from ml_track_tool.utils import add2doc
add2doc(EXP_PATH,text.value)`);
        input_cell.execute();
        input_cell.set_text(`${user_input}`);

    }
    // Button to add default cell
    var defaultCellButton = function () {
        Jupyter.toolbar.add_buttons_group([
            Jupyter.keyboard_manager.actions.register({
                'help': 'add to app',
                'icon': 'fa-plus-circle',
                'handler': add2doc
            }, 'add-2-doc-cell', 'add_2_doc cell')
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