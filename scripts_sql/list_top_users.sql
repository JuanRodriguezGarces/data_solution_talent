SELECT
    p.user_id,
    p.views,
    u.name AS user_name,
    u.email,
    p.created_at AS profile_created_at,
    p.updated_at AS profile_updated_at
FROM
    profiles p
JOIN
    users u ON p.user_id = u.id
ORDER BY
    p.views DESC
LIMIT 10;
