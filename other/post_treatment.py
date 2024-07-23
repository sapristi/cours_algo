from pathlib import Path
import json
import argparse

def remove_solutions(notebook: Path):
    data = json.loads(notebook.read_text())
    for cell in data["cells"]:
        if not cell["cell_type"] == "code":
            continue
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
        cell["outputs"] = []
    notebook.write_text(json.dumps(data))



def insert_clear_button(notebook: Path, root_dir: Path):
    notebook_rel = notebook.relative_to(root_dir)
    html = f"""<button type="button" id="button_for_indexeddb">Clear notebook {notebook_rel}</button>
    <script>
    window.button_for_indexeddb.onclick = function(e) {{
        window.indexedDB.open('JupyterLite Storage').onsuccess = function(e) {{
            let tables = ["checkpoints", "files"];
            let t = e.target.result.transaction(tables, "readwrite");
            function clearNotenook(tablename) {{
                t.objectStore(tablename).delete('{notebook_rel}').onsuccess = function(e) {{
                    console.log("Deleted {notebook_rel} state in " + tablename + " (" + e.target.result + ")");
                }}
            }}
            for (let tablename of tables) {{
                clearNotenook(tablename);
            }}
        }}
    }};
    </script>""".replace("\n", "")
    cell_source = f"""from IPython.display import display, HTML
display(HTML(\"\"\"{html}\"\"\"))"""
    cell = {
        "cell_type": "code",
        "source": cell_source
    }

    data = json.loads(notebook.read_text())
    data["cells"].insert(0, cell)
    notebook.write_text(json.dumps(data))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dir")
    args = parser.parse_args()
    root_dir = Path(args.dir)

    notebooks = root_dir.glob("**/*.ipynb")

    for notebook in notebooks:
        if ".ipynb_checkpoints" in notebook.parts:
            continue
        print(f"treating notebook {notebook}")
        remove_solutions(notebook)
        insert_clear_button(notebook, root_dir)
