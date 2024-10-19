const weightInputs = document.querySelectorAll('.weight');
const timeInputs = document.querySelectorAll('.exercise-time');
const listSelect = document.getElementById('exercise-select');

// Initially hide the time inputs and the select list
timeInputs.forEach(timeInput => timeInput.classList.add('hidden'));
listSelect.classList.add('hidden');

// Loop through all weight inputs
weightInputs.forEach(weightInput => {
    weightInput.addEventListener('keypress', (event) => {
        // Check if the Enter key is pressed
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent form submission
            // Check if the current weight input has a value
            if (weightInput.value) {
                // Show the time inputs and the select list
                timeInputs.forEach(timeInput => timeInput.classList.remove('hidden'));
                listSelect.classList.remove('hidden');
            }
        }
    });
});
