from flask import Flask, request, jsonify, render_template, send_file
import os
from PyPDF2 import PdfReader, PdfWriter

app = Flask(__name__)

# Function to add blank pages to a PDF
def add_blank_pages(input_file, output_file, option):
    try:
        reader = PdfReader(input_file)
        writer = PdfWriter()

        for i, page in enumerate(reader.pages):
            writer.add_page(page)
            if option == 1 and (i + 1) % 2 != 0:  # After odd pages
                writer.add_blank_page()
            elif option == 2 and (i + 1) % 2 == 0:  # After even pages
                writer.add_blank_page()
            elif option == 3:  # After every page
                writer.add_blank_page()

        with open(output_file, "wb") as output_pdf:
            writer.write(output_pdf)

        return "success"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Landing page
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# Route for PDF Blank Page Inserter
@app.route("/blank_page_inserter", methods=["GET", "POST"])
def blank_page_inserter():
    if request.method == "GET":
        return render_template("blank_page_inserter.html")
    elif request.method == "POST":
        if "pdf_file" not in request.files or request.files["pdf_file"].filename == "":
            return jsonify({"error": "No file uploaded or selected"}), 400

        pdf_file = request.files["pdf_file"]
        option = int(request.form.get("option", 0))
        custom_name = request.form.get("custom_name", "").strip()

        upload_folder = "uploads"
        output_folder = "outputs"
        os.makedirs(upload_folder, exist_ok=True)
        os.makedirs(output_folder, exist_ok=True)

        input_path = os.path.join(upload_folder, pdf_file.filename)
        output_path = os.path.join(output_folder, f"{custom_name}.pdf")

        pdf_file.save(input_path)

        result = add_blank_pages(input_path, output_path, option)

        if result == "success":
            return send_file(output_path, as_attachment=True)
        else:
            return jsonify({"error": result}), 500

# Placeholder routes for other tools
@app.route("/fill_in_blanks", methods=["GET"])
def fill_in_blanks():
    return render_template("fill_in_blanks.html")

@app.route("/pdf_splitter", methods=["GET"])
def pdf_splitter():
    return render_template("pdf_splitter.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
