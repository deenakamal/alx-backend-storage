-- Creates a stored procedure ComputeAverageScoreForUser.
DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
	DECLARE avgerage FLOAT;
	SELECT AVG(score)
	FROM corrections
	WHERE correction.user_id = user_id;

	UPDATE users
	SET avarage_score = average
	WHERE user_id = user_id
END $$

DELIMITER ;
