/* Seizure JavaScript class. */

const Seizure = class {

    constructor(seizure) {

        // Parse seizure fields.
        this.when = new Date(seizure.pk);
        this.titleDate = this.when.toLocaleTimeString("en-us", {
            weekday: "short",
            year: "numeric",
            month: "short",
            day: "numeric",
            timeZoneName: "short"
        });
        this.verboseDate = this.when.toLocaleTimeString("en-us", {
            weekday: "long",
            year: "numeric",
            month: "long",
            day: "numeric",
            timeZoneName: "short"
        });
        this.unixTime = this.id = this.rowId = this.DT_RowId = this.when.getTime();

        this.deviceName = seizure.fields.device_name;
        this.deviceType = seizure.fields.device_type;
        this.deviceIcon = deviceIcons[this.deviceType];
        this.deviceLabel = `${this.deviceIcon} ${this.deviceName}`;

        this.latitude = seizure.fields.latitude;
        this.longitude = seizure.fields.longitude;

        this.address = null;
        if (seizure.fields.address) {
            this.address = seizure.fields.address.replace(/\n/g, ", ");
        }

        this.altitude = null;
        if (seizure.fields.altitude) {
            this.altitude = seizure.fields.altitude;
        }

        this.battery = null;
        if (seizure.fields.battery) {
            this.battery = seizure.fields.battery;
        }

        this.brightness = null;
        if (seizure.fields.brightness) {
            this.brightness = seizure.fields.brightness * 100;
        }

        this.volume = null;
        if (seizure.fields.volume) {
            this.volume = seizure.fields.volume * 100;
        }

        this.ssid = seizure.fields.ssid;

    };
};
