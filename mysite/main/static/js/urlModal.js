/*
    Codebook Variable Reorder

    Included in myProjectsTabs/codeUnit.html
    Handles fetching URLs from unit text
    Link passed to a pop-up warning modal
*/

// Converts plain URLs to modal-triggering anchor tags
function linkify(str) {
    return str.replace(/(<a href=")?((https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)))(">(.*)<\/a>)?/gi, function () {
        var url = arguments[2];
        var displayText = arguments[7] || arguments[2];
        return '<a type="button" class="modal-link" data-bs-toggle="modal" data-bs-target="#externalLinkModal" data-url="' + url + '" data-display-text="' + displayText + '">' + displayText + '</a>';
    });
}

$(document).ready(function () {
    // Only apply linkify to user-facing tab content, not all divs
    var targetDiv = $('#home-tab-pane');
    var data = targetDiv.html();
    var linkedContent = linkify(data);
    targetDiv.html(linkedContent);

    // Modal behavior for external links
    $('.modal-link').on('click', function () {
        var url = $(this).data('url');
        var displayText = $(this).data('display-text');
        var linkHtml = '<a href="' + url + '" target="_blank">' + displayText + '</a>';
        $('#externalLinkModal .modal-link-clickable').html(linkHtml);
    });

    // Auto-select radio input when its parent list item is clicked
    $('.list-group-item').on('click', function () {
        var input = $(this).find('.form-check-input');
        input.prop('checked', true);
    });

    // (Optional) Debug for tab change
    // const tabEl = document.querySelector('button[data-bs-toggle="tab"]');
    // tabEl?.addEventListener('shown.bs.tab', event => {
    //   console.log('Activated tab:', event.target);
    //   console.log('Previous tab:', event.relatedTarget);
    // });
});