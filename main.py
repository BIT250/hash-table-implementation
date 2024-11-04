import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from dataGenerator import DataGenerator
from reportsMaker import ReportsMaker
from tableManagement import TableManagement


# Centering function for windows
def center_window(window, width=800, height=600):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


# Function to generate persons and display charts within the window
def open_population_window():
    population_window = tk.Toplevel()
    population_window.title("Population Generation & Charts")
    population_window.configure(bg="#f2f2f2")
    center_window(population_window, width=800, height=600)

    # Main frame to hold charts and buttons
    frame = tk.Frame(population_window, bg="#f2f2f2")
    frame.pack(pady=20)

    # Function to refresh charts after generating a new population
    def generate_and_show_charts():
        input_value = simpledialog.askstring("Input", "Enter number of persons:", parent=population_window)
        if input_value and input_value.isdigit():
            number_of_persons = int(input_value)
            if number_of_persons > 0:
                generate_persons(number_of_persons)
                refresh_charts()  # Refresh charts with new data
                messagebox.showinfo("Success", "New population generated and charts updated.")
            else:
                messagebox.showerror("Invalid input", "Please enter a positive number.")
        else:
            messagebox.showerror("Invalid input", "Please enter a valid integer.")

    # Function to load and display charts
    def refresh_charts():
        # Clear previous charts
        for widget in frame.winfo_children():
            widget.destroy()

        # Display the charts as embedded figures
        plot_chart(ReportsMaker.classify_by_county, frame, "CNP Count by County", row=0, column=0, colspan=2)
        plot_chart(ReportsMaker.age_group_pie_chart, frame, "Age Group Distribution", row=1, column=0)
        plot_chart(ReportsMaker.gender_pie_chart, frame, "Gender Distribution", row=1, column=1)

        # Add a "Generate New Population" button
        new_pop_button = ttk.Button(frame, text="Generate New Population", command=generate_and_show_charts)
        new_pop_button.grid(row=2, column=0, columnspan=2, pady=20)

    # Load and display charts initially when the window opens
    refresh_charts()


# Utility function to embed a chart in a tkinter frame at specified row and column
def plot_chart(plot_function, frame, title, row, column, colspan=1):
    fig = plot_function()  # Call the plot function to create the matplotlib figure
    if fig:
        fig.suptitle(title)
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=row, column=column, columnspan=colspan, padx=10, pady=10)


# Function to open the Hash Table window
def open_hash_table_window():
    hash_table_window = tk.Toplevel()
    hash_table_window.title("Hash Table Operations")
    hash_table_window.configure(bg="#f2f2f2")
    center_window(hash_table_window, width=600, height=400)

    frame = tk.Frame(hash_table_window, bg="#f2f2f2")
    frame.pack(pady=20)

    def generate_table_with_option():
        hash_method = simpledialog.askinteger("Hash Method", "Enter hash method (1 or 2):", parent=hash_table_window)
        if hash_method in [1, 2]:
            generate_hash_table(hash_method)
            messagebox.showinfo("Success", "Hash table generated successfully!")
        elif hash_method is not None:
            messagebox.showerror("Invalid input", "Please enter 1 or 2 for hash method.")
        else:
            messagebox.showinfo("Cancelled", "Input cancelled by user.")

    # Buttons in the Hash Table window
    generate_table_button = ttk.Button(frame, text="Generate Hash Table", command=generate_table_with_option)
    generate_table_button.grid(row=0, column=0, padx=10, pady=10)


# Main functions to generate persons and hash table
def generate_persons(number_of_persons):
    print("Generating persons")
    persons = DataGenerator.generate_persons(number_of_persons)
    TableManagement.save_data(persons)
    TableManagement.generate_hash_table(1)
    print("Done")


def generate_hash_table(hash_method=1):
    print("Generating Hash Table")
    TableManagement.generate_hash_table(hash_method)
    print("Done")


# Main application window
root = tk.Tk()
root.title("Data Management Interface")
root.geometry("400x300")
root.configure(bg="#e6f7ff")

# Header label
header = tk.Label(root, text="Data Management System", font=("Helvetica", 16, "bold"), bg="#e6f7ff")
header.pack(pady=20)

# Frame for main buttons
button_frame = tk.Frame(root, bg="#e6f7ff")
button_frame.pack(pady=40, padx=20)

# Main buttons with styling
population_button = ttk.Button(button_frame, text="Open Population Window", command=open_population_window)
population_button.grid(row=0, column=0, padx=10, pady=10)

hash_table_button = ttk.Button(button_frame, text="Open Hash Table Window", command=open_hash_table_window)
hash_table_button.grid(row=1, column=0, padx=10, pady=10)

# Center the main window
center_window(root, width=400, height=300)
root.mainloop()
