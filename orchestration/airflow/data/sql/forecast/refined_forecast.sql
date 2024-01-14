CREATE OR REPLACE TABLE `estudos-410923.refined_DNC.refined_forecast`
AS
SELECT 
c.name                                                AS city,
  SPLIT(CAST(f.hour AS STRING), ':')[SAFE_OFFSET(0)]  AS hour,
  f.temperature,
  f.humidity,
  f.precipitation
FROM DNC.forecast f
JOIN DNC.city c
 ON f.city = c.id
ORDER BY c.name, f.hour, f.temperature, f.humidity, f.precipitation;