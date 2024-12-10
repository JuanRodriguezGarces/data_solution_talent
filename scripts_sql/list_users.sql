WITH ranked_resumes AS (
    SELECT
        r.id,
        r.user_id,
        r.video,
        r.type,
        r.created_at,
        ROW_NUMBER() OVER (PARTITION BY r.user_id ORDER BY r.created_at DESC) AS rn
    FROM
        resumes r
    WHERE
        r.type = 'pitch_video'
        AND r.video IS NOT NULL
        AND r.video <> ''  -- Aseguramos que el video no sea una cadena vacía
        AND r.created_at >= DATE_TRUNC('month', NOW() - INTERVAL '2 months')
)
SELECT
    p.user_id,
    rr.video,
    p.onboarding_goal AS main_objective,
    p.updated_at,
    p.created_at
FROM
    profiles p
JOIN
    ranked_resumes rr ON p.user_id = rr.user_id
WHERE
    p.onboarding_goal = 'be_discovered-[hire]'
    AND rr.rn = 1  -- Seleccionamos solo el primer video por usuario
ORDER BY
    p.user_id;
