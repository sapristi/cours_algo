from pathlib import Path
import json
import argparse

def remove_solutions(notebook: Path):
    data = json.loads(notebook.read_text())
    for cell in data["cells"]:
        source_treated = []
        is_removed = False
        for line in cell["source"]:
            if "#BEGIN" in line:
                is_removed = True
            if not is_removed:
                source_treated.append(line)
            if "#END" in line:
                is_removed = False
        cell["source"] = source_treated
    notebook.write_text(json.dumps(data))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dir")
    args = parser.parse_args()
    target_dir = Path(args.dir)

    notebooks = target_dir.glob("**/*.ipynb")

    for notebook in notebooks:
        print(f"treating notebook {notebook}")
        remove_solutions(notebook)
