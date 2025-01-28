from flask import Flask, request, jsonify, render_template, send_file
import os
from PyPDF2 import PdfReader, PdfWriter

app = Flask(__name__)

# Function to add blank pages to a PDF
def add_blank_pages(input_file, output_file, option, range_start, range_end, interval):
    try:
        reader = PdfReader(input_file)
        writer = PdfWriter()

        # Get the total number of pages
        total_pages = len(reader.pages)
        range_start = max(1, range_start or 1)
        range_end = min(total_pages, range_end or total_pages)

        # Iterate through pages
        for i, page in enumerate(reader.pages):
            writer.add_page(page)
            page_number = i + 1  # Page numbers start at 1

            # Add blank page based on user choice
            if range_start <= page_number <= range_end:
                if option == 1 and page_number % interval == 0:  # Add every N pages
                    writer.add_blank_page()
                elif option == 2:  # Add after all pages in the range
                    writer.add_blank_page()

        with open(output_file, "wb") as output_pdf:
            writer.write(output_pdf)

        return "success"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Route to render the upload form
@app.route("/", methods=["GET"])
def home():
    return render_template("upload.html")

# Route to handle PDF processing
@app.route("/process", methods=["POST"])
def process_pdf():
    try:
        # Validate if file exists
        if "pdf_file" not in request.files or request.files["pdf_file"].filename == "":
            return jsonify({"error": "No file uploaded or selected"}), 400

        pdf_file = request.files["pdf_file"]
        option = int(request.form.get("option", 0))
        custom_name = request.form.get("custom_name", "").strip()
        range_start = request.form.get("range_start", type=int)
        range_end = request.form.get("range_end", type=int)
        interval = request.form.get("interval", type=int, default=1)

        # Validate inputs
        if not custom_name:
            return jsonify({"error": "Custom file name is required"}), 400
        if option not in [1, 2]:
            return jsonify({"error": "Invalid option selected"}), 400
        if interval < 1:
            return jsonify({"error": "Interval must be greater than or equal to 1"}), 400

        # Prepare file paths
        upload_folder = "uploads"
        output_folder = "outputs"
        os.makedirs(upload_folder, exist_ok=True)
        os.makedirs(output_folder, exist_ok=True)

        input_path = os.path.join(upload_folder, pdf_file.filename)
        output_path = os.path.join(output_folder, f"{custom_name}.pdf")

        # Save the uploaded file temporarily
        pdf_file.save(input_path)

        # Process the PDF file
        result = add_blank_pages(input_path, output_path, option, range_start, range_end, interval)

        if result == "success":
            return send_file(output_path, as_attachment=True)
        else:
            return jsonify({"error": result}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
