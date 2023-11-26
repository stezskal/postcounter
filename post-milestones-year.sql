SELECT totals.*
FROM (
    SELECT avTotals.*
    FROM (
        SELECT
            PAX,
            COUNT(Date) AS TotalPosts,
            MAX(Date) AS LastPost,
            MIN(Date) AS FirstPost
        FROM attendance_view av
        WHERE YEAR(av.Date) = YEAR(NOW())  # Restricting posts to the current year
        GROUP BY PAX
    ) avTotals
    WHERE avTotals.LastPost > (NOW() - INTERVAL 180 DAY)
) totals
WHERE RIGHT(totals.TotalPosts, 2) IN ('92', '93', '94', '95', '96', '97', '98', '99', '00', '01', '02', '03')
ORDER BY totals.TotalPosts DESC;
