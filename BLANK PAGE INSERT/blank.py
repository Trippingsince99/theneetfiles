import os
from tkinter import Tk, Label, Button, filedialog, Radiobutton, IntVar, messagebox
from PyPDF2 import PdfReader, PdfWriter

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

        messagebox.showinfo("Success", f"PDF saved successfully at {output_file}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def select_pdf():
    file_path = filedialog.askopenfilename(
        title="Select PDF File",
        filetypes=[("PDF Files", "*.pdf")]
    )
    if file_path:
        lbl_selected_file.config(text=os.path.basename(file_path))
        return file_path
    return None


def save_pdf(input_file, option):
    if not input_file:
        messagebox.showerror("Error", "Please select a PDF file first!")
        return

    output_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")],
        title="Save Modified PDF"
    )

    if output_path:
        add_blank_pages(input_file, output_path, option)


# Initialize Tkinter
root = Tk()
root.title("PDF Blank Page Inserter")
root.geometry("400x350")

# Variables
selected_file = None
option_var = IntVar(value=1)  # Default option: After odd pages

# UI Elements
Label(root, text="PDF Blank Page Inserter", font=("Arial", 16)).pack(pady=10)

btn_select_file = Button(root, text="Select PDF File", command=lambda: globals().update({"selected_file": select_pdf()}))
btn_select_file.pack(pady=5)

lbl_selected_file = Label(root, text="No file selected", fg="gray")
lbl_selected_file.pack(pady=5)

Label(root, text="Choose where to add blank pages:").pack(pady=10)

Radiobutton(root, text="After Every Odd Page", variable=option_var, value=1).pack()
Radiobutton(root, text="After Every Even Page", variable=option_var, value=2).pack()
Radiobutton(root, text="After Every Page", variable=option_var, value=3).pack()

btn_save_pdf = Button(root, text="Save Modified PDF", command=lambda: save_pdf(selected_file, option_var.get()))
btn_save_pdf.pack(pady=20)

# Run Tkinter loop
root.mainloop()
