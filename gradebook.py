import json
import os

GRADEBOOK_FILE = "gradebook.json"

def load_gradebook():
    if os.path.exists(GRADEBOOK_FILE):
        with open(GRADEBOOK_FILE, "r") as f:
            return json.load(f)
    return []

def save_gradebook(gradebook):
    with open(GRADEBOOK_FILE, "w") as f:
        json.dump(gradebook, f, indent=4)

def add_course(gradebook):
    code = input("Course code: ").strip()
    if any(course["code"] == code for course in gradebook):
        print("Course code already exists!")
        return
    name = input("Course name: ").strip()
    try:
        credits = float(input("Credits: "))
        semester = input("Semester: ").strip()
        score = float(input("Score (0-100): "))
        if not (0 <= score <= 100):
            print("Invalid score!")
            return
    except ValueError:
        print("Invalid input!")
        return
    course = {
        "code": code,
        "name": name,
        "credits": credits,
        "semester": semester,
        "score": score
    }
    gradebook.append(course)
    save_gradebook(gradebook)
    print("Course added successfully!")

def update_course(gradebook):
    code = input("Enter course code to update: ").strip()
    for course in gradebook:
        if course["code"] == code:
            course["name"] = input(f"Course name ({course['name']}): ") or course["name"]
            try:
                credits_input = input(f"Credits ({course['credits']}): ")
                course["credits"] = float(credits_input) if credits_input else course["credits"]
                score_input = input(f"Score ({course['score']}): ")
                if score_input:
                    score = float(score_input)
                    if not (0 <= score <= 100):
                        print("Invalid score!")
                        return
                    course["score"] = score
            except ValueError:
                print("Invalid input!")
                return
            course["semester"] = input(f"Semester ({course['semester']}): ") or course["semester"]
            save_gradebook(gradebook)
            print("Course updated successfully!")
            return
    print("Course not found!")

def delete_course(gradebook):
    code = input("Enter course code to delete: ").strip()
    for i, course in enumerate(gradebook):
        if course["code"] == code:
            confirm = input(f"Are you sure you want to delete {course['name']}? (y/n): ").lower()
            if confirm == "y":
                gradebook.pop(i)
                save_gradebook(gradebook)
                print("Course deleted!")
            return
    print("Course not found!")

def view_gradebook(gradebook):
    if not gradebook:
        print("Gradebook is empty!")
        return
    print(f"{'Code':<10}{'Name':<30}{'Credits':<8}{'Semester':<10}{'Score':<6}")
    print("-" * 70)
    for course in gradebook:
        print(f"{course['code']:<10}{course['name']:<30}{course['credits']:<8}{course['semester']:<10}{course['score']:<6}")

def calculate_gpa(gradebook):
    if not gradebook:
        print("Gradebook is empty!")
        return
    total_points = sum(course["score"] * course["credits"] for course in gradebook)
    total_credits = sum(course["credits"] for course in gradebook)
    overall_gpa = total_points / total_credits
    print(f"Overall GPA: {overall_gpa:.2f}")
    semesters = {}
    for course in gradebook:
        sem = course["semester"]
        if sem not in semesters:
            semesters[sem] = {"points": 0, "credits": 0}
        semesters[sem]["points"] += course["score"] * course["credits"]
        semesters[sem]["credits"] += course["credits"]
    print("GPA by semester:")
    for sem, data in semesters.items():
        gpa = data["points"] / data["credits"]
        print(f"  {sem}: {gpa:.2f}")

def main():
    gradebook = load_gradebook()
    while True:
        print("\n--- Student Gradebook CLI ---")
        print("1. Add Course")
        print("2. Update Course")
        print("3. Delete Course")
        print("4. View Gradebook")
        print("5. Calculate GPA")
        print("6. Exit")
        choice = input("Choose an option (1-6): ").strip()
        if choice == "1":
            add_course(gradebook)
        elif choice == "2":
            update_course(gradebook)
        elif choice == "3":
            delete_course(gradebook)
        elif choice == "4":
            view_gradebook(gradebook)
        elif choice == "5":
            calculate_gpa(gradebook)
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
