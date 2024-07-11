-- Creates trigger.
DELIMITER //

CREATE TRIGGER decrease_quantity
AFTER INSERT ON orders FOR EACH ROW
BEGIN
	UPDATE items
	SET quantity = quantity - 1 * NEW.number
	WHERE name = NEW.name;
END //

DELIMITER;
