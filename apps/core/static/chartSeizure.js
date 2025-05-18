/* Parse, display, and chart a single seizure. */
function chartSeizure(seizureData) {

    // List device type icon, and link time.
    const seizure = new Seizure(seizureData)
    const listNode = document.createElement("li")
    listNode.classList.add("list-group-item")
    listNode.classList.add("list-group-item-action")
    listNode.classList.add("list-group-item-text")
    listNode.classList.add("small")
    listNode.classList.add("card-text")
    listNode.onclick = function() {
        window.location.href = `#${seizure.unixTime}`
    }

    const linkNode = document.createElement("a")
    linkNode.title = `${seizure.deviceIcon} ${seizure.titleDate}`
    linkNode.href = `#${seizure.unixTime}`
    linkNode.classList.add("seizure-link")
    linkNode.appendChild(document.createTextNode(seizure.titleDate))
    listNode.appendChild(document.createTextNode(seizure.deviceIcon))
    listNode.appendChild(linkNode)
    seizureList.appendChild(listNode)

    return seizure
}
