/* Seizure JavaScript class. */

const Seizure = class {

    constructor(seizure) {

        // Parse seizure fields.
        this.date = new Date(seizure.pk);
        this.titleDate = this.date.toLocaleTimeString("en-us", {
            weekday: "short",
            year: "numeric",
            month: "short",
            day: "numeric",
            timeZoneName: "short"
        });
        this.unixTime = this.date.getTime();

        this.deviceName = seizure.fields.device_name;
        this.deviceType = seizure.fields.device_type;
        this.deviceIcon = this.icon = deviceIcons[this.deviceType]
        this.deviceText = `${this.deviceIcon} ${this.deviceName}`

        this.address = null;
        if (seizure.fields.address) {
            this.address = seizure.fields.address.replace(/\n/g, ", ");
        };

        this.altitude = null;
        if (seizure.fields.altitude) {
            this.altitude = parseFloat(seizure.fields.altitude).toFixed(2);
        };

        this.latitude = seizure.fields.latitude
        this.longitude = seizure.fields.longitude;
        this.coordinates = `${this.latitude}, ${this.longitude}`;
        this.mapURL = `<a href="${gmapsURL}${seizure.fields.latitude},${seizure.fields.longitude}" target="_blank" title="Google Maps: ${this.coordinates}}">${this.coordinates}</a>`;

        this.battery = null;
        if (seizure.fields.battery) {
            this.battery = parseFloat(seizure.fields.battery).toFixed(2);
        };

        this.brightness = null;
        if (seizure.fields.brightness) {
            this.brightness = parseFloat(seizure.fields.brightness * 100).toFixed(2);
        };

        this.volume = null;
        if (seizure.fields.volume) {
            this.volume = parseFloat(seizure.fields.volume * 100).toFixed(2);
        };

        this.ssid = null;
        if (seizure.fields.ssid) {
            this.ssid = seizure.fields.ssid;
        };

    };
};
