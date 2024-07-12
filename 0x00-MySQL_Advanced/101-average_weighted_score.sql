-- Creates stored procedure ComputeAverageWeightedScoreForUsers.
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight FLOAT;
    DECLARE average_weighted_score FLOAT;

    -- Calculate total weighted score for all users
    SELECT SUM(corrections.score * projects.weight)
    INTO total_weighted_score
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id;

    -- Calculate total weight across all projects
    SELECT SUM(weight)
    INTO total_weight
    FROM projects;

    -- Handle division by zero scenario
    IF total_weight > 0 THEN
        SET average_weighted_score = total_weighted_score / total_weight;
    ELSE
        SET average_weighted_score = 0;
    END IF;

    -- Update all users' average scores with calculated average
    UPDATE users
    SET average_score = average_weighted_score;
END $$

DELIMITER ;
