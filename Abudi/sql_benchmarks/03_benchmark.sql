CREATE OR REPLACE FUNCTION public.get_exact_benchmark_plan(tbl_type text)
RETURNS text AS $$
DECLARE
  plan_line text;
  full_plan text := '';
  sql_query text;
BEGIN
  IF tbl_type = 'standard' THEN
    -- Now both use the same 1-hour grouping logic
    sql_query := 'SELECT device_id, date_trunc(''hour'', created_at) AS bucket, AVG(moisture)
                  FROM public.standard_telemetry_table
                  WHERE created_at > NOW() - INTERVAL ''7 days''
                  GROUP BY bucket, device_id';
  ELSE
    sql_query := 'SELECT device_id, time_bucket(''1 hour'', time) AS bucket, AVG(moisture)
                  FROM public.telemetry_hypertable
                  WHERE time > NOW() - INTERVAL ''7 days''
                  GROUP BY bucket, device_id';
  END IF;

  FOR plan_line IN EXECUTE 'EXPLAIN (ANALYZE, FORMAT TEXT) ' || sql_query LOOP
    full_plan := full_plan || plan_line || chr(10);
  END LOOP;

  RETURN full_plan;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
