-- Step 1: Add `animal_name` to `weights` and `deep_cleans`
ALTER TABLE weights ADD COLUMN animal_name VARCHAR(255);
ALTER TABLE deep_cleans ADD COLUMN animal_name VARCHAR(255);

-- Backfill `animal_name` in `weights`
UPDATE weights
SET animal_name = (
    SELECT name
    FROM animal_profiles
    WHERE animal_profiles.id = weights.animal_id
);

-- Backfill `animal_name` in `deep_cleans`
UPDATE deep_cleans
SET animal_name = (
    SELECT name
    FROM animal_profiles
    WHERE animal_profiles.id = deep_cleans.animal_id
);

-- Step 2: Create trigger functions for `animal_name` sync

-- Trigger for syncing `weights.animal_name`
CREATE OR REPLACE FUNCTION update_weights_animal_name()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE weights
    SET animal_name = NEW.name
    WHERE animal_id = NEW.id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for syncing `deep_cleans.animal_name`
CREATE OR REPLACE FUNCTION update_deep_cleans_animal_name()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE deep_cleans
    SET animal_name = NEW.name
    WHERE animal_id = NEW.id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Attach triggers to `animal_profiles`
CREATE TRIGGER sync_weights_animal_name
AFTER UPDATE OF name ON animal_profiles
FOR EACH ROW
EXECUTE FUNCTION update_weights_animal_name();

CREATE TRIGGER sync_deep_cleans_animal_name
AFTER UPDATE OF name ON animal_profiles
FOR EACH ROW
EXECUTE FUNCTION update_deep_cleans_animal_name();

-- Step 3: Add `latest_deep_clean_date` and `latest_cleaner_name` to `animal_profiles`
ALTER TABLE animal_profiles ADD COLUMN latest_deep_clean_date DATE;
ALTER TABLE animal_profiles ADD COLUMN latest_cleaner_name VARCHAR(255);

-- Backfill `latest_deep_clean_date` and `latest_cleaner_name`
UPDATE animal_profiles
SET latest_deep_clean_date = subquery.latest_clean_date,
    latest_cleaner_name = subquery.cleaner_name
FROM (
    SELECT animal_id, MAX(clean_date) AS latest_clean_date, 
           (ARRAY_AGG(cleaner_name ORDER BY clean_date DESC))[1] AS cleaner_name
    FROM deep_cleans
    GROUP BY animal_id
) AS subquery
WHERE animal_profiles.id = subquery.animal_id;

-- Step 4: Create trigger function for syncing `latest_deep_clean_date` and `latest_cleaner_name`
CREATE OR REPLACE FUNCTION update_latest_deep_clean()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE animal_profiles
    SET latest_deep_clean_date = subquery.latest_clean_date,
        latest_cleaner_name = subquery.cleaner_name
    FROM (
        SELECT MAX(clean_date) AS latest_clean_date, 
               (ARRAY_AGG(cleaner_name ORDER BY clean_date DESC))[1] AS cleaner_name
        FROM deep_cleans
        WHERE animal_id = NEW.animal_id
    ) AS subquery
    WHERE animal_profiles.id = NEW.animal_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Attach triggers to `deep_cleans`
CREATE TRIGGER sync_latest_deep_clean_after_insert
AFTER INSERT ON deep_cleans
FOR EACH ROW
EXECUTE FUNCTION update_latest_deep_clean();

CREATE TRIGGER sync_latest_deep_clean_after_update
AFTER UPDATE ON deep_cleans
FOR EACH ROW
EXECUTE FUNCTION update_latest_deep_clean();

CREATE TRIGGER sync_latest_deep_clean_after_delete
AFTER DELETE ON deep_cleans
FOR EACH ROW
EXECUTE FUNCTION update_latest_deep_clean();
