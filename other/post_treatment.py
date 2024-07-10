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



def insert_clear_button(notebook: Path):
    html = f"""
    <button type="button" id="button_for_indexeddb">Clear notebook {notebook}</button>
    <script>
    window.button_for_indexeddb.onclick = function(e) {{
        window.indexedDB.open('JupyterLite Storage').onsuccess = function(e) {{
            // There are also other tables that I'm not clearing:
            // "counters", "settings", "local-storage-detect-blob-support"
            let tables = ["checkpoints", "files"];

            let db = e.target.result;
            let t = db.transaction(tables, "readwrite");

            function clearNotenook(tablename) {{
                let st = t.objectStore(tablename);
                st.delete(notebookName).onsuccess = function(e) {{
                    console.log("Deleted {notebook} state in " + tablename + " (" + e.target.result + ")");
                }}
            }}

            for (let tablename of tables) {{
                clearTable(tablename);
            }}
        }}
    }};
    </script>
    """
    cell_source = f"""
    from IPython.display import display, HTML
    display(HTML({html}))
    """
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
    target_dir = Path(args.dir)

    notebooks = target_dir.glob("**/*.ipynb")

    for notebook in notebooks:
        print(f"treating notebook {notebook}")
        remove_solutions(notebook)
        insert_clear_button(notebook)
