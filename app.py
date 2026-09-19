print("MEMORA CORE")
print("AI OS Intelligence Layer")
print("System starting...")\

from monitor import get_system_info, get_top_processes
from memory import create_database, save_memory, get_memories_for_project, get_audit_logs
from ai_engine import(
    extract_memory,
    answer_from_memory,
    analyze_system,
    predict_system_problem,
    analyze_processes,
    detect_workflow
)

print("MEMORA CORE")
print("AI OS Intelligence Layer")
print("--------------------------------")

history =[]

print("\n Collecting system data...")

for i in range(3):
    system = get_system_info()

    history.append(system)

    print(
        f"Reading {i+1}: "
        f"CPU={system['cpu']}% | "
        f"RAM={system['ram']}% | "
        f"Disk={system['disk']}% "
    )  


print("\n================================")
print("          MEMORA AI PREDICTION")
print("================================")

prediction = predict_system_problem(history)

print(prediction)

print("\nTOP PROCESSES")
print("------------------------------")

processes = get_top_processes()

for process in processes:
    print(
        process["name"],
        "| CPU: ",
        process["cpu"],
        "% | RAM: ",
        round(process["memory"], 2),
        "%"
        )
print("\n================================")
print("          PROCESS ANALYSIS")
print("================================")

process_analysis = analyze_processes(processes)

for message in process_analysis:
    print("MEMORA:", message)

print("\n===============================")
print("       MEMORA AI ANALYSIS")
print("===============================")

warnings = analyze_system(system)

for warning in warnings:
    print("MEMORA:", warning)

print("\n===============================")
print("       WORKFLOW DETECTION")
print("===============================")

workflow = detect_workflow(processes)

print("MEMORA WORKFLOW:", workflow)

print("\n=================================================")
print("   MEMORA CORE")
print("   SECURITY TEST")
print("=================================================")

create_database()

print("\n================================================")
print("     MEMORA AI MEMORY")
print("=================================================")

project = input("Enter project name: ")
user_input = input("Tell Memora something about your project: ")

detected_memories = extract_memory(user_input)

if detected_memories:

    for memory in detected_memories:
        save_memory(project, memory)
        print("Memory saved:", memory)
else:
    print("No important memory detected")


print("\n================================================")
print("      SMART MEMORY SEARCH")
print("================================================")

search_project = input("Which project should I search for? ")

question = input("Ask Memora a question: ")

result = get_memories_for_project(
    search_project,
    search_project
)

if result["allowed"]:
    answer = answer_from_memory(question, result["memories"])

    print("\nMEMORA:")
    print(answer)

else: 
    print("\nACCESS DENIED")
    print(result["message"])    

print("\n TEST 1: Projest B requesting Project B")
print("------------------------------")

result = get_memories_for_project(
    "Project B", 
    "Project B"
)

print(result)

print("\n TEST 2: Project A requesting Project B")
print("------------------------------")

result = get_memories_for_project(
    "Project A", 
    "Project B"
)

print(result)

print("\n TEST 3: Project B requesting Project A")
print("------------------------------")

result = get_memories_for_project(
    "Project B",
    "Project A"
)

print(result)

print('\n AUDIT LOGS')
print("===============================")

logs = get_audit_logs()

for log in logs:
    project, action, target_project, result, timestamp = log

    print(f"""
        Project: {project}
        Action: {action}
        Target: {target_project}
        Result: {result}
        Time: {timestamp}
        -------------------------------
        """)

print("\nMEMORY CONTENTS")
print("=================================")

print("\nProject A:")
print(get_memories_for_project("Project A", "Project A"))

print("\nProject B:")
print(get_memories_for_project("Project B", "Project B"))



