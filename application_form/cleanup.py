import os

# Function to recursively remove occurrences of the provided placeholder from all HTML, TS, SPEC.TS, and CSS files
def clean_project_files(directory, placeholders, extensions):
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):  # Only process specific file types
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    # Remove all placeholder texts
                    for placeholder in placeholders:
                        content = content.replace(placeholder, "")
                    # Write the updated content back to the file
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

# Define placeholders to remove
placeholders_to_remove = ["```json", "```ts", "```html", "```css", "```"]

# Define file extensions to clean
file_extensions_to_clean = [".html", ".ts", ".spec.ts", ".css"]

# Execute the function to clean up the project directory
clean_project_files("full_angular_project", placeholders_to_remove, file_extensions_to_clean)

# Confirm completion
"Placeholders removed from all relevant files successfully."
