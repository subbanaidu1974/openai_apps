import os
import zipfile
import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# Load the JSON schema again
json_path = "angular_app2/output.json"
with open(json_path, "r") as file:
    form_json = json.load(file)


os.environ['OPENAI_API_KEY'] = "<api key>"

# Load OpenAI API Key
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI GPT-4-turbo model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, openai_api_key=openai_api_key)

# Define the Angular project directory
angular_project_dir = "angular_app2/full_angular_project"
os.makedirs(angular_project_dir, exist_ok=True)

# Define required Angular files
angular_files = {
    "src/main.ts": "Main entry point for Angular application",
    "src/index.html": "HTML entry point for Angular application",
    "src/polyfills.ts": "Angular Polyfills",
    "src/environments/environment.ts": "Development environment settings",
    "src/environments/environment.prod.ts": "Production environment settings",
    "tsconfig.json": "TypeScript configuration",
    "tsconfig.app.json": "TypeScript config for Angular",
    "tsconfig.spec.json": "Testing TypeScript configuration",
    "karma.conf.js": "Karma configuration for testing",
    "src/test.ts": "Entry file for testing",
    "angular.json": "Angular project configuration",
    "package.json": "Node package configuration",
    "src/assets/.gitkeep": "Assets directory placeholder",
    "src/app/app.module.ts": "Main Angular module",
    "src/app/app-routing.module.ts": "Angular routing module",
    "src/app/app.component.ts": "Root application component",
    "src/app/app.component.html": "Root application HTML",
    "src/app/app.component.css": "Root application CSS",
    "src/app/app.component.spec.ts": "Root application test file",
    "src/app/home/home.component.ts": "Home Page Component",
    "src/app/home/home.component.html": "Home Page HTML with navigation links",
    "src/app/home/home.component.css": "Home Page CSS"
}

# Generate individual components for each section in the JSON file and add them to routing
routes = []
for section in form_json.keys():
    component_name = section.lower().replace(" ", "-")
    component_class = section + "Component"
    angular_files[f"src/app/{component_name}/{component_name}.component.ts"] = f"Component for {section} section"
    angular_files[f"src/app/{component_name}/{component_name}.component.html"] = f"HTML for {section} component"
    angular_files[f"src/app/{component_name}/{component_name}.component.css"] = f"CSS for {section} component"
    angular_files[f"src/app/{component_name}/{component_name}.component.spec.ts"] = f"Test file for {section} component"
    routes.append({
        "path": component_name,
        "component": component_class
    })

# Add the Home Page route
routes.insert(0, {"path": "", "component": "HomeComponent"})

# Function to generate Angular code
def generate_angular_file(file_name, file_type, extra_data=None):
    """Generates a specific Angular file dynamically."""
    
    messages = [
        SystemMessage(content="You are an expert Angular developer generating structured, compilable Angular code dynamically."),
        HumanMessage(content=f"""
        Generate a **{file_type}** file for an Angular 16+ application.
        - Ensure it follows best practices and is fully compilable.
        - If it is a component, implement Reactive Forms based on the JSON schema.
        - If it is a module, ensure it imports necessary dependencies.
        - If it is a routing module, properly define all routes.

        Extra Data (if applicable):
        ```json
        {json.dumps(extra_data, indent=4) if extra_data else ""}
        ```

        Provide the complete code for `{file_name}`.
        """)
    ]

    response = llm.invoke(messages)
    return response.content

# Generate files dynamically
for file_path, file_type in angular_files.items():
    print(f"Generating {file_path}...")
    file_content = generate_angular_file(file_path, file_type, routes if "routing" in file_path else None)
    full_path = os.path.join(angular_project_dir, file_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    with open(full_path, "w") as f:
        f.write(file_content)

# Create a ZIP file for the complete Angular project
zip_file_path = "angular_app2/full_angular_project.zip"
with zipfile.ZipFile(zip_file_path, 'w') as zipf:
    for root, _, files in os.walk(angular_project_dir):
        for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path, os.path.relpath(file_path, angular_project_dir))

# Return the ZIP file path
zip_file_path
