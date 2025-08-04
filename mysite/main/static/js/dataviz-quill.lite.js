/*
    Quill editor with limited functionality

    Include {{ <variable>|default:""|json_script:"initial-data" }} in the HTML file
    Populates form with "initial-data" on document ready
    Django gets "about" from "quill-form" on form submit
    References the text editor with ID "editor"
*/

$(document).ready(function () {
    // Get and parse existing data for the form
    const initialdata = document.getElementById('initial-data');
    const rawHTML = initialdata ? JSON.parse(initialdata.textContent || '""') : "";

    // Included toolbar options
    const toolbarOptions = [
        [{ font: [false, 'bootstrap-sans', 'serif', 'monospace'] }, { size: ['small', false, 'large', 'huge'] }],
        ['bold', 'italic', 'underline', 'strike'],
        [{ color: [] }, { background: [] }],
        [{ list: 'ordered' }, { list: 'bullet' }, { indent: '-1' }, { indent: '+1' }],
        [{ direction: 'rtl' }, { align: [] }, 'link', 'clean']
    ];

    // Whitelist the explicit font options (Sans-Serif is implicit)
    const Font = Quill.import('formats/font');
    Font.whitelist = ['bootstrap-sans', 'serif', 'monospace'];
    Quill.register(Font, true);

    // Quill editor initialization
    const quill = new Quill('#editor', {
        modules: { toolbar: toolbarOptions },
        theme: 'snow'
    });

    // Convert raw HTML into Quill Delta
    if (rawHTML && rawHTML.trim()) {
        const quillDelta = (Quill.version.startsWith('1'))
            ? quill.clipboard.convert(rawHTML)               // Quill 1.x
            : quill.clipboard.convert({ html: rawHTML });    // Quill 2.x
        quill.setContents(quillDelta, 'silent');
    } else {
        quill.setContents([], 'silent'); // empty editor
    }

    // Track quill editor
    const form = document.querySelector('#quill-form');
    form.addEventListener('formdata', (event) => {
        // Append Quill content before submitting
        event.formData.append('about', quill.root.innerHTML);
    });

});
