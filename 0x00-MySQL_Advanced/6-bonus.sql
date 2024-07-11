-- Creates a stored procesure AddBouns.
DELIMITER $$

CREATE PROCEDURE AddBonus(
    IN user_id INT,
    IN project_name VARCHAR(255),
    IN score INT
)
BEGIN
    DECLARE project_id INT;

    -- Check if the project_name exists in projects table
    IF NOT EXISTS (
        SELECT id FROM projects WHERE name = project_name
    ) THEN
        INSERT INTO projects (name) VALUES (project_name);
    END IF;

    -- Insert the correction with user_id, project_id, and score
    INSERT INTO corrections (user_id, project_id, score)
    VALUES (
        user_id,
        (SELECT id FROM projects WHERE name = project_name),
        score
    );
END $$

DELIMITER ;
