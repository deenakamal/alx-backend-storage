-- Drop the procedure if it already exists
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    UPDATE users u
    SET average_score = (
        SELECT  
            CASE WHEN SUM(corrections.score * projects.weight) IS NOT NULL AND SUM(projects.weight) IS NOT NULL
                 THEN SUM(corrections.score * projects.weight) / SUM(projects.weight)
                 ELSE 0 
            END
        FROM 
            corrections
        JOIN 
            projects ON projects.id = corrections.project_id
        WHERE 
            corrections.user_id = u.id
    );
END $$

DELIMITER ;
