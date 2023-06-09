import pandas as pd
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor

# Read the dataset
dataset = pd.read_csv("cleaned_Crop_data.csv")

# Create a GUI using Tkinter
window = tk.Tk()
window.title("Crop Production Prediction")
window.geometry("400x400")


# Function to update the crop dropdown based on the selected state
def update_crop_dropdown(*args):
    selected_state = state_dropdown.get()

    # Filter dataset based on the selected state
    crop_options = dataset.loc[dataset['State_Name'] == selected_state, 'Crop'].unique().tolist()

    # Clear and update the crop dropdown options
    crop_dropdown['values'] = crop_options
    crop_dropdown.set("")  # Clear the currently selected value


# Function to predict production based on the selected state, crop, area, and rainfall
def predict_production():
    state = state_dropdown.get()
    crop = crop_dropdown.get()
    area = float(entry_area.get())
    rainfall = float(entry_rainfall.get())

    # Filter data for selected state, crop, and year
    State_data = dataset.query(f"State_Name == '{state}'")
    State_data = State_data.query(f"Crop == '{crop}'")

    # Select features and target
    X = State_data[["Crop_Year", "Area", "Annual_Rainfall"]]
    Y = State_data["Production"]

    # Split data into training and testing sets
    xtrain, xtest, ytrain, ytest = train_test_split(X, Y, random_state=12, train_size=0.7)

    # Create a KNN regression model with k=5
    knn_model = KNeighborsRegressor()

    # Train the model on the training data
    knn_model.fit(xtrain, ytrain)

    # Make a prediction
    prediction = knn_model.predict([[2023, area, rainfall]])  # Example: Use the year 2023 for prediction

    # Update the output label with the prediction result
    output_label.configure(text=f"Predicted Production: {prediction[0]} tonnes")


# Function to submit the prediction
def submit_prediction():
    if not state_dropdown.get() or not crop_dropdown.get() or not entry_area.get() or not entry_rainfall.get():
        messagebox.showwarning("Error", "Please fill in all the fields.")
    else:
        predict_production()


# Function to clear/reset the input fields
def clear_fields():
    state_dropdown.set("")
    crop_dropdown.set("")
    entry_area.delete(0, tk.END)
    entry_rainfall.delete(0, tk.END)
    output_label.configure(text="")


# Function to quit the application
def quit_app():
    window.destroy()


# Define the dropdown list options
state_options = dataset['State_Name'].unique().tolist()

# Create the state dropdown widget
state_label = tk.Label(window, text="State:")
state_label.pack()
state_dropdown = ttk.Combobox(window, values=state_options, width=25)
state_dropdown.pack(pady=5)

# Create the crop dropdown widget
crop_label = tk.Label(window, text="Crop:")
crop_label.pack()
crop_dropdown = ttk.Combobox(window, width=25)
crop_dropdown.pack(pady=5)

# Link the crop dropdown to the state dropdown selection
state_dropdown.bind("<<ComboboxSelected>>", update_crop_dropdown)

# Create input fields in the GUI
area_label = tk.Label(window, text="Area (in hectares):")
area_label.pack(pady = 5)

entry_area = tk.Entry(window, width=30)
entry_area.pack(pady=5)

rainfall_label = tk.Label(window, text="Rainfall (in mm):")
rainfall_label.pack()
entry_rainfall = tk.Entry(window, width=30)
entry_rainfall.pack(pady=5)

# Create output label in the GUI
output_label = tk.Label(window, text="")
output_label.pack(pady=5)

# Create submit button in the GUI
submit_button = tk.Button(window, text="Submit", command=submit_prediction, width=30, bg="#4CAF50", fg="white")
submit_button.pack(pady=10)

# Create clear/reset button in the GUI
clear_button = tk.Button(window, text="Clear", command=clear_fields, width=30)
clear_button.pack(pady=5)

# Create quit button in the GUI
quit_button = tk.Button(window, text="Quit", command=quit_app, width=30)
quit_button.pack(pady=5)

# Run the GUI
window.mainloop()

