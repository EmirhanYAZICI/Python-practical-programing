import os

IGNORE_DIRS = {".git", ".github", ".vscode", "__pycache__", "venv", ".venv"}
REPO_URL = "[https://github.com/EmirhanYAZICI/Python-practical-programming.git](https://github.com/EmirhanYAZICI/Python-practical-programming.git)"
BT = "`" * 3

def get_projects():
    return sorted(
        d for d in os.listdir(".")
        if os.path.isdir(d) and d not in IGNORE_DIRS and not d.startswith(".")
    )

def get_description(folder):
    readme_path = os.path.join(folder, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    return line
    return "-"

def build_tree(projects):
    lines = ["Python-practical-programming/"]
    for p in projects:
        lines.append(f"├── {p}/")
        files = sorted(
            f for f in os.listdir(p)
            if not f.startswith(".") and f != "__pycache__"
        )
        for i, fname in enumerate(files):
            prefix = "└── " if i == len(files) - 1 else "├── "
            lines.append(f"│   {prefix}{fname}")
    lines.append("└── README.md")
    return "\n".join(lines)

def main():
    projects = get_projects()
    rows = []
    for idx, p in enumerate(projects, start=1):
        num = p.split("-")[0] if "-" in p and p.split("-")[0].isdigit() else f"{idx:02d}"
        desc = get_description(p)
        rows.append(f"| {num} | [{p}](./{p}) | {desc} |")

    table = "\n".join(rows) if rows else "| - | - | - |"
    tree = build_tree(projects)

    content = (
        "# Python Practical Programming\n\n"
        "A collection of small, practical Python projects and data analysis exercises kept in a single, organized repository.\n\n"
        "## Projects\n\n"
        "| # | Project | Description |\n"
        "| :--- | :--- | :--- |\n"
        f"{table}\n\n"
        "## Structure\n\n"
        f"{BT}text\n"
        f"{tree}\n"
        f"{BT}\n\n"
        "## Usage\n\n"
        f"{BT}bash\n"
        f"git clone {REPO_URL}\n"
        "cd Python-practical-programming\n"
        f"{BT}\n"
    )
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    main()