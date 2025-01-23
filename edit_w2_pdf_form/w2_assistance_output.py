
import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


def create_fillable_pdf(json_data, output_file):
    c = canvas.Canvas(output_file, pagesize=letter)
    # pdfmetrics.registerFont(TTFont('Helvetica', 'Helvetica.ttf'))  # Register font if needed

    # Title (Static)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, json_data["form_title"])
    
    # Loop through each field in the JSON data
    for field in json_data["fields"]:
        x = field["position"]["x"]
        y = field["position"]["y"]
        width = field["position"]["width"]
        height = field["position"]["height"]

        # Draw the label
        c.setFont("Helvetica", 10)
        c.drawString(x, y + height + 2, field["label"])

        # Create the appropriate field type
        if field["type"] == "text":
            c.acroForm.textfield(name=field["id"], x=x, y=y, width=width, height=height,
                                  tooltip=field["placeholder"], borderStyle='bevelled', 
                                  forceBorder=True, borderColor=colors.black, 
                                  fillColor=colors.white, textColor=colors.black)
        elif field["type"] == "number":
            c.acroForm.textfield(name=field["id"], x=x, y=y, width=width, height=height,
                                  tooltip=field["placeholder"], borderStyle='bevelled', 
                                  forceBorder=True, borderColor=colors.black,
                                  fillColor=colors.white, textColor=colors.black)
        # Add other types as needed (e.g., checkboxes, dropdowns)

    c.save()


# Sample JSON data structure (you can read this from a file instead)
sample_json = '''{
  "form_title": "IRS Form W-2 (Page 2)",
  "fields": [
    {
      "id": "employee_ssn",
      "label": "Employee's Social Security Number",
      "type": "text",
      "placeholder": "XXX-XX-XXXX",
      "position": { "x": 50, "y": 700, "width": 250, "height": 20 }
    },
    {
      "id": "employer_ein",
      "label": "Employer Identification Number (EIN)",
      "type": "text",
      "placeholder": "XX-XXXXXXX",
      "position": { "x": 320, "y": 700, "width": 250, "height": 20 }
    },
    {
      "id": "employer_name_address",
      "label": "Employer's Name, Address, and ZIP Code",
      "type": "text",
      "placeholder": "Enter employer details",
      "position": { "x": 50, "y": 660, "width": 520, "height": 20 }
    },
    {
      "id": "control_number",
      "label": "Control Number",
      "type": "text",
      "placeholder": "Enter control number",
      "position": { "x": 50, "y": 600, "width": 250, "height": 20 }
    },
    {
      "id": "employee_name",
      "label": "Employee's Name",
      "type": "text",
      "placeholder": "Enter first and last name",
      "position": { "x": 320, "y": 600, "width": 250, "height": 20 }
    },
    {
      "id": "employee_address",
      "label": "Employee's Address and ZIP Code",
      "type": "text",
      "placeholder": "Enter address details",
      "position": { "x": 50, "y": 560, "width": 520, "height": 20 }
    },
    {
      "id": "wages_tips",
      "label": "Wages, Tips, Other Compensation",
      "type": "number",
      "placeholder": "Enter amount",
      "position": { "x": 50, "y": 510, "width": 250, "height": 20 }
    },
    {
      "id": "federal_income_tax",
      "label": "Federal Income Tax Withheld",
      "type": "number",
      "placeholder": "Enter amount",
      "position": { "x": 320, "y": 510, "width": 250, "height": 20 }
    },
    {
      "id": "social_security_wages",
      "label": "Social Security Wages",
      "type": "number",
      "placeholder": "Enter amount",
      "position": { "x": 50, "y": 470, "width": 250, "height": 20 }
    },
    {
      "id": "social_security_tax",
      "label": "Social Security Tax Withheld",
      "type": "number",
      "placeholder": "Enter amount",
      "position": { "x": 320, "y": 470, "width": 250, "height": 20 }
    },
    {
      "id": "medicare_wages",
      "label": "Medicare Wages and Tips",
      "type": "number",
      "placeholder": "Enter amount",
      "position": { "x": 50, "y": 430, "width": 250, "height": 20 }
    },
    {
      "id": "medicare_tax",
      "label": "Medicare Tax Withheld",
      "type": "number",
      "placeholder": "Enter amount",
      "position": { "x": 320, "y": 430, "width": 250, "height": 20 }
    },
    {
      "id": "state_id_number",
      "label": "State Employer’s State ID Number",
      "type": "text",
      "placeholder": "Enter state ID number",
      "position": { "x": 50, "y": 390, "width": 250, "height": 20 }
    },
    {
      "id": "state_wages",
      "label": "State Wages, Tips, etc.",
      "type": "number",
      "placeholder": "Enter amount",
      "position": { "x": 320, "y": 390, "width": 250, "height": 20 }
    },
    {
      "id": "state_income_tax",
      "label": "State Income Tax",
      "type": "number",
      "placeholder": "Enter amount",
      "position": { "x": 50, "y": 350, "width": 250, "height": 20 }
    },
    {
      "id": "local_wages",
      "label": "Local Wages, Tips, etc.",
      "type": "number",
      "placeholder": "Enter amount",
      "position": { "x": 320, "y": 350, "width": 250, "height": 20 }
    },
    {
      "id": "local_income_tax",
      "label": "Local Income Tax",
      "type": "number",
      "placeholder": "Enter amount",
      "position": { "x": 50, "y": 310, "width": 250, "height": 20 }
    },
    {
      "id": "locality_name",
      "label": "Locality Name",
      "type": "text",
      "placeholder": "Enter locality name",
      "position": { "x": 320, "y": 310, "width": 250, "height": 20 }
    }
  ]
}
'''

# Load the JSON data (you can read from 'w2.json' file)
data = json.loads(sample_json)

# Create the fillable PDF form
create_fillable_pdf(data, 'dpa_fillable_form.pdf')
