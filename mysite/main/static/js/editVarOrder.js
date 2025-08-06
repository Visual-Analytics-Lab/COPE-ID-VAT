/*
    Codebook Variable Reorder

    Included in myProjectsTabs/codebook.html
    Handles moving table rows up/down
    Disables top/bottom up/down buttons
    Saves variable IDs for form submission
*/

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

function refreshButtons() {
    const table = document.getElementById("orderVariables");

    // Get all <tr> in the tbody of this specific table
    const rows = table.querySelectorAll("tbody tr");

    const editableRows = [];

    rows.forEach((row) => {
        const upBtn = row.querySelector(".btn-up");
        const downBtn = row.querySelector(".btn-down");

        // Only include rows that have both buttons
        if (upBtn && downBtn) {
            editableRows.push({ upBtn, downBtn });
        }
    });

    // Reset and disable buttons accordingly
    editableRows.forEach(({ upBtn, downBtn }, index) => {
        upBtn.disabled = false;
        downBtn.disabled = false;

        if (index === 0) upBtn.disabled = true;
        if (index === editableRows.length - 1) downBtn.disabled = true;
    });
}

// Ensure buttons are set correctly after DOM load
document.addEventListener("DOMContentLoaded", refreshButtons);

function submitReorder() {
    // Get variable order modal
    const modalTable = document.querySelector("#editVarOrder tbody");

    // Get table rows
    const rows = modalTable.querySelectorAll("tr");

    // Intialize array to store variable IDs
    const ids = [];

    // Add IDs to array
    rows.forEach(row => {
        const variableId = row.getAttribute("data-variable-id");
        if (variableId) {
            ids.push(variableId);
        }
    });

    // Store variable IDs for form submit
    document.getElementById("reordered-ids").value = ids.join(",");
    document.getElementById("reorder-form").submit();
}