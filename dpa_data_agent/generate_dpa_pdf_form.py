import json
from fpdf import FPDF

# Sample JSON structure
json_data = '''
{
  "title": "Downpayment Assistance Form",
  "fields": [
    {
      "label": "Full Name",
      "type": "text",
      "x": 10,
      "y": 40,
      "width": 90,
      "value": "John Doe"
    },
    {
      "label": "Email",
      "type": "text",
      "x": 10,
      "y": 55,
      "width": 90,
      "value": "john.doe@example.com"
    },
    {
      "label": "Phone Number",
      "type": "text",
      "x": 10,
      "y": 70,
      "width": 90,
      "value": "123-456-7890"
    },
    {
      "label": "Loan Officer Name",
      "type": "text",
      "x": 10,
      "y": 85,
      "width": 90,
      "value": "Sarah Smith"
    },
    {
      "label": "Loan Amount",
      "type": "text",
      "x": 10,
      "y": 100,
      "width": 90,
      "value": "$250,000"
    },
    {
      "label": "Loan Program",
      "type": "text",
      "x": 10,
      "y": 115,
      "width": 90,
      "value": "FHA"
    },
    {
      "label": "Program Name",
      "type": "text",
      "x": 10,
      "y": 130,
      "width": 90,
      "value": "Local Downpayment Assistance Program"
    },
    {
      "label": "Eligibility Criteria",
      "type": "text",
      "x": 10,
      "y": 145,
      "width": 90,
      "value": "Income below $50,000"
    },
    {
      "label": "Assistance Amount",
      "type": "text",
      "x": 10,
      "y": 160,
      "width": 90,
      "value": "$10,000"
    },
    {
      "label": "First-Time Homebuyer",
      "type": "checkbox",
      "x": 10,
      "y": 180,
      "width": 5,
      "height": 5,
      "value": true
    }
  ],
  "submit_button": {
    "label": "Submit",
    "x": 80,
    "y": 210,
    "width": 20,
    "height": 5
  }
}
'''

# Load JSON data
data = json.loads(json_data)

# Create PDF
pdf = FPDF()
pdf.add_page()

# Title
pdf.set_font("Arial", 'B', 16)
pdf.set_fill_color(200, 220, 255)  # Light blue background
pdf.cell(0, 10, data['title'], 0, 1, 'C', 1)

# Add fields
pdf.set_font("Arial", '', 12)
for field in data['fields']:
    if field['type'] == 'text':
        pdf.set_xy(field['x'], field['y'])
        pdf.cell(field['width'], 10, field['label'] + ':', 0, 0)
        pdf.rect(field['x'] + field['width'], field['y'], 90, 10)  # Draw text box
        pdf.set_xy(field['x'] + field['width'] + 1, field['y'] + 1)
        pdf.cell(88, 8, field['value'], 0, 0)  # Display value
    elif field['type'] == 'checkbox':
        pdf.set_xy(field['x'], field['y'])
        pdf.cell(5, 5, '', 1)  # Draw checkbox
        if field['value']:
            pdf.set_xy(field['x'] + 1, field['y'] + 1)
            pdf.cell(3, 3, 'X', 0)  # Mark checkbox as checked
        pdf.set_xy(field['x'] + 10, field['y'])
        pdf.cell(0, 5, field['label'], 0, 0)

# Submit button
submit_button = data['submit_button']
pdf.set_xy(submit_button['x'], submit_button['y'])
pdf.set_fill_color(255, 200, 200)  # Light red background
pdf.rect(submit_button['x'], submit_button['y'], submit_button['width'], submit_button['height'], 'F')
pdf.set_xy(submit_button['x'] + 1, submit_button['y'] + 1)
pdf.set_font("Arial", 'B', 10)
pdf.cell(submit_button['width'] - 2, submit_button['height'] - 2, submit_button['label'], 0, 0, 'C')

# Save PDF
pdf.output('generated_dpa_data_form.pdf')
