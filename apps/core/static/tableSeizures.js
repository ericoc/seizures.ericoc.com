/* Loop through each seizure, displaying them. */
async function tableSeizures(seizures) {

    // Loop through seizures, displaying each.
    for (const seizureData of seizures) {
        await tableSeizure(seizureData);
    };

    // Append the list of seizure links to the navigation card.
    seizuresCard.appendChild(seizureList);

    // Add a card footer of the seizure count.
    const seizureCount = seizures.length;
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
        console.log(anchor);
    };

    // Log if single marker.
    if (seizureCount === 1) {
        // console.log(markers[Object.keys(markers)[0]]);
        console.log('Only one seizure.');
        console.log(seizures);
    };

};
