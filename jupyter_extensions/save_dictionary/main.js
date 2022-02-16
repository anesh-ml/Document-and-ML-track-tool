'use strict';
define([
    'base/js/namespace',
    'base/js/events'
], function (Jupyter, events) {

    // Adds a cell above current cell (will be top if no cells)

    var save_dict_func = function () {

        // getting variable and file
        let input_cell = Jupyter.notebook.get_selected_cell();
        let user_input = input_cell.get_text();
        let user_input_list = user_input.split(",")
        let dict_ = user_input_list[0]
        let file_type = user_input_list[1]
        let file_path = user_input_list[2]
        //Jupyter.notebook.insert_cell_below('code');
        //Jupyter.notebook.select_next();
        //let open_sheet_cell = Jupyter.notebook.get_selected_cell();
        input_cell.set_text(`from ml_track_tool.utils import save_dict
save_dict(${dict_},"${file_type}", "${file_path}")`);
        input_cell.execute();
        input_cell.set_text(`${user_input}`);

    }
    // Button to add default cell
    var defaultCellButton = function () {
        Jupyter.toolbar.add_buttons_group([
            Jupyter.keyboard_manager.actions.register({
                'help': 'save dictionary',
                'icon': 'fa-cloud-download ',
                'handler': save_dict_func
            }, 'save-dict-cell', 'save_dict cell')
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