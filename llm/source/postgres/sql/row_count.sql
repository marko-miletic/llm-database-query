SELECT table_name, row_count
FROM (
  SELECT relname AS table_name, n_live_tup AS row_count
  FROM pg_stat_user_tables
) s
ORDER BY table_name;