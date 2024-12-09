// Defining variables
const csrfToken = document.querySelector('input[type="hidden"]').value;
const nextButton = document.querySelector('button');

// Attach 'blur' event handlers to all input fields excluding hidden elements
function addEventHandlerToInputs() {
    const inputElements = document.querySelectorAll('.input:not([type="hidden"])');
    inputElements.forEach(item => {
        item.addEventListener("blur", validateInputData);
    });
}

// Check input values for the 'is-success' class and enable nextButton if all are valid
function checkInputForValid() {
    const inputElements = document.querySelectorAll('.input:not([type="hidden"])');
    const allValid = Array.from(inputElements).every(element =>
        element.classList.contains('is-success')
    );
    nextButton.disabled = !allValid;
}

// Validate input data on blur event by sending POST data to the backend
async function validateInputData(event) {
    try {
        const inputElement = event.target;
        const queryPayload = new URLSearchParams({
            field_name: inputElement.name,
            field_value: inputElement.value,
            csrf_token: csrfToken
        }).toString();

        // Create a new request object
        const request = new Request('/validate', {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: queryPayload
        });

        // Fetch the response from the server
        const response = await fetch(request);
        if (!response.ok) {
            // Error handling: server does not respond with a 200 status code
            throw new Error(`Could not validate against server: ${response.status}`);
        } else {
            // Process the server response
            const serverResponseHTML = await response.text();
            const parser = new DOMParser();
            const newHTML = parser.parseFromString(serverResponseHTML, 'text/html').body.firstChild;

            // Replace the input element with the new HTML
            inputElement.replaceWith(newHTML);

            // Re-select the new element after replacement
            const updatedElement = document.querySelector(`[name="${inputElement.name}"]`);

            // Re-attach event listener
            updatedElement.addEventListener("blur", validateInputData);

            // Clear input data if the validation response indicates an error
            if (updatedElement.classList.contains('is-danger')) {
                updatedElement.value = "";
            }

            // Re-check validation for enabling the next button
            checkInputForValid();
        }
    } catch (error) {
        // Log error if request fails
        console.error(`Could not contact server: ${error}`);
    }
}

// Initialize the input event handlers
addEventHandlerToInputs();

