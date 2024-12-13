-- Create or replace the trigger function
CREATE OR REPLACE FUNCTION update_latest_weight()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE animal_profiles
    SET latest_weight = (
            SELECT weight
            FROM weights
            WHERE animal_id = NEW.animal_id
            ORDER BY record_date DESC
            LIMIT 1
        ),
        latest_record_date = (
            SELECT record_date
            FROM weights
            WHERE animal_id = NEW.animal_id
            ORDER BY record_date DESC
            LIMIT 1
        )
    WHERE id = NEW.animal_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Attach the trigger to the weights table
CREATE TRIGGER update_animal_profiles_latest_weight
AFTER INSERT OR UPDATE OR DELETE ON weights
FOR EACH ROW
EXECUTE FUNCTION update_latest_weight();
