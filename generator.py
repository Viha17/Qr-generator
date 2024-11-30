import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import qrcode
from PIL import Image, ImageTk

class BeautifulQRCodeGenerator:
    def __init__(self, master):
        self.master = master
        master.title("QR Code Generator")
        master.geometry("600x750")
        master.configure(bg="#2c3e50")  # Deep dark background

        # Create a main frame
        self.main_frame = tk.Frame(master, bg="#34495e", padx=20, pady=20)
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Title
        self.title_label = tk.Label(
            self.main_frame, 
            text="QR Code Generator", 
            font=("Segoe UI", 18, "bold"),
            bg="#34495e", 
            fg="#ecf0f1"
        )
        self.title_label.pack(pady=(0, 20))

        # URL Input Frame
        self.input_frame = tk.Frame(self.main_frame, bg="#34495e")
        self.input_frame.pack(fill=tk.X, pady=10)

        # URL Label
        self.url_label = tk.Label(
            self.input_frame, 
            text="Enter URL:", 
            font=("Segoe UI", 12),
            bg="#34495e", 
            fg="#bdc3c7"
        )
        self.url_label.pack(side=tk.TOP, anchor='w')

        # URL Entry with custom style
        style = ttk.Style()
        style.configure("Custom.TEntry", 
                        foreground="#2c3e50",
                        background="#ecf0f1",
                        font=("Segoe UI", 12))
        
        self.url_entry = ttk.Entry(
            self.input_frame, 
            width=50, 
            style="Custom.TEntry"
        )
        self.url_entry.pack(fill=tk.X, pady=(5, 10))
        self.url_entry.bind('<KeyRelease>', self.generate_qr)

        # QR Code Display Frame
        self.qr_frame = tk.Frame(self.main_frame, bg="#34495e", bd=10)
        self.qr_frame.pack(pady=10)

        # QR Code Label with a subtle border effect
        self.qr_label = tk.Label(
            self.qr_frame, 
            bg="#2c3e50", 
            width=300, 
            height=300
        )
        self.qr_label.pack()

        # Button Frame
        self.button_frame = tk.Frame(self.main_frame, bg="#34495e")
        self.button_frame.pack(pady=10)

        # Save Button with custom style
        self.save_button = tk.Button(
            self.button_frame, 
            text="Save QR Code", 
            command=self.save_qr,
            font=("Segoe UI", 12, "bold"),
            bg="#3498db",  # Bright blue
            fg="white",
            activebackground="#2980b9",
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        self.save_button.pack(side=tk.LEFT, padx=10)

        # Initialize QR Code generator
        self.qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        # Placeholder message
        self.placeholder_text = tk.Label(
            self.qr_label, 
            text="Your QR Code will appear here",
            font=("Segoe UI", 12),
            bg="#2c3e50", 
            fg="#7f8c8d"
        )
        self.placeholder_text.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def generate_qr(self, event=None):
        # Remove placeholder
        self.placeholder_text.place_forget()

        # Clear previous QR code
        self.qr.clear()

        # Get URL from entry
        url = self.url_entry.get()

        # Check if URL is not empty
        if url:
            try:
                # Add data to QR code
                self.qr.add_data(url)
                self.qr.make(fit=True)

                # Create an image from the QR Code with a gradient-like effect
                qr_image = self.qr.make_image(
                    fill_color="#2c3e50",  # Dark background color for QR code
                    back_color="#ecf0f1"   # Light background for contrast
                )

                # Resize image to fit in the window
                qr_image = qr_image.resize((300, 300), Image.LANCZOS)

                # Convert to PhotoImage
                self.photo = ImageTk.PhotoImage(qr_image)

                # Update label with new QR code
                self.qr_label.configure(image=self.photo)
                self.qr_label.image = self.photo
            except Exception as e:
                messagebox.showerror("Error", f"Could not generate QR code: {str(e)}")

    def save_qr(self):
        # Check if QR code exists
        url = self.url_entry.get()
        if not url:
            messagebox.showwarning("Warning", "Please enter a URL first")
            return

        # Open save dialog
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
            )
            
            if file_path:
                # Generate and save QR code
                self.qr.clear()
                self.qr.add_data(url)
                self.qr.make(fit=True)
                qr_image = self.qr.make_image(
                    fill_color="#2c3e50",  # Dark QR code color
                    back_color="#ecf0f1"   # Light background
                )
                qr_image.save(file_path)
                messagebox.showinfo("Success", f"QR Code saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save QR code: {str(e)}")

def main():
    root = tk.Tk()
    root.resizable(False, False)  # Prevent window resizing
    qr_generator = BeautifulQRCodeGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()

# Required libraries:
# pip install qrcode pillow