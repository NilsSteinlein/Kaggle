from github import Github
import os
import base64

# Initialize GitHub API
g = Github(os.getenv('GITHUB_TOKEN'))
repo = g.get_repo(f"{os.getenv('GITHUB_REPOSITORY')}")

def list_notebooks():
    """
    List all Jupyter notebooks in the repository.
    Returns a Markdown list of links to the notebooks.
    """
    notebooks = []
    contents = repo.get_contents("")  # Start at repo root
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        elif file_content.path.endswith(".ipynb"):
            notebooks.append(f"[{file_content.name}]({file_content.html_url})")
    
    return "\n".join(notebooks)

def update_readme(notebooks_list):
    """
    Update the README.md file with the provided list of notebooks.
    """
    readme_path = "README.md"
    content_file = repo.get_contents(readme_path)
    readme_content = content_file.decoded_content.decode("utf-8")

    # Define the markers
    start_marker = "<!-- PROJECTS-START -->"
    end_marker = "<!-- PROJECTS-END -->"

    # Find the location of the markers
    start_index = readme_content.find(start_marker) + len(start_marker)
    end_index = readme_content.find(end_marker)

    # Construct the new README content
    new_readme_content = (readme_content[:start_index] + "\n" + notebooks_list + "\n" + readme_content[end_index:])

    # Update the README file
    repo.update_file(content_file.path, "Update projects list in README", new_readme_content, content_file.sha)

# Get the list of notebooks and update the README
notebooks_list = list_notebooks()
update_readme(notebooks_list)
