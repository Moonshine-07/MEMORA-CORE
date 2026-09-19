
import sqlite3
from datetime import datetime, timedelta
import os


# ==================================================
# DATABASE LOCATION
# ==================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE = os.path.join(
    BASE_DIR,
    "memora.db"
)


# ==================================================
# CREATE DATABASE
# ==================================================

def create_database():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    print("DATABASE:", DATABASE)

    # --------------------------------------------------
    # MEMORIES TABLE
    # --------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project TEXT NOT NULL,
            information TEXT NOT NULL,
            created_at TEXT NOT NULL,
            expires_at TEXT,
            UNIQUE(project, information)
        )
        """
    )

    # --------------------------------------------------
    # MIGRATE OLD DATABASE
    # --------------------------------------------------

    cursor.execute(
        "PRAGMA table_info(memories)"
    )

    columns = [
        column[1]
        for column in cursor.fetchall()
    ]

    if "expires_at" not in columns:

        cursor.execute(
            """
            ALTER TABLE memories
            ADD COLUMN expires_at TEXT
            """
        )

    # --------------------------------------------------
    # AUDIT LOG TABLE
    # --------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project TEXT NOT NULL,
            action TEXT NOT NULL,
            target_project TEXT NOT NULL,
            result TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
        """
    )

    # --------------------------------------------------
    # SETTINGS TABLE
    # --------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
        """
    )

    connection.commit()

    connection.close()


# ==================================================
# AUTOMATIC EXPIRED MEMORY CLEANUP
# ==================================================

def cleanup_expired_memories():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    now = datetime.now().isoformat()

    # Find expired memories first
    cursor.execute(
        """
        SELECT project, information
        FROM memories
        WHERE expires_at IS NOT NULL
        AND expires_at <= ?
        """,
        (now,)
    )

    expired_memories = cursor.fetchall()

    # Delete expired memories
    cursor.execute(
        """
        DELETE FROM memories
        WHERE expires_at IS NOT NULL
        AND expires_at <= ?
        """,
        (now,)
    )

    connection.commit()

    connection.close()

    # Record automatic cleanup
    for project, information in expired_memories:

        log_event(
            project,
            "AUTO_EXPIRE",
            project,
            "ALLOWED"
        )

    return len(expired_memories)


# ==================================================
# FETCH MEMORIES
# ==================================================

def fetch_memories_for_project(project):

    # Clean expired memories before returning data
    cleanup_expired_memories()

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    now = datetime.now().isoformat()

    cursor.execute(
        """
        SELECT information
        FROM memories
        WHERE project = ?
        AND (
            expires_at IS NULL
            OR expires_at > ?
        )
        ORDER BY id ASC
        """,
        (
            project,
            now
        )
    )

    memories = [
        row[0]
        for row in cursor.fetchall()
    ]

    connection.close()

    return memories


# ==================================================
# ACCESS CONTROL
# ==================================================

def get_memories_for_project(
    current_project,
    requested_project
):

    if current_project != requested_project:

        log_event(
            current_project,
            "READ",
            requested_project,
            "BLOCKED"
        )

        return {
            "allowed": False,
            "message": (
                "Access denied: memory belongs "
                "to another project."
            ),
            "memories": []
        }

    memories = fetch_memories_for_project(
        requested_project
    )

    log_event(
        current_project,
        "READ",
        requested_project,
        "ALLOWED"
    )

    return {
        "allowed": True,
        "memories": memories
    }


# ==================================================
# SAVE MEMORY
# ==================================================

def save_memory(
    project,
    information,
    duration_days=None
):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    created_at = datetime.now()

    if duration_days is None:

        expires_at = None

    else:

        expires_at = (
            created_at
            + timedelta(days=duration_days)
        ).isoformat()

    cursor.execute(
        """
        INSERT OR IGNORE INTO memories
        (
            project,
            information,
            created_at,
            expires_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            project,
            information,
            created_at.isoformat(),
            expires_at
        )
    )

    connection.commit()

    connection.close()

    log_event(
        project,
        "SAVE",
        project,
        "ALLOWED"
    )


# ==================================================
# DELETE MEMORY
# ==================================================

def delete_memory(
    project,
    information
):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM memories
        WHERE project = ?
        AND information = ?
        """,
        (
            project,
            information
        )
    )

    connection.commit()

    connection.close()

    log_event(
        project,
        "DELETE",
        project,
        "ALLOWED"
    )


# ==================================================
# AUDIT LOG
# ==================================================

def log_event(
    project,
    action,
    target_project,
    result
):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO audit_logs
        (
            project,
            action,
            target_project,
            result,
            timestamp
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            project,
            action,
            target_project,
            result,
            datetime.now().isoformat()
        )
    )

    connection.commit()

    connection.close()


def get_audit_logs():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            project,
            action,
            target_project,
            result,
            timestamp
        FROM audit_logs
        ORDER BY id DESC
        """
    )

    logs = cursor.fetchall()

    connection.close()

    return logs


# ==================================================
# SETTINGS
# ==================================================

def save_setting(
    key,
    value
):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO settings
        (key, value)
        VALUES (?, ?)
        """,
        (
            key,
            str(value)
        )
    )

    connection.commit()

    connection.close()


def get_setting(
    key,
    default=None
):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT value
        FROM settings
        WHERE key = ?
        """,
        (key,)
    )

    result = cursor.fetchone()

    connection.close()

    if result is None:

        return default

    return result[0]


def delete_setting(
    key
):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM settings
        WHERE key = ?
        """,
        (key,)
    )

    connection.commit()

    connection.close()