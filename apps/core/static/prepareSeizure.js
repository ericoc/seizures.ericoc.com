/* Prepare and handle adding a seizure. */
function prepareSeizure(csrfToken) {

    // Change the add button to a spinner.
    const addSpan = document.getElementById("add-span");
    addSpan.classList.remove("bi");
    addSpan.classList.remove("bi-plus-lg");
    addSpan.classList.add("spinner-grow");
    addSpan.classList.add("spinner-grow-sm");
    addSpan.role = "status";

    // Add the seizure using the CSRF token.
    const added = addSeizure(csrfToken);

    // Successfully adding a seizure reloads the page; this does not matter.
    if (added === true) {
        addSpan.classList.remove("spinner-grow");
        addSpan.classList.remove("spinner-grow-sm");
        addSpan.classList.add("bi");
        addSpan.classList.add("bi-check-lg");
    };
};
