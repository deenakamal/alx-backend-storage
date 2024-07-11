-- Creates trigger that resets the attribute valid_email.
DELIMITER $$
CREATE TRIGGER reset_email
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
	IF NEW.email != OLD.email THEN
		SET valid_email = 0;
	END IF;
END $$
DELIMITER;
