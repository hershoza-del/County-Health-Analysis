SELECT * FROM data.county_health_analysis;

SELECT COUNT(*) AS total_counties,
COUNT(blk_child_pov_rate) AS has_blk_pov,
SUM(CASE WHEN blk_child_pov_rate IS NOT NULL
AND whi_child_pov_rate IS NOT NULL THEN 1 ELSE 0 END) AS has_both_pov,
SUM(CASE WHEN blk_med_income IS NOT NULL
AND whi_med_income IS NOT NULL THEN 1 ELSE 0 END) AS has_both_income
FROM data.county_health_analysis;

SELECT ROUND(AVG(blk_child_pov_rate - whi_child_pov_rate), 2) AS avg_pov_gap
FROM data.county_health_analysis
WHERE blk_child_pov_rate IS NOT NULL AND whi_child_pov_rate IS NOT NULL;

SELECT SUM(CASE WHEN blk_child_pov_rate > whi_child_pov_rate THEN 1 ELSE 0 END) AS blk_higher,
SUM(CASE WHEN blk_child_pov_rate <= whi_child_pov_rate THEN 1 ELSE 0 END) AS blk_same_or_lower
FROM data.county_health_analysis
WHERE blk_child_pov_rate IS NOT NULL AND whi_child_pov_rate IS NOT NULL;

SELECT CASE WHEN rural_pct >= 50 THEN 'Mostly rural' ELSE 'Mostly urban' END AS area_type,
       COUNT(*) AS counties,
       ROUND(AVG(uninsured_rate), 2) AS avg_uninsured,
       ROUND(AVG(pcp_rate), 2)       AS avg_pcp,
       ROUND(AVG(prev_hos_stays), 0) AS avg_prev_stays
FROM data.county_health_analysis
WHERE rural_pct IS NOT NULL
GROUP BY area_type;

SELECT CASE WHEN med_income < 55000 THEN '1: Under 55k'
            WHEN med_income < 70000 THEN '2: 55k–70k'
            ELSE '3: 70k+' END AS income_band,
       CASE WHEN rural_pct >= 50 THEN 'Rural' ELSE 'Urban' END AS area_type,
       COUNT(*) AS counties,
       ROUND(AVG(uninsured_rate), 2) AS avg_uninsured,
       ROUND(AVG(pcp_rate), 2) AS avg_pcp
FROM data.county_health_analysis
WHERE rural_pct IS NOT NULL AND med_income IS NOT NULL
GROUP BY income_band, area_type
ORDER BY income_band, area_type;

SELECT CASE WHEN state = 'WV' THEN 'West Virginia' ELSE 'Rest of US' END AS region,
       COUNT(od_rate) AS counties_with_data,
       ROUND(AVG(od_rate), 2) AS avg_county_rate,
       ROUND(SUM(od_deaths) * 100000.0 / SUM(od_pop), 2) AS overall_rate
FROM data.county_health_analysis
WHERE od_rate IS NOT NULL
GROUP BY region;

SELECT state,
       ROUND(SUM(od_deaths) * 100000.0 / SUM(od_pop), 2) AS state_od_rate
FROM data.county_health_analysis
WHERE od_deaths IS NOT NULL AND od_pop IS NOT NULL
GROUP BY state
ORDER BY state_od_rate DESC;