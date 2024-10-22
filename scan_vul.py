import tkinter as tk
import customtkinter as ctk
from tkinter import scrolledtext, messagebox
import requests
from requests.exceptions import RequestException
import re
from threading import Thread

def launch_scan_vul_tool(root, return_to_home):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    scan_frame = ctk.CTkFrame(root)
    scan_frame.pack(fill="both", expand=True, padx=20, pady=20)

    header = ctk.CTkFrame(scan_frame)
    header.pack(fill="x", padx=20, pady=(20, 40))
    
    title_label = ctk.CTkLabel(
        header,
        text="Scanner de Vulnérabilités",
        font=("Roboto", 24, "bold")
    )
    title_label.pack(pady=10)

    input_frame = ctk.CTkFrame(scan_frame)
    input_frame.pack(fill="x", padx=40, pady=20)

    ctk.CTkLabel(
        input_frame,
        text="URL cible:",
        font=("Roboto", 14)
    ).pack(pady=(10, 0))
    
    entry_url = ctk.CTkEntry(
        input_frame,
        width=400,
        height=35,
        font=("Roboto", 12),
        placeholder_text="https://exemple.com"
    )
    entry_url.pack(pady=(5, 15))

    options_frame = ctk.CTkFrame(scan_frame)
    options_frame.pack(fill="x", padx=40, pady=(0, 20))

    xss_var = ctk.BooleanVar(value=True)
    sql_var = ctk.BooleanVar(value=True)
    
    ctk.CTkCheckBox(
        options_frame,
        text="XSS",
        variable=xss_var,
        font=("Roboto", 12)
    ).pack(side="left", padx=10)
    
    ctk.CTkCheckBox(
        options_frame,
        text="SQL Injection",
        variable=sql_var,
        font=("Roboto", 12)
    ).pack(side="left", padx=10)

    button_frame = ctk.CTkFrame(scan_frame)
    button_frame.pack(pady=20)

    ctk.CTkButton(
        button_frame,
        text="Démarrer le scan",
        command=lambda: Thread(target=start_scan, args=(entry_url.get(), log_text, xss_var.get(), sql_var.get())).start(),
        font=("Roboto", 14),
        width=200,
        height=40
    ).pack(side="left", padx=10)

    ctk.CTkButton(
        button_frame,
        text="Retour à l'accueil",
        command=lambda: navigate_home(scan_frame, root, return_to_home),
        font=("Roboto", 14),
        width=200,
        height=40
    ).pack(side="left", padx=10)

    log_frame = ctk.CTkFrame(scan_frame)
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

def start_scan(url, log_text, check_xss=True, check_sql=True):
    if not url:
        messagebox.showerror("Erreur", "Veuillez entrer une URL valide.")
        return

    log_text.delete(1.0, tk.END)
    
    log_text.insert(tk.END, "=== DÉMARRAGE DU SCAN DE VULNÉRABILITÉS ===\n\n", "title")
    log_text.insert(tk.END, f"Cible : {url}\n", "info")
    log_text.insert(tk.END, "Tests activés:\n", "info")
    if check_xss:
        log_text.insert(tk.END, "  • XSS (Cross-Site Scripting)\n", "info")
    if check_sql:
        log_text.insert(tk.END, "  • SQL Injection\n", "info")
    log_text.insert(tk.END, "\n", "info")
    log_text.update()

    vulnerabilities = []

    if check_xss:
        log_text.insert(tk.END, "[ Test des vulnérabilités XSS ]\n", "title")
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')"
        ]
        for payload in xss_payloads:
            try:
                response = requests.get(f"{url}?input={payload}")
                if response.status_code == 200 and payload in response.text:
                    vuln = f"Vulnérabilité XSS détectée avec : {payload}"
                    vulnerabilities.append(vuln)
                    log_text.insert(tk.END, f"[!] {vuln}\n", "warning")
                else:
                    log_text.insert(tk.END, f"[+] Test XSS négatif pour : {payload}\n", "success")
            except RequestException as e:
                log_text.insert(tk.END, f"[-] Erreur : {str(e)}\n", "error")
            log_text.update()

    if check_sql:
        log_text.insert(tk.END, "\n[ Test des vulnérabilités SQL Injection ]\n", "title")
        sql_payloads = [
            "' OR '1'='1",
            "' OR '1'='1' --",
            "1' ORDER BY 1--",
            "1' UNION SELECT NULL--"
        ]
        for payload in sql_payloads:
            try:
                response = requests.get(f"{url}?input={payload}")
                if "error" in response.text.lower() or "mysql" in response.text.lower():
                    vuln = f"Vulnérabilité SQL Injection détectée avec : {payload}"
                    vulnerabilities.append(vuln)
                    log_text.insert(tk.END, f"[!] {vuln}\n", "warning")
                else:
                    log_text.insert(tk.END, f"[+] Test SQL négatif pour : {payload}\n", "success")
            except RequestException as e:
                log_text.insert(tk.END, f"[-] Erreur : {str(e)}\n", "error")
            log_text.update()

    log_text.insert(tk.END, "\n=== RÉSUMÉ DU SCAN ===\n", "title")
    if vulnerabilities:
        log_text.insert(tk.END, f"\n{len(vulnerabilities)} vulnérabilité(s) détectée(s):\n", "warning")
        for v in vulnerabilities:
            log_text.insert(tk.END, f"• {v}\n", "warning")
    else:
        log_text.insert(tk.END, "\nAucune vulnérabilité détectée.\n", "success")
    
    log_text.insert(tk.END, "\n=== SCAN TERMINÉ ===\n", "title")
    log_text.see(tk.END)

def navigate_home(current_frame, root, return_to_home):
    current_frame.pack_forget()
    return_to_home()

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Scanner de Vulnérabilités")
    root.geometry("800x600")
    launch_scan_vul_tool(root, lambda: None)
    root.mainloop()