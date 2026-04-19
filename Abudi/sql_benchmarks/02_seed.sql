-- PART 2: Data Seeding
-- Generates 500,000 records for each table

-- Clean existing data
TRUNCATE public.standard_telemetry_table;
TRUNCATE public.telemetry_hypertable;

-- Seed Standard Table
INSERT INTO public.standard_telemetry_table (device_id, moisture, created_at)
SELECT 
    'PLANT_' || (floor(random() * 5)::text),
    30 + (random() * 40),
    NOW() - (i * interval '1 minute') 
FROM generate_series(1, 500000) s(i);

-- Seed Hypertable
INSERT INTO public.telemetry_hypertable (device_id, moisture, time)
SELECT 
    'PLANT_' || (floor(random() * 5)::text),
    30 + (random() * 40),
    NOW() - (i * interval '1 minute') 
FROM generate_series(1, 500000) s(i);

-- Perform Maintenance (Calculates statistics for more accurate EXPLAIN results)
ANALYZE public.standard_telemetry_table;
ANALYZE public.telemetry_hypertable;
