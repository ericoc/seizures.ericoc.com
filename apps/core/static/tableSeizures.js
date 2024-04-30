/* Loop through each seizure, displaying them. */
async function tableSeizures(seizureData) {

    // Parse JSON containing seizure data.
    // Start seizure navigation list items.
    const seizures = Object.values(JSON.parse(JSON.parse(seizureData)));
    const seizureCount = seizures.length;

    // Loop through seizures, displaying each.
    for (const seizure of seizures) {
        await tableSeizure(seizure);
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

    // Log if referenced by URL anchor.
    const anchor = String(window.location.hash).split('#')[1];
    if (anchor) {
        const marker = markers[anchor];
        console.log(marker);
    };

    // Log if single marker.
    if (seizureCount === 1) {
        console.log(markers[Object.keys(markers)[0]]);
    };

};
