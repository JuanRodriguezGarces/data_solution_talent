SELECT 
    id AS Id_challenge,
    name AS Name,
    description AS Description,
    status AS Status,
    opencall_objective AS OpenCall_Objective,
    created_at AS Created_at
FROM 
    challenges
WHERE 
    status = 'open'
    AND created_at >= DATE_TRUNC('month', NOW() - INTERVAL '3 months')
ORDER BY 
    created_at DESC;
