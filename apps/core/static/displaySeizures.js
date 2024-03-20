/* Loop through each seizure, displaying them. */
async function displaySeizures(seizureData) {

    // Parse JSON containing seizure data.
    // Start seizure navigation list items.
    const seizures = Object.values(JSON.parse(JSON.parse(seizureData)));
    const seizureCount = seizures.length;

    // Loop through seizures, displaying each.
    for (const seizure of seizures) {
        await displaySeizure(seizure);
    };

    // Append the list of seizure links to the navigation card.
    seizuresCard.appendChild(seizureList);

    // Add a card footer of the seizure count.
    const cardFooter = document.createElement("h5");
    cardFooter.classList.add("card-footer");
    cardFooter.classList.add("text-secondary");
    cardFooter.classList.add("text-center");
    let countText = `${seizureCount.toLocaleString("en-US")} seizure`;
    if (seizureCount > 1) { countText += "s"; };
    document.title += ` ${countText}`;
    cardFooter.appendChild(document.createTextNode(countText));
    cardFooter.title = countText;
    seizuresCard.appendChild(cardFooter);

    // Set map bounds using minimum and maximum seizure coordinates.
    map.fitBounds([
        [Math.min(...latitudes), Math.min(...longitudes)],
        [Math.max(...latitudes), Math.max(...longitudes)]
    ]);

    // Open popup for marker if referenced by URL anchor.
    const anchor = String(window.location.hash).split('#')[1];
    if (anchor) {
        console.log(anchor);
        const marker = markers[anchor];
        console.log(marker);
        if (marker) { marker.openPopup(); };
    };

    // Open popup if single marker.
    if (seizureCount === 1) {
        markers[Object.keys(markers)[0]].openPopup();
    };

};
