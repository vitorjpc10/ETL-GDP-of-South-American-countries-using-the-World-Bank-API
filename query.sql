SELECT
    c.id,
    c.name,
    c.iso3_code,
	MAX(CASE WHEN g.year = 2019 THEN g.value / 1e9 END) AS "2019",
	MAX(CASE WHEN g.year = 2020 THEN g.value / 1e9 END) AS "2020",
	MAX(CASE WHEN g.year = 2021 THEN g.value / 1e9 END) AS "2021",
	MAX(CASE WHEN g.year = 2022 THEN g.value / 1e9 END) AS "2022",
	MAX(CASE WHEN g.year = 2023 THEN g.value / 1e9 END) AS "2023"
FROM
	country c
LEFT JOIN
	gdp g ON c.id = g.country_id
GROUP BY
	c.id, c.name, c.iso3_code
ORDER BY
	c.name