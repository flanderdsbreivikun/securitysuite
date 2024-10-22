import tkinter as tk
import requests
from tkinter import messagebox, scrolledtext
import customtkinter as ctk

class ForumClient:
    def __init__(self, root, go_home_callback):
        self.root = root
        self.go_home_callback = go_home_callback
        self.root.title("Forum")
        self.root.geometry("600x600")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.main_frame = ctk.CTkFrame(root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.title_label = ctk.CTkLabel(self.main_frame, text="Forum", font=("Roboto", 24, "bold"))
        self.title_label.pack(pady=10)

        self.thread_list = scrolledtext.ScrolledText(self.main_frame, state='disabled', width=70, height=15, bg="#222222", fg="#ffffff", font=("Consolas", 11))
        self.thread_list.pack(pady=10)

        self.load_threads()

        self.new_thread_label = ctk.CTkLabel(self.main_frame, text="Créer un nouveau thread:", font=("Roboto", 14))
        self.new_thread_label.pack(pady=(10, 0))

        self.title_entry = ctk.CTkEntry(self.main_frame, width=300, height=35, font=("Roboto", 12), placeholder_text="Titre du thread")
        self.title_entry.pack(pady=5)

        self.message_entry = ctk.CTkEntry(self.main_frame, width=300, height=35, font=("Roboto", 12), placeholder_text="Votre message")
        self.message_entry.pack(pady=5)

        self.username_entry = ctk.CTkEntry(self.main_frame, width=300, height=35, font=("Roboto", 12), placeholder_text="Pseudo")
        self.username_entry.pack(pady=5)

        self.create_thread_button = ctk.CTkButton(self.main_frame, text="Créer Thread", command=self.create_thread)
        self.create_thread_button.pack(pady=(5, 20))


        self.home_button = ctk.CTkButton(self.main_frame, text="Retour à l'accueil", command=lambda: self.navigate_home(self.main_frame, self.root, self.go_home_callback))
        self.home_button.pack(pady=(5, 10))

    def load_threads(self):
        self.thread_list.config(state='normal')
        self.thread_list.delete(1.0, tk.END) 

        response = requests.get("http://162.19.79.46:5000/forum") 
        if response.status_code == 200:
            threads = response.json()
            for thread in threads:
                self.thread_list.insert(tk.END, f"{thread['id']} - {thread['title']} - {thread['username']} (Cliquez pour voir)\n")
            self.thread_list.bind("<ButtonRelease-1>", self.on_thread_click)
        else:
            print(f"Failed to load threads: {response.status_code} {response.text}")
            messagebox.showerror("Error", "Erreur lors du chargement des threads.")

        self.thread_list.config(state='disabled')

    def on_thread_click(self, event):
        index = self.thread_list.index("@%s,%s" % (event.x, event.y))
        line = int(index.split('.')[0])
        thread_id = int(self.thread_list.get(f"{line}.0", f"{line}.end").split(" - ")[0])
        self.navigate_to_thread(thread_id)

    def create_thread(self):
        title = self.title_entry.get()
        message = self.message_entry.get()
        username = self.username_entry.get()

        if not title or not message or not username:
            messagebox.showwarning("Warning", "Veuillez remplir tous les champs.")
            return
        
        response = requests.post("http://162.19.79.46:5000/forum", json={'title': title, 'message': message, 'username': username})

        if response.status_code == 201:
            messagebox.showinfo("Success", "Thread créé avec succès!")
            self.load_threads()
        else:
            print(f"Failed to create thread: {response.status_code} {response.text}")
            messagebox.showerror("Error", "Erreur lors de la création du thread.")

    def navigate_home(self, current_frame, root, return_to_home):
        current_frame.pack_forget()
        return_to_home()

    def navigate_to_thread(self, thread_id):
        self.main_frame.pack_forget()
        ThreadDetail(self.root, thread_id, self.go_home_callback)

class ThreadDetail:
    def __init__(self, root, thread_id, go_home_callback):
        self.root = root
        self.thread_id = thread_id
        self.go_home_callback = go_home_callback
        self.root.title("Détails du Thread")
        self.root.geometry("600x600")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.detail_frame = ctk.CTkFrame(root)
        self.detail_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.title_label = ctk.CTkLabel(self.detail_frame, text="Détails du Thread", font=("Roboto", 24, "bold"))
        self.title_label.pack(pady=10)

        self.response_text = scrolledtext.ScrolledText(self.detail_frame, state='disabled', width=70, height=20, bg="#222222", fg="#ffffff", font=("Consolas", 11))
        self.response_text.pack(pady=10)

        self.load_thread_details()

        self.username_entry = ctk.CTkEntry(self.detail_frame, width=300, height=35, font=("Roboto", 12), placeholder_text="Pseudo")
        self.username_entry.pack(pady=5)

        self.response_entry = ctk.CTkEntry(self.detail_frame, width=300, height=35, font=("Roboto", 12), placeholder_text="Votre réponse")
        self.response_entry.pack(pady=5)

        self.reply_button = ctk.CTkButton(self.detail_frame, text="Répondre", command=self.submit_response)
        self.reply_button.pack(pady=(5, 20))


        self.home_button = ctk.CTkButton(self.detail_frame, text="Retour au Forum", command=self.return_to_forum)
        self.home_button.pack(pady=(5, 10))

    def load_thread_details(self):
        response = requests.get(f"http://162.19.79.46:5000/forum/{self.thread_id}")
        if response.status_code == 200:
            thread_data = response.json()
            self.response_text.config(state='normal')
            self.response_text.delete(1.0, tk.END) 
            self.response_text.insert(tk.END, f"{thread_data['title']} - {thread_data['username']}\n{thread_data['message']}\n\n")
            for resp in thread_data['responses']:
                self.response_text.insert(tk.END, f"{resp['username']}: {resp['message']}\n")
            self.response_text.config(state='disabled')
        else:
            messagebox.showerror("Error", "Erreur lors du chargement des détails du thread.")

    def submit_response(self):
        username = self.username_entry.get()
        message = self.response_entry.get()

        if not username or not message:
            messagebox.showwarning("Warning", "Veuillez remplir tous les champs.")
            return
        
        response = requests.post(f"http://162.19.79.46:5000/forum/{self.thread_id}/responses", json={'username': username, 'message': message})

        if response.status_code == 201:
            messagebox.showinfo("Success", "Réponse ajoutée avec succès!")
            self.load_thread_details()
        else:
            messagebox.showerror("Error", "Erreur lors de l'ajout de la réponse.")

    def return_to_forum(self):
        self.detail_frame.pack_forget()
        ForumClient(self.root, self.go_home_callback) 

if __name__ == "__main__":
    root = ctk.CTk()
    app = ForumClient(root, lambda: None)
    root.mainloop()
