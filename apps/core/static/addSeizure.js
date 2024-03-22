/* Send request to Django Rest Framework (DRF) API to add a seizure. */
function addSeizure(csrfToken) {

    if (confirm("Are you sure that you want to add a seizure?")) {
        navigator.geolocation.getCurrentPosition((position) => {

            // Build the new seizure JSON.
            const newSeizure = JSON.stringify({
                "timestamp": new Date(),
                "device_name": "Browser",
                "device_type": "Browser",
                "ssid": null,
                "altitude": null,
                "latitude": position.coords.latitude,
                "longitude": position.coords.longitude,
                "address": null,
                "battery": null,
                "brightness": null,
                "volume": null,
            });

            // POST JSON request to API to add seizure, with CSRF token.
            const xhr = new XMLHttpRequest();
            xhr.open("POST", "/api/seizures/");
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.setRequestHeader("X-CSRFToken", csrfToken);

            // Show alert upon successful seizure addition, and reload.
            xhr.onreadystatechange = () => {
                if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 201) {
                    window.alert(`Seizure added.`);
                };
            };
            xhr.send(newSeizure);
            window.location.reload();
        });
    };
};
