  // Step 1:
  const s1NextBtn = document.getElementById('step1Next');

  // Get project name
  const projectNameInput = document.getElementById('in-project-name');

  // Get n units
  const nUnitsInput = document.getElementById('in-n-units');

  // Step 2:
  const desiredUnitsSpan = document.getElementById('out-desired-units');
  const selectedUnitsSpan = document.getElementById('in-selected-units');

  // Step 3:

  // Step 4:
  // Get project name span
  const projectNameSpan = document.getElementById('out-project-name');
  const darwnSampleSpan = document.getElementById('out-drawn-sample');

  // Add an event listener to the button
  s1NextBtn.addEventListener('click', () => {
    // Get the current value of the input field
    const projectNameValue = projectNameInput.value;

    // Update the content of the span
    projectNameSpan.textContent = projectNameValue;

    // Get the current value of the input field
    const nUnitsValue = nUnitsInput.value;

    // Update the content of the span
    desiredUnitsSpan.textContent = nUnitsValue;
  });

  // Select the button using its ID
  const s2NextBtn = document.getElementById('step2Next');

  // Add an event listener to the button
  s2NextBtn.addEventListener('click', () => {
    // Get the current value of the input field
    const selectedUnitsValue = selectedUnitsSpan.value;

    // Update the content of the span
    darwnSampleSpan.textContent = selectedUnitsValue;
  });

    // Select the button using its ID
  const s3NextBtn = document.getElementById('step3Next');

  // Add an event listener to the button
  s3NextBtn.addEventListener('click', () => {
    // Get the current value of the input field
    const selectedUnitsValue = selectedUnitsSpan.value;

    // Update the content of the span
    darwnSampleSpan.textContent = selectedUnitsValue;
  });

  // Select all radio buttons with the name 'cluster-choice'
  const clusterOptions = document.querySelectorAll('input[name="cluster-choice"]');

  // Select the span where the selected cluster choice will be displayed
  const clusterChoiceSpan = document.getElementById('out-cluster-choice');

  // Function to update the cluster choice display
  function updateClusterChoice() {
    // Find the currently selected option
    let selectedValue = null;
    clusterOptions.forEach(option => {
      if (option.checked) {
        selectedValue = option.value; // Get the value of the selected radio button
      }
    });

    // Update the text content of the span
    clusterChoiceSpan.textContent = selectedValue ? selectedValue.charAt(0).toUpperCase() + selectedValue.slice(1) : "None selected";
  }

  // Initialize the display with the default selected option
  updateClusterChoice();

  // Add an event listener to update the display when the selection changes
  clusterOptions.forEach(option => {
    option.addEventListener('change', updateClusterChoice);
  });

  // Select all radio buttons with the name 'sample-pref'
  const sampleOptions = document.querySelectorAll('input[name="sample-pref"]');

  // Select the span where the selected sampling technique will be displayed
  const sampleTechSpan = document.getElementById('out-sample-tech');

  // Create a mapping object for the display text
  const samplingTechniqueMapping = {
    simple: "Simple Random Sample",
    systematic: "Systematic Random Sampling",
    chronologically: "Chronologically by unit post ID"
  };

  // Function to update the sampling technique display
  function updateSamplingTechnique() {
    // Find the currently selected option
    let selectedValue = null;
    sampleOptions.forEach(option => {
    if (option.checked) {
      selectedValue = option.value; // Get the value of the selected radio button
    }
  });

    // Update the text content of the span
    sampleTechSpan.textContent = selectedValue ? samplingTechniqueMapping[selectedValue] : "None selected";
  }

  // Initialize the display with the default selected option
  updateSamplingTechnique();

  // Add an event listener to update the display when the selection changes
  sampleOptions.forEach(option => {
    option.addEventListener('change', updateSamplingTechnique);
  });

  // Select all platform input fields
  const platformInputs = document.querySelectorAll('#platform1, #platform2, #platform3, #platform4, #platform5, #platform6, #platform7, #platform8, #platform9, #platform10');

  // Select the total field
  const selectedUnitsInput = document.getElementById('in-selected-units');

  // Function to calculate the total value
  function updateTotalUnits() {
    const nUnitsValue = nUnitsInput.value;
    let total = 0;

    // Sum up the values of all platform inputs
    platformInputs.forEach(input => {
      const value = parseInt(input.value) || 0; // Convert to number or use 0 if empty
      total += value;
    });

    // Update the total field
    selectedUnitsInput.value = total;

    if (total > nUnitsValue) {
    // Add the 'is-invalid' class
    selectedUnitsInput.classList.add('is-invalid');
    } else {
      // Remove the 'is-invalid' class
      selectedUnitsInput.classList.remove('is-invalid');
    }
  }

  // Add event listeners to all platform inputs
  platformInputs.forEach(input => {
    input.addEventListener('input', updateTotalUnits);
  });

  // Initialize the total field on page load
  updateTotalUnits();