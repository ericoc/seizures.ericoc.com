-- Table: public.seizures

-- DROP TABLE IF EXISTS public.seizures;

CREATE TABLE IF NOT EXISTS public.seizures
(
    "timestamp" timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    device_name character varying(32) COLLATE pg_catalog."default" NOT NULL,
    device_type character varying(32) COLLATE pg_catalog."default" NOT NULL,
    ssid character varying(32) COLLATE pg_catalog."default",
    altitude numeric(20,15),
    latitude numeric(20,15) NOT NULL,
    longitude numeric(20,15) NOT NULL,
    address text COLLATE pg_catalog."default",
    battery numeric(20,15),
    brightness numeric(20,15),
    volume numeric(20,15),
    CONSTRAINT seizures_pkey PRIMARY KEY ("timestamp")
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.seizures
    OWNER to seizures;
