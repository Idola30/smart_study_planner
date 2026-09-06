# Smart Study Planner
# Programming Fundamentals Coursework

import json

FILE_NAME = "study_log.txt"


def classify_session(duration):
    """Return a simple category for the length of a study session."""
    if duration < 30:
        return "Short"
    elif duration <= 90:
        return "Medium"
    else:
        return "Long"


def add_session(sessions):
    """Get one study session from the user and add it to the list."""
    print("\n--- Add Study Session ---")

    subject = input("Subject: ").strip()
    while subject == "":
        print("Subject cannot be empty.")
        subject = input("Subject: ").strip()

    topic = input("Topic covered: ").strip()
    while topic == "":
        print("Topic cannot be empty.")
        topic = input("Topic covered: ").strip()

    date_label = input("Date/day: ").strip()
    while date_label == "":
        print("Date/day cannot be empty.")
        date_label = input("Date/day: ").strip()

    while True:
        value = input("Duration (minutes): ").strip()
        try:
            duration = float(value)
            if duration <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    session = {
        "subject": subject,
        "topic": topic,
        "date": date_label,
        "duration": duration
    }

    sessions.append(session)
    print("Study session added successfully.")


def view_sessions(sessions):
    """Display all recorded sessions in a simple table."""
    print("\n--- All Study Sessions ---")

    if not sessions:
        print("No study sessions have been recorded yet.")
        return

    print("-" * 82)
    print(f"{'No.':<5}{'Subject':<18}{'Topic':<25}{'Minutes':<12}{'Class':<12}")
    print("-" * 82)

    for number, session in enumerate(sessions, start=1):
        subject = session.get("subject", "")
        topic = session.get("topic", "")
        duration = float(session.get("duration", 0))
        category = classify_session(duration)

        print(
            f"{number:<5}"
            f"{subject[:17]:<18}"
            f"{topic[:24]:<25}"
            f"{duration:<12.1f}"
            f"{category:<12}"
        )

    print("-" * 82)


def search_by_subject(sessions):
    """Search for a subject without worrying about upper/lower case."""
    print("\n--- Search by Subject ---")
    subject = input("Enter subject name: ").strip()

    if subject == "":
        print("Please enter a subject name.")
        return

    matches = [
        session for session in sessions
        if session.get("subject", "").strip().lower() == subject.lower()
    ]

    if not matches:
        print(f"No sessions found for '{subject}'.")
        return

    print(f"\nSessions for {subject}:")
    print("-" * 68)
    print(f"{'Date':<15}{'Topic':<28}{'Minutes':<12}{'Class':<12}")
    print("-" * 68)

    total_minutes = 0

    for session in matches:
        duration = float(session.get("duration", 0))
        total_minutes += duration
        print(
            f"{session.get('date', '')[:14]:<15}"
            f"{session.get('topic', '')[:27]:<28}"
            f"{duration:<12.1f}"
            f"{classify_session(duration):<12}"
        )

    print("-" * 68)
    print(f"Total time for {subject}: {total_minutes:.1f} minutes "
          f"({total_minutes / 60:.2f} hours)")


def study_statistics(sessions):
    """Calculate and display the main study statistics."""
    print("\n--- Study Statistics ---")

    if not sessions:
        print("There are no study sessions to analyse.")
        return

    total_minutes = sum(float(session.get("duration", 0)) for session in sessions)
    print(f"Total hours studied: {total_minutes / 60:.2f}")

    subject_totals = {}

    for session in sessions:
        subject = session.get("subject", "Unknown")
        duration = float(session.get("duration", 0))

        # Keep the subject names readable while grouping them case-insensitively.
        key = subject.strip().lower()
        if key not in subject_totals:
            subject_totals[key] = {"name": subject, "minutes": 0}
        subject_totals[key]["minutes"] += duration

    print("\nTime studied per subject:")
    for data in sorted(subject_totals.values(), key=lambda item: item["name"].lower()):
        print(f"- {data['name']}: {data['minutes'] / 60:.2f} hours")

    weakest = min(subject_totals.values(), key=lambda item: item["minutes"])
    print(f"\nSubject with least study time: {weakest['name']} "
          f"({weakest['minutes'] / 60:.2f} hours)")

    longest = max(sessions, key=lambda session: float(session.get("duration", 0)))
    longest_minutes = float(longest.get("duration", 0))
    print(
        f"Longest single session: {longest.get('subject', '')} - "
        f"{longest.get('topic', '')} ({longest_minutes:.1f} minutes)"
    )


def save_sessions(sessions):
    """Save all sessions to study_log.txt in JSON format."""
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(sessions, file, indent=4)
        print(f"Study sessions saved to {FILE_NAME}.")
    except OSError as error:
        print(f"Could not save the study sessions: {error}")


def load_sessions():
    """Load saved sessions. Return an empty list when no file exists."""
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        print("Saved file has an unexpected format. Starting with an empty list.")
        return []

    except FileNotFoundError:
        # This is normal on the first run of the programme.
        return []
    except (json.JSONDecodeError, OSError) as error:
        print(f"Could not load the saved sessions: {error}")
        return []


def main():
    sessions = load_sessions()

    print("======================================")
    print("        SMART STUDY PLANNER")
    print("======================================")

    while True:
        print("\n1. Add a study session")
        print("2. View all sessions")
        print("3. Search sessions by subject")
        print("4. View statistics")
        print("5. Save and exit")

        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            add_session(sessions)
        elif choice == "2":
            view_sessions(sessions)
        elif choice == "3":
            search_by_subject(sessions)
        elif choice == "4":
            study_statistics(sessions)
        elif choice == "5":
            save_sessions(sessions)
            print("Thank you for using Smart Study Planner.")
            break
        else:
            print("Invalid choice. Please choose a number from 1 to 5.")


if __name__ == "__main__":
    main()
