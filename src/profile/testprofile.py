from fpdf import FPDF
import os

python_files = ["models.py", "schemas.py", "services.py", "views.py", "enums.py"]  # Add your file names here

# Create a PDF instance
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=10)
pdf.set_font("Courier", size=12)

# Loop through each file and add its content to the PDF
for py_file in python_files:
    pdf.add_page()  # Add a new page for each file
    pdf.set_font("Courier", size=12)
    pdf.cell(0, 10, f"File: {py_file}", ln=True, align='C')  # Add file title

    # Open and read the Python file
    with open(py_file, "r") as file:
        lines = file.readlines()

    # Write each line of the file to the PDF
    for line in lines:
        pdf.multi_cell(0, 10, line)

# Save the PDF
output_filename = "profilefiles1.pdf"
pdf.output(output_filename)
print(f"PDF created: {output_filename}")
