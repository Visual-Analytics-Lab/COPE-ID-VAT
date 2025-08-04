/*
    Included in editVariable.html

    Initializes and handles Quill Editor (RTE)
    Moves value rows up/down
    Disables first Up and last Down button
    Hides/shows value table if there are values
    Adds/Deletes value row
    Listens for navigation buttons
*/

$(document).ready(function () {
    // ~~~ Quill Editor Initialization ~~~
    const initialComment = JSON.parse(document.getElementById('initial-description').textContent);

    const quill = new Quill('#editor', {
        modules: {
            syntax: true,
            toolbar: '#toolbar-container',
        },
        theme: 'snow',
    });

    if (initialComment.trim()) {
        quill.root.innerHTML = initialComment;
    }

    quill.on('text-change', function () {
        document.getElementById('variable-description').value = quill.root.innerHTML;
    });

    // Initial sync on page load
    document.getElementById('variable-description').value = quill.root.innerHTML;

    // ~~~ Table Row Manipulation ~~~
    function moveRowUp(button) {
        const row = button.closest("tr");
        const previousRow = row.previousElementSibling;

        if (previousRow) {
            row.parentNode.insertBefore(row, previousRow);
            refreshButtons();
        }
    }

    function moveRowDwn(button) {
        const row = button.closest("tr");
        const nextRow = row.nextElementSibling;

        if (nextRow) {
            row.parentNode.insertBefore(nextRow, row);
            refreshButtons();
        }
    }

    // Get comment select dropdown
    const variableComment = document.getElementById('variable-comment')

    function showValueTable() {
        const noVals = document.getElementById("no-vals");
        noVals.style.display = "none";
        const valTable = document.getElementById("val-table");
        valTable.style.display = 'block';
        variableComment.value = 'variable-comment-no';
        variableComment.disabled = false;
    }

    function hideValueTable() {
        const valTable = document.getElementById("val-table");
        valTable.style.display = 'none';
        const noVals = document.getElementById("no-vals");
        noVals.style.display = "block";
        variableComment.value = 'variable-comment-yes';
        variableComment.disabled = true;
    }

    function refreshButtons() {
        const rows = document.querySelectorAll("tbody tr");

        const numRows = rows.length;

        if (numRows == 0) {
            hideValueTable();
        }
        else {
            showValueTable();
        }

        rows.forEach((row, index) => {
            const upBtn = row.querySelector(".btn-up");
            const downBtn = row.querySelector(".btn-down");

            // Disable both by default
            upBtn.disabled = false;
            downBtn.disabled = false;

            // Disable Up on first row
            if (index === 0) upBtn.disabled = true;

            // Disable Down on last row
            if (index === rows.length - 1) downBtn.disabled = true;
        });
    }

    window.moveRowUp = moveRowUp;
    window.moveRowDwn = moveRowDwn;

    refreshButtons();

    // ~~~ Add & Delete Value Row ~~~
    // Listen for add button click
    $('#add-btn').on('click', function () {
        // Populate html for new row
        const newValue =
            `<tr>
          <td style="width: 5%;"><input type="number" class="form-control validate-field" name="value[]" placeholder="Value" aria-label="Variable value input"></td>
          <td style="width: 20;"><input type="text" class="form-control"name="label[]" type="text" placeholder="Label" aria-label="Variable label input"></td>
          <td style="width: 10%;"><input type="text" class="form-control" name="eg[]" placeholder="Example" aria-label="Variable example input"></td>
          <td>
            <div class="btn-group" role="group" aria-label="Up and Down">
              <button type="button" class="btn btn-secondary text-center btn-up" onclick="moveRowUp(this)"><i class="bi bi-caret-up"></i></button>
              <button type="button" class="btn btn-secondary text-center btn-down" onclick="moveRowDwn(this)"><i class="bi bi-caret-down"></i></button>
            </div>
          </td>
          <td><a type="button" class="icon-link trash-hover py-2" id="delete-btn"><i class="bi bi-trash3"></i></a></td>
        </div>`;
        // Add new row to bottom of rows
        $('#value-rows').append(newValue);
        refreshButtons();
    });

    // Listen for delete button click
    $('#value-rows').on('click', '#delete-btn', function () {
        // Fetch nearest row and delete
        // console.log("delete clicked")
        $(this).closest('tr').remove();
        refreshButtons();
    });

     // ~~~ Navigation Buttons ~~~
    // Listen for cancel button click
    $('#cancel-btn').on('click', function () {
        // Clear all inputs fields in the first row
        $('#value-rows ul:first-child input').val('');

        // Remove all rows except the first one
        $('#value-rows ul:not(:first-child)').remove();
    });

    // Listen for return button click
    $('#return-btn').on('click', function () {
        // console.log("return");
        $('#edit-action').val('return');
    });

    // Listen for save button click
    $('#save-variable').on('click', function () {
        // console.log("save");
        $('#edit-action').val('save');
    });

    // Listen for cancel button click
    $('#cancel-variable').on('click', function () {
        // console.log("cancel");
        $('#edit-action').val('cancel');
    });

    // Listen for delete button click
    $('#delete-variable').on('click', function () {
        // console.log("delete");
        $('#delete-action').val('delete');
    });

    // Listen for previous button click
    $('#prev-btn').on('click', function () {
        // console.log("previous");
        $('#edit-action').val('previous');
    });

    // Listen for next button click
    $('#next-btn').on('click', function () {
        // console.log("next");
        $('#edit-action').val('next');
    });

    // ~~~ Variable Name Validation ~~~
    const pattern = /^[a-zA-Z@][a-zA-Z0-9@#\$,._]*[a-zA-Z0-9@#\$,._]?$/;
    const reservedKeywords = new Set(["ALL", "AND", "BY", "EQ", "GE", "GT", "LE", "LT", "NE", "NOT", "OR", "TO", "WITH",
        "S1", "E1", "C1", "NET", "SUB", "TN", "CALC"]);

    function validateInput(input) {
        if (input.type === 'text') {
            const value = input.value.toUpperCase();
            if (!pattern.test(value) || reservedKeywords.has(value)) {
                input.setCustomValidity("Invalid input or reserved keyword.");
                input.classList.add('is-invalid');
                // input.classList.remove('is-valid');
            } else {
                input.setCustomValidity("");
                // input.classList.add('is-valid');
                input.classList.remove('is-invalid');
            }
        } else if (input.type === 'number') {
            if (isNaN(input.value) || input.value.trim() === '') {
                input.setCustomValidity("Please enter a valid number.");
                // input.classList.add('is-invalid');
                input.classList.remove('is-valid');
            } else {
                input.setCustomValidity("");
                // input.classList.add('is-valid');
                input.classList.remove('is-invalid');
            }
        }
    }

    $('.needs-validation').on('submit', function (event) {
        const form = this;
        let isValid = true;

        $('.validate-field').each(function () {
            validateInput(this);
            if (!this.checkValidity()) {
                isValid = false;
            }
        });

        if (!isValid) {
            event.preventDefault();
            event.stopPropagation();
        }

        $(this).addClass('was-validated');
    });

    $('.validate-field').on('input', function () {
        validateInput(this);
    });
});
