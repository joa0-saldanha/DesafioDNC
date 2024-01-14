CREATE OR REPLACE TABLE `estudos-410923.refined_DNC.refined_traffic`
AS
SELECT 
  o.name                                        as origin,
  d.name                                        as destination,
  CAST(t.lengthInMeters/1000 AS INTEGER)        as distanceKM,
  CAST(t.travelTimeInSeconds/60 AS INTEGER)     as distanceMinutes,
  CAST(t.trafficLengthInMeters/1000 AS INTEGER)      as trafficDelayKM,
  CAST(t.trafficDelayInSeconds/60 AS INTEGER)   as trafficDelayMinutes
FROM DNC.traffic t
LEFT JOIN DNC.route r
  ON t.route = r.id
LEFT JOIN DNC.city o 
  ON r.origin = o.id
LEFT JOIN DNC.city d 
  ON r.destination = d.id;