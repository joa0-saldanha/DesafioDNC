DELETE FROM `estudos-410923.DNC.traffic` t
WHERE EXTRACT(DATE FROM TIMESTAMP(t.departureTime)) < DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY);
