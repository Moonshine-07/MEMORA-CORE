
import psutil
import time

from memory import (
    create_database,
    get_setting,
    save_setting
)


# ==================================================
# MAKE SURE DATABASE EXISTS
# ==================================================

create_database()


# ==================================================
# DEFAULT PROTECTED APPLICATIONS
# ==================================================

DEFAULT_PROTECTED_APPS = {
    "1password.exe",
    "bitwarden.exe",
    "keepass.exe",
    "keepassxc.exe",
    "lastpass.exe",
}


# ==================================================
# LIGHTWEIGHT MONITOR SETTINGS
# ==================================================

MONITOR_INTERVAL = 5

_last_process_scan = 0

_cached_processes = []


# ==================================================
# LOAD PROTECTED APPLICATIONS
# ==================================================

def load_protected_apps():

    saved_apps = get_setting(
        "protected_apps",
        None
    )

    if saved_apps:

        apps = set()

        for app in saved_apps.split("|"):

            app = app.strip().lower()

            if app:
                apps.add(app)

        return apps

    return set(DEFAULT_PROTECTED_APPS)


# ==================================================
# CURRENT PROTECTED APPLICATIONS
# ==================================================

PROTECTED_APPS = load_protected_apps()


# ==================================================
# SAVE PROTECTED APPLICATIONS
# ==================================================

def save_protected_apps():

    value = "|".join(
        sorted(PROTECTED_APPS)
    )

    save_setting(
        "protected_apps",
        value
    )


# ==================================================
# ADD PROTECTED APPLICATION
# ==================================================

def add_protected_app(app_name):

    if app_name:

        app_name = (
            app_name
            .lower()
            .strip()
        )

        PROTECTED_APPS.add(
            app_name
        )

        save_protected_apps()


# ==================================================
# REMOVE PROTECTED APPLICATION
# ==================================================

def remove_protected_app(app_name):

    if app_name:

        app_name = (
            app_name
            .lower()
            .strip()
        )

        PROTECTED_APPS.discard(
            app_name
        )

        save_protected_apps()


# ==================================================
# CHECK PROTECTED APPLICATION
# ==================================================

def is_protected_app(process_name):

    if not process_name:
        return False

    return (
        process_name.lower()
        in PROTECTED_APPS
    )


# ==================================================
# SYSTEM INFORMATION
# ==================================================

def get_system_info():

    cpu = psutil.cpu_percent(
        interval=0
    )

    ram = psutil.virtual_memory().percent

    disk = psutil.disk_usage('/').percent

    return {
        "cpu": cpu,
        "ram": ram,
        "disk": disk
    }


# ==================================================
# PROCESS MONITORING
# ==================================================

def get_top_processes(limit=20):

    global _last_process_scan
    global _cached_processes

    current_time = time.time()

    # Use cached information if
    # the last scan was less than 5 seconds ago.

    if (
        current_time
        - _last_process_scan
        < MONITOR_INTERVAL
    ):

        return _cached_processes[:limit]

    processes = []

    for process in psutil.process_iter(
        [
            "pid",
            "name",
            "cpu_percent",
            "memory_percent"
        ]
    ):

        try:

            info = process.info

            process_name = info.get(
                "name"
            )

            # Skip protected applications

            if is_protected_app(
                process_name
            ):

                continue

            processes.append({

                "pid": info.get(
                    "pid"
                ),

                "name": (
                    process_name
                    or "Unknown"
                ),

                "cpu": (
                    info.get(
                        "cpu_percent"
                    )
                    or 0
                ),

                "memory": (
                    info.get(
                        "memory_percent"
                    )
                    or 0
                )

            })

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):

            pass

    # Sort by RAM usage

    processes.sort(
        key=lambda x: x["memory"],
        reverse=True
    )

    # Update cache

    _cached_processes = processes

    _last_process_scan = current_time

    return processes[:limit]