SELECT *
FROM (
    SELECT *
    FROM (
        SELECT
            PAX,
            COUNT(Date) AS TotalPosts,
            MAX(Date) AS LastPost,
            MIN(Date) AS FirstPost
        FROM attendance_view av
        GROUP BY PAX
    ) avTotals
    WHERE avTotals.LastPost > (NOW() - INTERVAL 180 DAY) # Looking for PAX active in the Last 180 Days
) totals
WHERE RIGHT(totals.TotalPosts, 2) IN ('92', '93', '94', '95', '96', '97', '98', '99', '00', '01', '02', '03')
ORDER BY TotalPosts DESC;
