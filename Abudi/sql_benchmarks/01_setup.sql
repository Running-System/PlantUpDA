-- PART 1: Table Creation
-- Run this first to set up the environment

-- 1. Enable TimescaleDB (if supported)
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- 2. Standard Heap Table
DROP TABLE IF EXISTS public.standard_telemetry_table;
CREATE TABLE public.standard_telemetry_table (
    id SERIAL PRIMARY KEY,
    device_id TEXT,
    moisture DOUBLE PRECISION,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. TimescaleDB Hypertable
DROP TABLE IF EXISTS public.telemetry_hypertable;
CREATE TABLE public.telemetry_hypertable (
    device_id TEXT,
    moisture DOUBLE PRECISION,
    time TIMESTAMPTZ NOT NULL
);

-- Convert Table to Hypertable (Partitioned by time)
SELECT create_hypertable('public.telemetry_hypertable', 'time', chunk_time_interval => INTERVAL '1 day');
