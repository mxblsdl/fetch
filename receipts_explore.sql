-- SQLite
-- Get the approximate date ranges of the data
SELECT DISTINCT STRFTIME('%m',DATETIME( CAST(dateScanned as INTEGER) / 1000, 'unixepoch')) as Month,
STRFTIME('%Y',DATETIME( CAST(dateScanned as INTEGER) / 1000, 'unixepoch')) as Year
FROM Receipts;

-- March has the most recent data
SELECT
STRFTIME('%m',DATETIME( CAST(dateScanned as INTEGER) / 1000, 'unixepoch')) as Month,
STRFTIME('%Y',DATETIME( CAST(dateScanned as INTEGER) / 1000, 'unixepoch')) as Year,
brandCode,
count(brandCode) as count
FROM Receipts
JOIN Items
WHERE Month = '03'
GROUP BY brandCode
ORDER BY count(brandCode) desc
limit 5;

SELECT
STRFTIME('%m',DATETIME( CAST(dateScanned as INTEGER) / 1000, 'unixepoch')) as Month,
STRFTIME('%Y',DATETIME( CAST(dateScanned as INTEGER) / 1000, 'unixepoch')) as Year,
brandCode,
count(brandCode) as count
FROM Receipts
JOIN Items
WHERE Month = '02'
GROUP BY brandCode
ORDER BY count(brandCode) desc
limit 5;