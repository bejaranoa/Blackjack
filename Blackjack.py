import customtkinter as ctk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.geometry('400x240')

def button_function():
    frame = ctk.CTkFrame(root)
    frame.pack(fill="both", expand=1)

button = ctk.CTkButton(master=root, text="Play", command=button_function)
button.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

root.mainloop()