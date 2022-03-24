'use strict';
define([
    'base/js/namespace',
    'base/js/events'
], function (Jupyter, events) {

    // Adds a cell above current cell (will be top if no cells)

    var save_note = function () {

        // getting variable and file
        let input_cell = Jupyter.notebook.get_selected_cell();
        let user_input = input_cell.get_text();
        input_cell.set_text("")
        //Jupyter.notebook.insert_cell_below('code');
        //Jupyter.notebook.select_next();
        //let open_sheet_cell = Jupyter.notebook.get_selected_cell();
        input_cell.set_text(`with open(f"{EXP_PATH}/plots/${user_input}", "w") as file1:
    file1.write(text.value)`);
        input_cell.execute();
        input_cell.set_text(`${user_input}`);

    }
    // Button to add default cell
    var defaultCellButton = function () {
        Jupyter.toolbar.add_buttons_group([
            Jupyter.keyboard_manager.actions.register({
                'help': 'save note',
                'icon': 'fa-floppy-o',
                'handler': save_note
            }, 'save-note-cell', 'save_note cell')
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