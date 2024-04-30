/* Send request to Django Rest Framework (DRF) API to add a seizure. */
function prepareSeizure(csrfToken) {

    const addSpan = document.getElementById("add-span");
    addSpan.classList.remove("bi");
    addSpan.classList.remove("bi-plus-lg");
    addSpan.classList.add("spinner-grow");
    addSpan.classList.add("spinner-grow-sm");
    addSpan.role = "status";

    const added = addSeizure(csrfToken);

    if (added === true) {
        addSpan.classList.remove("spinner-grow");
        addSpan.classList.remove("spinner-grow-sm");
        addSpan.classList.add("bi");
        addSpan.classList.add("bi-check-lg");
    };
};
