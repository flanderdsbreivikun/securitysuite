import tkinter as tk
import customtkinter as ctk
from tkinter import scrolledtext, messagebox
import socket
from threading import Thread

def launch_port_scanner_tool(root, return_to_home):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    port_frame = ctk.CTkFrame(root)
    port_frame.pack(fill="both", expand=True, padx=20, pady=20)

    header = ctk.CTkFrame(port_frame)
    header.pack(fill="x", padx=20, pady=(20, 40))
    
    title_label = ctk.CTkLabel(
        header,
        text="Scanner de Ports",
        font=("Roboto", 24, "bold")
    )
    title_label.pack(pady=10)

    input_frame = ctk.CTkFrame(port_frame)
    input_frame.pack(fill="x", padx=40, pady=20)

    ctk.CTkLabel(
        input_frame,
        text="Adresse IP cible:",
        font=("Roboto", 14)
    ).pack(pady=(10, 0))
    
    entry_target = ctk.CTkEntry(
        input_frame,
        width=300,
        height=35,
        font=("Roboto", 12)
    )
    entry_target.pack(pady=(5, 15))

    ctk.CTkLabel(
        input_frame,
        text="Plage de ports (ex: 1-1024):",
        font=("Roboto", 14)
    ).pack(pady=(10, 0))
    
    entry_ports = ctk.CTkEntry(
        input_frame,
        width=300,
        height=35,
        font=("Roboto", 12)
    )
    entry_ports.pack(pady=(5, 15))

    button_frame = ctk.CTkFrame(port_frame)
    button_frame.pack(pady=20)

    ctk.CTkButton(
        button_frame,
        text="Démarrer le scan",
        command=lambda: start_scan(entry_target.get(), entry_ports.get(), log_text),
        font=("Roboto", 14),
        width=200,
        height=40
    ).pack(side="left", padx=10)

    ctk.CTkButton(
        button_frame,
        text="Retour à l'accueil",
        command=lambda: navigate_home(port_frame, root, return_to_home),
        font=("Roboto", 14),
        width=200,
        height=40
    ).pack(side="left", padx=10)

    log_frame = ctk.CTkFrame(port_frame)
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
    
    log_text.tag_configure("success", foreground="#00ff00")
    log_text.tag_configure("error", foreground="#ff6b6b")
    log_text.tag_configure("info", foreground="#63c5ea")

def start_scan(target, port_range, log_text):
    if not target or not port_range:
        messagebox.showerror("Erreur", "Veuillez entrer une adresse IP et une plage de ports.")
        return

    log_text.insert(tk.END, "=== Démarrage du scan ===\n", "info")
    log_text.insert(tk.END, f"Cible : {target}\n", "info")
    log_text.insert(tk.END, f"Ports : {port_range}\n\n", "info")
    log_text.update()

    try:
        start_port, end_port = map(int, port_range.split('-'))
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer une plage de ports valide (ex: 1-1024).")
        return

    for port in range(start_port, end_port + 1):
        Thread(target=scan_port, args=(target, port, log_text)).start()

def scan_port(target, port, log_text):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)

    result = sock.connect_ex((target, port))
    if result == 0:
        log_text.insert(tk.END, f"[+] Port {port} : OUVERT\n", "success")
    else:
        log_text.insert(tk.END, f"[-] Port {port} : FERMÉ\n", "error")
    log_text.see(tk.END)
    sock.close()

def navigate_home(current_frame, root, return_to_home):
    current_frame.pack_forget()
    return_to_home()

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Scanner de Ports")
    root.geometry("800x600")
    launch_port_scanner_tool(root, lambda: None)
    root.mainloop()