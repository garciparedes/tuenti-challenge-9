SELECT table_from.user_id,
       table_from.date_time                                            as session_from,
       table_to.date_time                                              as session_to,
       TIMESTAMPDIFF(SECOND, table_from.date_time, table_to.date_time) as seconds,
       (
         SELECT COUNT(*)
         FROM activity as act
         WHERE date_time BETWEEN table_from.date_time AND table_to.date_time
           AND user_id = table_from.user_id
       ) as num_actions
FROM (
         SELECT RANK() over (PARTITION BY user_id ORDER BY date_time) as idx,
                date_time,
                user_id
         FROM (
                  SELECT LAG(action, 1) OVER (PARTITION BY user_id ORDER BY date_time) AS previous,
                         date_time,
                         user_id,
                         action
                  FROM activity
              ) AS T1
         WHERE T1.previous IS NULL
            OR T1.action LIKE 'open'
            OR T1.previous LIKE 'close'
         ORDER BY user_id, date_time
     ) AS table_from INNER JOIN (
         SELECT RANK() over (PARTITION BY user_id ORDER BY date_time) as idx,
                date_time,
                user_id
         FROM (SELECT LAG(action, -1) OVER (PARTITION BY user_id ORDER BY date_time) AS next,
                      date_time,
                      user_id,
                      action
               FROM activity
              ) AS T1
         WHERE T1.next IS NULL
            OR T1.action LIKE 'close'
            OR T1.next LIKE 'open'
         ORDER BY user_id, date_time
     ) AS table_to ON table_from.idx = table_to.idx AND
                 table_from.user_id = table_to.user_id
ORDER BY user_id, session_from;

