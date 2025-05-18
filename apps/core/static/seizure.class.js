/* Seizure JavaScript class. */
const Seizure = class {

    constructor(seizure) {

        // Parse seizure fields.
        this.when = new Date(seizure.pk)
        this.titleDate = this.when.toLocaleTimeString("en-us", {
            weekday: "short",
            year: "numeric",
            month: "short",
            day: "numeric",
            timeZoneName: "short"
        })
        this.verboseDate = this.when.toLocaleTimeString("en-us", {
            weekday: "long",
            year: "numeric",
            month: "long",
            day: "numeric",
            timeZoneName: "short"
        })
        this.unixTime = this.id = this.rowId = this.DT_RowId = this.when.getTime()

        this.deviceName = seizure.fields.device_name
        this.deviceType = seizure.fields.device_type
        this.deviceIcon = deviceIcons[this.deviceType]
        this.deviceLabel = `${this.deviceIcon} ${this.deviceName}`

        this.latitude = seizure.fields.latitude
        this.longitude = seizure.fields.longitude
        this.address = seizure.fields.address
        if (this.address && this.address.includes("\n")) {
            this.address = this.address.replace(/\n/g, ", ")
        }
        this.altitude = seizure.fields.altitude

        this.battery = seizure.fields.battery

        this.brightness = seizure.fields.brightness
        if (this.brightness && this.brightness > 0) {
            this.brightness = this.brightness * 100
        }

        this.volume = seizure.fields.volume
        if (this.volume && this.volume > 0) {
            this.volume = this.volume * 100
        }

        this.ssid = seizure.fields.ssid

    }
}

// Base Google Maps URL.
const gmapsURL = "https://www.google.com/maps/search/?api=1&query="
