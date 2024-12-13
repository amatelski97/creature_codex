from psycopg import connect
import os

# Database settings
DATABASE_URL = "postgresql://postgres:1597@localhost:5432/creature_codex_live"

def get_applied_migrations(conn):
    """
    Retrieve the list of already applied migrations from the database.
    """
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS migration_versions (
                version INTEGER PRIMARY KEY,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        
        cur.execute("SELECT version FROM migration_versions ORDER BY version;")
        return [row[0] for row in cur.fetchall()]

def apply_migration(conn, migration_version, migration_content):
    """
    Apply a single migration and record it in the migration_versions table.
    """
    with conn.cursor() as cur:
        try:
            cur.execute(migration_content)
            cur.execute("INSERT INTO migration_versions (version) VALUES (%s);", (migration_version,))
            conn.commit()
        except Exception as e:
            print(f"Error applying migration version {migration_version}: {e}")
            raise

def run_migrations():
    """
    Run all pending migrations.
    """
    migrations_dir = os.path.join(os.path.dirname(__file__), "sql")
    migration_files = sorted(f for f in os.listdir(migrations_dir) if f.endswith(".sql"))
    
    with connect(DATABASE_URL, autocommit=True) as conn:
        applied_versions = get_applied_migrations(conn)

        for migration_file in migration_files:
            version = int(migration_file.split("_")[0])  # Extract version from filename
            if version not in applied_versions:
                print(f"Applying migration: {migration_file}")
                with open(os.path.join(migrations_dir, migration_file), "r") as f:
                    try:
                        apply_migration(conn, version, f.read())
                        print(f"Migration {migration_file} applied successfully.")
                    except Exception as e:
                        print(f"Failed to apply migration {migration_file}: {e}")

if __name__ == "__main__":
    run_migrations()
