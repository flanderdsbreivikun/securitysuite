import tkinter as tk
import requests
from tkinter import messagebox, scrolledtext
import customtkinter as ctk

class ShoutboxClient:
    def __init__(self, root, go_home_callback):
        self.root = root
        self.go_home_callback = go_home_callback
        self.auto_refresh = False
        self.root.title("Shoutbox")
        self.root.geometry("400x600")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.main_frame = ctk.CTkFrame(root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.header = ctk.CTkFrame(self.main_frame)
        self.header.pack(fill="x", padx=20, pady=(20, 40))

        title_label = ctk.CTkLabel(
            self.header,
            text="Shoutbox",
            font=("Roboto", 24, "bold")
        )
        title_label.pack(pady=10)

        self.frame_username = ctk.CTkFrame(self.main_frame)
        self.frame_username.pack(pady=(10, 0))

        self.username_label = ctk.CTkLabel(self.frame_username, text="Pseudo:", font=("Roboto", 14))
        self.username_label.pack(side=tk.LEFT)

        self.username_entry = ctk.CTkEntry(self.frame_username, width=200, height=35, font=("Roboto", 12))
        self.username_entry.pack(side=tk.LEFT, padx=5)

        self.frame_message = ctk.CTkFrame(self.main_frame)
        self.frame_message.pack(pady=(10, 0))

        self.message_label = ctk.CTkLabel(self.frame_message, text="Message:", font=("Roboto", 14))
        self.message_label.pack(side=tk.LEFT)

        self.message_entry = ctk.CTkEntry(self.frame_message, width=200, height=35, font=("Roboto", 12))
        self.message_entry.pack(side=tk.LEFT, padx=5)

        self.send_button = ctk.CTkButton(self.main_frame, text="Envoyer", command=self.send_message, height=35)
        self.send_button.pack(pady=(10, 0))

        self.messages_area = scrolledtext.ScrolledText(self.main_frame, state='disabled', width=100, height=15, bg="#222222", fg="#ffffff", font=("Consolas", 11))
        self.messages_area.pack(pady=10)

        self.home_button = ctk.CTkButton(self.main_frame, text="Retour à l'accueil", command=self.go_home, height=35)
        self.home_button.pack(pady=(5, 10))

        self.auto_refresh_var = tk.BooleanVar()
        self.auto_refresh_checkbox = ctk.CTkCheckBox(
            self.main_frame, 
            text="Recharger automatiquement les messages toutes les 5 secondes", 
            variable=self.auto_refresh_var,
            command=self.toggle_auto_refresh
        )
        self.auto_refresh_checkbox.pack()

        self.refresh_button = ctk.CTkButton(self.main_frame, text="Actualiser", command=self.load_messages, height=35)
        self.refresh_button.pack(pady=5)

        self.load_messages()

    def go_home(self):
        self.main_frame.pack_forget()
        self.go_home_callback()

    def toggle_auto_refresh(self):
        self.auto_refresh = self.auto_refresh_var.get()
        if self.auto_refresh:
            self.refresh_messages()
        else:
            self.root.after_cancel(self.refresh_task)

    def refresh_messages(self):
        self.load_messages()
        if self.auto_refresh:
            self.refresh_task = self.root.after(5001, self.refresh_messages)

    def send_message(self):
        username = self.username_entry.get()
        message = self.message_entry.get()
        
        if not username or not message:
            messagebox.showwarning("Warning", "Veuillez entrer un pseudo et un message.")
            return
        
        response = requests.post("http://162.19.79.46:5001/messages", json={'username': username, 'message': message})
        if response.status_code == 201:
            self.message_entry.delete(0, tk.END)
            self.load_messages()
        else:
            messagebox.showerror("Error", "Erreur lors de l'envoi du message.")

    def load_messages(self):
        self.messages_area.config(state='normal')
        self.messages_area.delete(1.0, tk.END)

        response = requests.get("http://162.19.79.46:5001/messages")
        if response.status_code == 200:
            messages = response.json()
            for msg in messages:
                self.messages_area.insert(tk.END, f"{msg['timestamp']}: ", 'red')
                self.messages_area.insert(tk.END, f"{msg['username']} - {msg['message']}\n")
        
        self.messages_area.config(state='disabled')

        self.messages_area.tag_config('red', foreground='red')

