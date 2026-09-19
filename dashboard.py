
import streamlit as st

from memory import (
    create_database,
    get_memories_for_project,
    fetch_memories_for_project,
    get_audit_logs,
    save_memory,
    delete_memory,
    cleanup_expired_memories
)

from monitor import (
    get_system_info,
    get_top_processes,
    PROTECTED_APPS,
    add_protected_app,
    remove_protected_app
)

from ai_engine import (
    analyze_system,
    detect_workflow,
    answer_from_memory
)


# ==================================================
# DATABASE
# ==================================================

create_database()

# Automatically remove expired memories
cleanup_expired_memories()


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Memora Core",
    page_icon="🧠",
    layout="wide"
)


# ==================================================
# HEADER
# ==================================================

st.title("🧠 MEMORA CORE")

st.subheader(
    "Privacy-Preserving AI Memory & OS Intelligence Layer"
)

st.caption(
    "Remember intelligently. Monitor responsibly. Protect by design."
)

st.divider()


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.header("⚙️ Control Center")

    privacy_mode = st.toggle(
        "🔒 Privacy Mode",
        value=False
    )

    monitoring_enabled = st.toggle(
        "🖥️ System Monitoring",
        value=True
    )

    workflow_enabled = st.toggle(
        "🔄 Workflow Detection",
        value=True
    )

    memory_collection_enabled = st.toggle(
        "🧠 Memory Collection",
        value=True
    )

    st.divider()

    st.info(
        "Memora uses local system metadata "
        "and project-scoped memory."
    )


# ==================================================
# PRIVACY STATUS
# ==================================================

st.header("🛡️ Privacy Status")

if privacy_mode:

    st.error(
        "🔒 PRIVACY MODE ACTIVE"
    )

    st.write(
        "Monitoring, process scanning, workflow "
        "detection, AI system analysis and new "
        "memory collection are paused."
    )

else:

    st.success(
        "🟢 PRIVACY MODE INACTIVE"
    )

    st.write(
        "Only the monitoring functions enabled "
        "by the user are active."
    )


st.divider()


# ==================================================
# PROTECTED APPLICATIONS
# ==================================================

st.header("🛡️ Protected Applications")

st.write(
    "Protected applications are excluded from "
    "Memora's process monitoring."
)

new_protected_app = st.text_input(
    "Application name",
    placeholder="Example: banking_app.exe"
)

if st.button(
    "➕ Protect Application"
):

    if new_protected_app.strip():

        add_protected_app(
            new_protected_app.strip()
        )

        st.success(
            f"🔒 {new_protected_app.strip()} "
            "has been protected."
        )

        st.rerun()

    else:

        st.warning(
            "Please enter an application name."
        )


if PROTECTED_APPS:

    st.write(
        "Currently protected:"
    )

    for app in sorted(PROTECTED_APPS):

        col1, col2 = st.columns(
            [5, 1]
        )

        with col1:

            st.write(
                f"🔒 {app}"
            )

        with col2:

            if st.button(
                "Remove",
                key=f"remove_{app}"
            ):

                remove_protected_app(
                    app
                )

                st.rerun()

else:

    st.info(
        "No applications are currently protected."
    )


st.divider()


# ==================================================
# SYSTEM MONITORING
# ==================================================

st.header("🖥️ System Intelligence")

system = None
processes = []


if privacy_mode:

    st.warning(
        "🔒 System monitoring paused."
    )

elif not monitoring_enabled:

    st.info(
        "⏸️ System monitoring disabled."
    )

else:

    system = get_system_info()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "CPU Usage",
            f"{system['cpu']}%"
        )

    with col2:

        st.metric(
            "RAM Usage",
            f"{system['ram']}%"
        )

    with col3:

        st.metric(
            "Disk Usage",
            f"{system['disk']}%"
        )


st.divider()


# ==================================================
# PROCESS MONITOR
# ==================================================

st.header("⚙️ Active Processes")


if privacy_mode:

    st.info(
        "🔒 Process monitoring paused."
    )

elif not monitoring_enabled:

    st.info(
        "⏸️ Process monitoring disabled."
    )

else:

    processes = get_top_processes()

    if processes:

        for process in processes[:10]:

            st.write(
                f"**{process['name']}** | "
                f"CPU: {round(process['cpu'], 2)}% | "
                f"RAM: {round(process['memory'], 2)}%"
            )

    else:

        st.info(
            "No process information available."
        )


st.divider()


# ==================================================
# AI SYSTEM ANALYSIS
# ==================================================

st.header("🤖 Memora AI Analysis")


if privacy_mode:

    st.info(
        "🔒 AI analysis paused."
    )

elif not monitoring_enabled:

    st.info(
        "⏸️ AI analysis requires monitoring."
    )

else:

    if system:

        analysis = analyze_system(
            system
        )

        if isinstance(
            analysis,
            list
        ):

            for message in analysis:

                st.info(message)

        else:

            st.info(analysis)

        if system["ram"] > 80:

            st.warning(
                "⚠️ High RAM usage detected."
            )

        elif system["cpu"] > 80:

            st.warning(
                "⚠️ High CPU usage detected."
            )

        else:

            st.success(
                "✅ System is operating normally."
            )


st.divider()


# ==================================================
# WORKFLOW DETECTION
# ==================================================

st.header("🔄 Workflow Detection")


if privacy_mode:

    st.info(
        "🔒 Workflow detection paused."
    )

elif not monitoring_enabled:

    st.info(
        "⏸️ Monitoring is disabled."
    )

elif not workflow_enabled:

    st.info(
        "⏸️ Workflow detection disabled."
    )

else:

    if processes:

        workflow = detect_workflow(
            processes
        )

        st.success(
            f"Detected workflow: {workflow}"
        )

    else:

        st.info(
            "No workflow information available."
        )


st.divider()


# ==================================================
# PROJECT MEMORY
# ==================================================

st.header("🧠 Project Memory")

project = st.selectbox(
    "Select Project",
    [
        "Project A",
        "Project B"
    ]
)


memory_result = get_memories_for_project(
    project,
    project
)


if memory_result["allowed"]:

    current_memories = (
        memory_result["memories"]
    )

else:

    current_memories = []


# ==================================================
# DISPLAY MEMORIES
# ==================================================

st.subheader(
    "📚 Stored Memories"
)


if current_memories:

    for index, memory in enumerate(
        current_memories
    ):

        col1, col2 = st.columns(
            [5, 1]
        )

        with col1:

            st.success(
                memory
            )

        with col2:

            if st.button(
                "🗑️ Delete",
                key=f"delete_{project}_{index}"
            ):

                delete_memory(
                    project,
                    memory
                )

                st.success(
                    "Memory deleted."
                )

                st.rerun()

else:

    st.info(
        "No memories stored for this project."
    )


# ==================================================
# ADD MEMORY
# ==================================================

st.subheader(
    "➕ Add New Memory"
)


if privacy_mode:

    st.warning(
        "🔒 New memory collection is paused."
    )

elif not memory_collection_enabled:

    st.info(
        "⏸️ Memory collection disabled."
    )

else:

    new_memory = st.text_input(
        "Information to remember",
        placeholder="Example: Project A uses FastAPI."
    )

    duration = st.selectbox(
        "Memory lifetime",
        [
            "Permanent",
            "1 Day",
            "7 Days"
        ]
    )

    if st.button(
        "💾 Save Memory"
    ):

        if new_memory.strip():

            if duration == "Permanent":

                save_memory(
                    project,
                    new_memory.strip()
                )

            elif duration == "1 Day":

                save_memory(
                    project,
                    new_memory.strip(),
                    1
                )

            else:

                save_memory(
                    project,
                    new_memory.strip(),
                    7
                )

            st.success(
                f"Memory saved for {project}."
            )

            st.rerun()

        else:

            st.warning(
                "Please enter some information."
            )


st.divider()


# ==================================================
# ASK MEMORA
# ==================================================

st.header("💬 Ask Memora AI")

question = st.text_input(
    "Ask something about the selected project",
    placeholder="Example: What framework does Project A use?"
)


if question:

    answer = answer_from_memory(
        question,
        current_memories
    )

    st.info(
        answer
    )


st.divider()


# ==================================================
# SECURITY AUDIT
# ==================================================

st.header("🔐 Security & Audit Trail")

logs = get_audit_logs()


if logs:

    col1, col2, col3, col4 = st.columns(4)

    allowed_count = sum(
        1
        for log in logs
        if log[3] == "ALLOWED"
    )

    blocked_count = sum(
        1
        for log in logs
        if log[3] == "BLOCKED"
    )

    save_count = sum(
        1
        for log in logs
        if log[1] == "SAVE"
    )

    delete_count = sum(
        1
        for log in logs
        if log[1] in [
            "DELETE",
            "AUTO_EXPIRE"
        ]
    )

    with col1:

        st.metric(
            "Total Events",
            len(logs)
        )

    with col2:

        st.metric(
            "Allowed",
            allowed_count
        )

    with col3:

        st.metric(
            "Blocked",
            blocked_count
        )

    with col4:

        st.metric(
            "Data Actions",
            save_count + delete_count
        )


    st.subheader(
        "Recent Security Events"
    )

    for log in logs[:10]:

        log_project = log[0]
        action = log[1]
        target_project = log[2]
        result = log[3]
        timestamp = log[4]

        if result == "BLOCKED":

            st.error(
                f"🚫 {log_project} → "
                f"{target_project} | "
                f"{action} | BLOCKED"
            )

        else:

            st.success(
                f"✅ {log_project} → "
                f"{target_project} | "
                f"{action} | ALLOWED"
            )

        st.caption(
            f"Time: {timestamp}"
        )

else:

    st.info(
        "No security events recorded yet."
    )


st.divider()


# ==================================================
# FOOTER
# ==================================================

st.caption(
    "🧠 Memora Core | "
    "AI Memory + OS Intelligence + "
    "Security + Privacy + Governance"
)