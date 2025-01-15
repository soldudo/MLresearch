import os
import subprocess
import sys

def run_cypher_scripts(neo4j_user, neo4j_password, folder_path):
  
    if not os.path.isdir(folder_path):
        print(f"Error: The folder {folder_path} does not exist.")
        sys.exit(1)

    # Collect all files ending with "_cypher.csv" (or adjust if needed).
    all_cypher_files = [
        f for f in os.listdir(folder_path) 
        if f.endswith("_cypher.csv")
    ]

    if not all_cypher_files:
        print(f"No files matching '*_cypher.csv' were found in {folder_path}.")
        return

    # Separate node files from edge files.
    node_files = sorted([f for f in all_cypher_files if f.startswith("nodes_")])
    edge_files = sorted([f for f in all_cypher_files if f.startswith("edges_")])

    # neo4j requires nodes imported prior to edges
    files_ordered = node_files + edge_files

    print("Node files to process first:", node_files)
    print("Edge files to process second:", edge_files)
    print("------------------------------------------")

    # Loop through the selected files in order.
    for filename in files_ordered:
        full_path = os.path.join(folder_path, filename)
        print(f"Running Cypher from: {full_path}")

        with open(full_path, "r", encoding="utf-8") as f:
            cypher_commands = f.read()

        # Run `cypher-shell` with the file content as stdin.
        process = subprocess.run(
            [
                "cypher-shell",
                "-u", neo4j_user,
                "-p", neo4j_password
            ],
            input=cypher_commands.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if process.returncode != 0:
            print(f"[ERROR] Error running {filename}:")
            print(process.stderr.decode("utf-8"))
            # uncomment below to exit on error instead of continuing to next file
            # sys.exit(1)
        else:
            print(process.stdout.decode("utf-8"))

    print("cypher scripts completed.")

if __name__ == "__main__":
    # Neo4j credentials
    NEO4J_USER = "neo4j"
    NEO4J_PASSWORD = "PASSWORD"

    FOLDER_PATH = "/var/lib/neo4j/import"

    run_cypher_scripts(NEO4J_USER, NEO4J_PASSWORD, FOLDER_PATH)
