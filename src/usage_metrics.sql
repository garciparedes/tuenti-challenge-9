WITH myactivity AS (
    SELECT ROW_NUMBER() OVER (ORDER BY a.user_id, a.date_time, a.action) AS global_idx,
           a.user_id,
           a.date_time,
           a.action
    FROM activity a
),
     table_from AS (
         SELECT ROW_NUMBER() OVER (ORDER BY t.user_id, t.date_time) AS join_idx,
                t.date_time,
                t.user_id,
                t.global_idx
         FROM (SELECT LAG(a.action) OVER (PARTITION BY a.user_id ORDER BY a.date_time) AS previous,
                      a.date_time,
                      a.user_id,
                      a.action,
                      a.global_idx
               FROM myactivity AS a) AS t
         WHERE t.action LIKE 'open'
            OR t.previous IS NULL
            OR t.previous LIKE 'close'
     ),
     table_to AS (
         SELECT ROW_NUMBER() OVER (ORDER BY t.user_id, t.date_time) AS join_idx,
                t.date_time,
                t.user_id,
                t.global_idx
         FROM (SELECT LEAD(a.action) OVER (PARTITION BY a.user_id ORDER BY a.date_time) AS next,
                      a.date_time,
                      a.user_id,
                      a.action,
                      a.global_idx
               FROM myactivity AS a) AS t
         WHERE t.action LIKE 'close'
            OR t.next IS NULL
            OR t.next LIKE 'open'
     )
SELECT CAST(table_from.user_id AS INTEGER)                                              AS user_id,
       CAST(DATE_FORMAT(table_from.date_time, '%Y-%m-%d %H:%i:%S') AS CHAR)             AS session_from,
       CAST(DATE_FORMAT(table_to.date_time, '%Y-%m-%d %H:%i:%S') AS CHAR)               AS session_to,
       CAST(TIMESTAMPDIFF(SECOND, table_from.date_time, table_to.date_time) AS INTEGER) AS seconds,
       CAST((table_to.global_idx - table_from.global_idx + 1) AS INTEGER)               AS num_actions
FROM table_from
         INNER JOIN table_to ON table_from.join_idx = table_to.join_idx
ORDER BY user_id, session_from;