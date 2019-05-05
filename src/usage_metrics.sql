WITH table_from AS (
    SELECT ROW_NUMBER() OVER(ORDER BY t.user_id, t.date_time) AS idx,
           t.date_time,
           t.user_id
    FROM (SELECT LAG(a.action, 1) OVER(PARTITION BY a.user_id ORDER BY a.date_time) AS previous,
                 a.date_time,
                 a.user_id,
                 a.action
          FROM activity AS a
         ) AS t
    WHERE t.action LIKE 'open'
       OR t.previous IS NULL
       OR t.previous LIKE 'close'
),
     table_to AS (
         SELECT ROW_NUMBER() OVER(ORDER BY t.user_id, t.date_time) AS idx,
                t.date_time,
                t.user_id
         FROM (SELECT LAG(a.action, -1) OVER(PARTITION BY a.user_id ORDER BY a.date_time) AS next,
                      a.date_time,
                      a.user_id,
                      a.action
               FROM activity AS a
              ) AS t
         WHERE t.action LIKE 'close'
            OR t.next IS NULL
            OR t.next LIKE 'open'
     )
SELECT CAST(table_from.user_id AS INTEGER)                                              AS user_id,
       CAST(DATE_FORMAT(table_from.date_time, '%Y-%m-%d %H:%i:%S') AS CHAR)             AS session_from,
       CAST(DATE_FORMAT(table_to.date_time, '%Y-%m-%d %H:%i:%S') AS CHAR)               AS session_to,
       CAST(TIMESTAMPDIFF(SECOND, table_from.date_time, table_to.date_time) AS INTEGER) AS seconds,
       CAST((SELECT COUNT(*)
             FROM activity
             WHERE date_time BETWEEN table_from.date_time AND table_to.date_time
               AND user_id = table_from.user_id) AS INTEGER)                            AS num_actions
FROM table_from
         INNER JOIN table_to ON table_from.idx = table_to.idx
ORDER BY user_id, session_from;