--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3 (Ubuntu 15.3-1.pgdg22.04+1)
-- Dumped by pg_dump version 15.3 (Ubuntu 15.3-1.pgdg22.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: seizures; Type: TABLE; Schema: public; Owner: seizures
--

CREATE TABLE public.seizures (
    "timestamp" timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    device_name character varying(32)[] NOT NULL,
    device_type character varying(32)[] NOT NULL,
    ip_address inet NOT NULL,
    ssid character varying(32),
    altitude numeric(20,15),
    latitude numeric(20,15) NOT NULL,
    longitude numeric(20,15) NOT NULL
);


ALTER TABLE public.seizures OWNER TO seizures;

--
-- Name: seizures seizures_pkey; Type: CONSTRAINT; Schema: public; Owner: seizures
--

ALTER TABLE ONLY public.seizures
    ADD CONSTRAINT seizures_pkey PRIMARY KEY ("timestamp");


--
-- PostgreSQL database dump complete
--
