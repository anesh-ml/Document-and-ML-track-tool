'use strict';
define([
    'base/js/namespace',
    'base/js/events'
], function (Jupyter, events) {

    // Adds a cell above current cell (will be top if no cells)

    var add_cell = function () {

        // getting variable and file
        let input_cell = Jupyter.notebook.get_selected_cell();
        let user_input = input_cell.get_text();

        let variable = user_input.split(",")[0];
        let file = user_input.split(",")[1];
        Jupyter.notebook.insert_cell_below('code');
        Jupyter.notebook.select_next();
        let get_data_cell = Jupyter.notebook.get_selected_cell();
        get_data_cell.set_text(`var,file="${variable}","${file}"`);
        get_data_cell.execute();
        get_data_cell.set_text("");
        get_data_cell.set_text(`inspector = utils.save_file(get_ipython())
values=inspector.get_value()
out=[eval(x) for x in values if  ((type(eval(x)).__name__=="DataFrame")&(x==var)) ]
inspector.save_data(out[0],file)
inspector.close()`);

        get_data_cell.execute();
        get_data_cell.set_text("");




    }
    // Button to add default cell
    var defaultCellButton = function () {
        Jupyter.toolbar.add_buttons_group([
            Jupyter.keyboard_manager.actions.register({
                'help': 'Add default cell',
                'icon': 'fa-play-circle',
                'handler': add_cell
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