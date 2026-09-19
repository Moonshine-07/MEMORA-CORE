def extract_memory(text):
    """
    Simple AI-style memory extraction.
    Finds useful information from user input.
    """
    text = text.strip()

    if not text:
        return[]

    memories = []

    keywords = [
        "use",
        "using",
        "built with",
        "build with",
        "project",
        "prefer",
        "always",
        "never",
        "database",
        "backend",
        "frontend",
        "python",
        "fastapi",
        "flask",
        "pydantic"
    ]

    lower_text = text.lower()

    for keyword in keywords:
        if keyword in lower_text:
            memories.append(text)
            break

    return memories 

if __name__=="__main__":
    print("=========================================================")
    print("       MEMORA AI ENGINE")
    print("=========================================================")

    text = input("Tell Memora something: ")

    memories = extract_memory(text)

    if memories:
        print("\n Memory detected:")
        for memory in memories:
            print("=>", memory)
    else:
        print("\nNo important memory detected.")

def answer_from_memory(question, memories):
    """
    Finds the most relevant stored memory for a question.
    """

    question_words = set(question.lower().split())

    best_memory = None
    best_score = 0

    for memory in memories:
        memory_words = set(memory.lower().split())
        score = len(question_words & memory_words)

        if score > best_score:
            best_score = score
            best_memory = memory

    if best_memory:
        return best_memory

    return "I couldn't find relevant information in my memory."

def analyze_system(system):
    cpu = system["cpu"]
    ram = system["ram"]
    disk = system["disk"]

    warnings = []

    if cpu >= 80:
        warnings.append(
            "CPU usage is high. Some applications may be using excessive processing power."
        )
    if ram >= 80:
        warnings.append(
            "RAM usage is high. Closing unused applications may improve performance."
        )    
    if disk >= 90:
        warnings.append(
            "Disk usage is high. Consider freeing up some storage space."
        )
    if not warnings:
        warnings.append(
        "System is running normally. No major resource problems detected."
        )

    return warnings

def predict_system_problem(history):
    """
    Predicts possible resource problems from previous readings.
    """

    if len(history) < 3:
        return "Not enough data to make a prediction."

    ram_values = [item["ram"] for item in history]
    cpu_values = [item["cpu"] for item in history]

    ram_increasing = (
        ram_values[-1] > ram_values[-2] and
         ram_values[-2] > ram_values[-3]
    )    
    cpu_increasing = (
        cpu_values[-1] > cpu_values[-2] and
        cpu_values[-2] > cpu_values[-3]
    )
    if ram_increasing and ram_values[-1] >= 70:
        return "RAM usage is continuously increasing. A memory problem may occur soon."
    if cpu_increasing and cpu_values[-1] >= 70:
        return "CPU usage is continuously increasing. A performance problem may occur soon."

    return "No major increasing resource trend detected"

def analyze_processes(processes):
    """
    Analyzes running processes and identifies heavy resource users.
    """
    if not processes:
        return ["No processes information available."]

    recommendations = []

    highest_memory = max(
        processes,
        key=lambda process:
        process["memory"]
    )

    highest_cpu = max(
        processes,
        key=lambda process:
        process["cpu"]
    )
    if highest_memory["memory"] >= 10:
        recommendations.append(
            f"{highest_memory['name']} is using "
            f"{highest_memory['memory']:.2f}% of RAM."
        )
    if highest_cpu["cpu"] >= 20:
        recommendations.append(
            f"{highest_cpu['name']} is using "
            f"{highest_cpu['cpu']:.2f}% of CPU."
        )    
    if not recommendations:
        recommendations.append(
            "No process is currently using excessive resources."
        )    
    return recommendations

def detect_workflow(processes):
    """
    Detects a workflow from currently running applications.
    """

    app_names = []

    for process in processes:
        name = process["name"].lower()
        if "code.exe" in name or name == "code":
            app_names.append("VS Code")

        elif "chrome.exe" in name or name == "chrome":
            app_names.append("Chrome")

        elif "python.exe" in name or name == "python":
            app_names.append("Python")

        elif "firefox.exe" in name or name == "firefox":
            app_names.append("Firefox")

        elif "msedge.exe" in name or name == "edge":
            app_names.append("Microsoft Edge")

    app_names = list(dict.fromkeys(app_names))

    if len(app_names) >= 2:
        return " + ".join(app_names)
    elif len(app_names) == 1:
        return f"Partial workflow detected: {app_names[0]}"
    else:
        return "No common workflow detected."