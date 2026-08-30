# MySQL Database Setup for Faction_Store

This guide provides instructions to set up the MySQL database backend for **Faction_Store**.

---

## 1. Prerequisites
Ensure you have a MySQL Server installed and running on your system (e.g., MySQL Community Server, XAMPP, WampServer, or Docker MySQL).

---

## 2. Database Creation
Connect to your MySQL server as `root` or an administrative user using the MySQL command line, MySQL Workbench, phpMyAdmin, or any SQL client, and run the following commands:

```sql
-- Create the Faction Store Database
CREATE DATABASE faction_store CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create a dedicated database user (optional, or use root)
CREATE USER 'root'@'127.0.0.1' IDENTIFIED BY 'admin';

-- Grant privileges to the user on the database
GRANT ALL PRIVILEGES ON faction_store.* TO 'root'@'127.0.0.1';

-- Flush privileges to apply changes
FLUSH PRIVILEGES;
```

---

## 3. Django Connection Configuration
The database connection settings are located in [settings.py](file:///c:/Users/romin/OneDrive/Desktop/fashion_store/faction_store/settings.py). 

We have implemented an **automatic fallback mechanism**:
- If MySQL is running and the database is configured with the variables below, Django will connect to MySQL automatically.
- If MySQL is down, not yet configured, or the credentials do not match, Django will dynamically fall back to a local SQLite database (`db.sqlite3`). This allows the project to be fully functional out-of-the-box immediately for testing.

### To customize database coordinates:
Configure the variables at the top of settings.py or set environment variables on your system:
- `DB_HOST` (Default: `127.0.0.1`)
- `DB_USER` (Default: `root`)
- `DB_PASSWORD` (Default: `admin`)
- `DB_NAME` (Default: `faction_store`)
- `DB_PORT` (Default: `3306`)

---

## 4. Run Migrations
After database setup is complete, run the standard Django migration commands in your terminal:

```bash
python manage.py makemigrations
python manage.py migrate
```

*Note: The PyMySQL driver handles the connection automatically and registers itself as the `MySQLdb` driver within settings.py.*
