import subprocess

class GitDiffParser:
    def __init__(self):
        return

    def get_staged_diff(self):
        # This method runs git diff --staged and returns raw diff string and returns None when no files staged
        try:
            diff = subprocess.run(["git", "diff", "--staged"], capture_output=True, text=True)
            return diff.stdout
        except subprocess.CalledProcessError as e:
            return None

    def parse_diff_to_chunks(self, diff_string):
        chunks = []
        current_chunk = None
        
        for line in diff_string.splitlines():
            if line.startswith("diff --git"):
                if current_chunk:
                    chunks.append(current_chunk)
                file_path = line.split(" ")[2][2:]
                current_chunk = {
                    "file_path": file_path,
                    "changes": [],
                    "additions": 0,
                    "deletions": 0
                }
            elif current_chunk:
                current_chunk["changes"].append(line)
                # Count additions/deletions
                if line.startswith("+") and not line.startswith("+++"):
                    current_chunk["additions"] += 1
                elif line.startswith("-") and not line.startswith("---"):
                    current_chunk["deletions"] += 1
        
        if current_chunk:
            chunks.append(current_chunk)
        
        # Convert changes list to string
        for chunk in chunks:
            chunk["changes"] = "\n".join(chunk["changes"])
        
        return chunks
        

# Main method
def main():
    gitDiff = GitDiffParser()
    diff_string = gitDiff.get_staged_diff()
    if diff_string:
        print(gitDiff.parse_diff_to_chunks(diff_string))
    else:
        print("No staged changes found.")
    return None

if __name__ == "__main__":
    main()
