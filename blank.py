from flask import Flask, request, jsonify, render_template
import os
from PyPDF2 import PdfReader, PdfWriter
import webbrowser

app = Flask(__name__)

# Function to add blank pages to a PDF
def add_blank_pages(input_file, output_file, option):
    try:
        reader = PdfReader(input_file)
        writer = PdfWriter()

        # Iterate through each page
        for i, page in enumerate(reader.pages):
            writer.add_page(page)
            # Add blank page based on user choice
            if option == 1 and (i + 1) % 2 != 0:  # After odd pages
                writer.add_blank_page()
            elif option == 2 and (i + 1) % 2 == 0:  # After even pages
                writer.add_blank_page()
            elif option == 3:  # After every page
                writer.add_blank_page()

        with open(output_file, "wb") as output_pdf:
            writer.write(output_pdf)

        return "PDF processed successfully!"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Route to render the upload form
@app.route("/", methods=["GET"])
def home():
    return render_template("upload.html")

# Route to handle PDF processing
@app.route("/process", methods=["POST"])
def process_pdf():
    if "pdf_file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    pdf_file = request.files["pdf_file"]
    option = int(request.form["option"])  # Get the selected option
    custom_folder = request.form["custom_folder"]  # Custom folder path
    custom_name = request.form["custom_name"]  # Custom file name

    if pdf_file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Ensure the custom folder exists
    os.makedirs(custom_folder, exist_ok=True)

    # Save the uploaded file temporarily
    input_path = os.path.join(custom_folder, pdf_file.filename)
    output_path = os.path.join(custom_folder, f"{custom_name}.pdf")

    pdf_file.save(input_path)

    # Process the file
    result = add_blank_pages(input_path, output_path, option)

    if "successfully" in result:
        # Open the custom folder automatically
        webbrowser.open(custom_folder)
        return jsonify({"message": result, "output_file": output_path}), 200
    else:
        return jsonify({"error": result}), 500

# Main function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
