/* Parse, display, and map a single seizure. */
async function displaySeizure(seizure) {

    // Get seizure icon and parse timestamp.
    const deviceIcon = deviceIcons[seizure.fields.device_type];
    const jsDate = new Date(seizure.pk);
    const titleDate = jsDate.toLocaleTimeString(
        "en-us", {
            weekday: "short",
            year: "numeric",
            month: "short",
            day: "numeric",
            timeZoneName: "short"
        }
    );
    const unixTime = jsDate.getTime();

    // List device type icon, and link time to open map marker popup.
    const listNode = document.createElement("li");
    listNode.classList.add("list-group-item");
    listNode.classList.add("list-group-item-action");
    listNode.classList.add("list-group-item-text");
    listNode.classList.add("small");
    listNode.classList.add("card-text");
    listNode.onclick = function() {
        window.location.href = `#${unixTime}`;
        markers[unixTime].openPopup();
    };
    listNode.id = `${unixTime}`;

    const linkNode = document.createElement("a");
    linkNode.title = `${deviceIcon} ${titleDate}`;
    linkNode.href = `#${unixTime}`;
    linkNode.onclick = function() { markers[unixTime].openPopup(); };
    linkNode.appendChild(document.createTextNode(titleDate));

    listNode.appendChild(document.createTextNode(deviceIcon));
    listNode.appendChild(linkNode);
    seizureList.appendChild(listNode);

    // Append coordinates to arrays, for later maps bounds calculation.
    latitudes.push(Number(seizure.fields.latitude));
    longitudes.push(Number(seizure.fields.longitude));

    // Create a table to display within each marker popup.
    let contentString = '<table class="table table-bordered table-responsive table-rounded table-striped table-hover">';
    contentString += `<tr title="${deviceIcon} ${titleDate}">`;
    contentString += `<th scope="row" class="text-center fw-bold" colspan="2">${deviceIcon} <a href="#${unixTime}"><time datetime="${jsDate.toISOString()}">${titleDate}</a></th>`;
    contentString += "</tr>";

    // Address links to Google Maps.
    if (seizure.fields.address) {
        const addressParsed = seizure.fields.address.replace(/\n/g, ", ");
        contentString += `<tr title="Address: ${addressParsed}">`;
        contentString += '<td class="fw-bold">Address</td>';
        contentString += `<td><a href="${gmapsURL}${addressParsed}" target="_blank" title="Google Maps: ${addressParsed}">${addressParsed}</a></td>`;
        contentString += "</tr>";
    };

    // Altitude.
    if (seizure.fields.altitude) {
        const altitudeParsed = `${parseFloat(seizure.fields.altitude).toFixed(2)} ft`;
        contentString += `<tr title="Altitude: ${altitudeParsed}">`;
        contentString += `<td class="fw-bold">Altitude</td><td>${altitudeParsed}</td>`;
        contentString += "</tr>";
    };

    // Battery.
    if (seizure.fields.battery) {
        const batteryParsed = `${parseFloat(seizure.fields.battery).toFixed(2)}%`;
        contentString += `<tr title="Battery: ${batteryParsed}">`;
        contentString += `<td class="fw-bold">Battery</td><td>${batteryParsed}</td>`;
        contentString += "</tr>";
    };

    // Brightness.
    if (seizure.fields.brightness) {
        const brightnessParsed = `${parseFloat(seizure.fields.brightness*100).toFixed(2)}%`;
        contentString += `<tr title="Brightness: ${brightnessParsed}">`;
        contentString += `<td class="fw-bold">Brightness</td><td>${brightnessParsed}</td>`;
        contentString += "</tr>";
    };

    // GPS Coordinates link to Google Maps.
    contentString += `<tr title="Coordinates: ${seizure.fields.latitude}, ${seizure.fields.longitude}">`;
    contentString += '<td class="fw-bold">Coordinates</td>';
    contentString += `<td><a href="${gmapsURL}${seizure.fields.latitude},${seizure.fields.longitude}" target="_blank" title="Google Maps: ${seizure.fields.latitude}, ${seizure.fields.longitude}">${seizure.fields.latitude}, ${seizure.fields.longitude}</a></td>`;
    contentString += "</tr>";

    // Device.
    if (seizure.fields.device_name) {
        contentString += `<tr title="Device: ${deviceIcon} ${seizure.fields.device_name}">`;
        contentString += '<td class="fw-bold">Device</td>';
        contentString += `<td>${deviceIcon} ${seizure.fields.device_name}</a></td>`;
        contentString += "</tr>";
    };

    // SSID.
        if (seizure.fields.ssid) {
        contentString += `<tr title="SSID: ${seizure.fields.ssid}">`;
        contentString += '<td class="fw-bold">SSID</td>';
        contentString += `<td>${seizure.fields.ssid}</td>`;
        contentString += "</tr>";
    };

    // UTC date.
    const utcDate = jsDate.toUTCString();
    contentString += `<tr title="UTC: ${utcDate}">`;
    contentString += '<td class="fw-bold">UTC</td>';
    contentString += `<td><time datetime="${jsDate.toISOString()}">${utcDate}</time></td>`;
    contentString += "</tr>";

    // Volume.
    if (seizure.fields.volume) {
        const volumeParsed = `${parseFloat(seizure.fields.volume*100).toFixed(2)}%`;
        contentString += `<tr title="Volume: ${volumeParsed}">`;
        contentString += `<td class="fw-bold">Volume</td><td>${volumeParsed}</td>`;
        contentString += "</tr>";
    };

    // Finish marker table popup.
    contentString += "</table>";

    // Create map marker for each seizure.
    markers[unixTime] = L.marker([
        Number(seizure.fields.latitude),
        Number(seizure.fields.longitude)
    ]).addTo(map).bindPopup(contentString);
};
