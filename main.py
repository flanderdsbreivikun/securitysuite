import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import ddos_tool
import scan_vul
import sql_injection
import scan_ports
from shoutbox import ShoutboxClient

class ModernSecurityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Security Testing Suite")
        self.root.geometry("800x600")
        self.setup_home()

    def setup_home(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.header = ctk.CTkFrame(self.main_frame)
        self.header.pack(fill="x", padx=20, pady=(20, 40))
        
        self.title_label = ctk.CTkLabel(
            self.header, 
            text="Security Testing Suite",
            font=("Roboto", 24, "bold")
        )
        self.title_label.pack(pady=10)

        self.nav_bar = ctk.CTkFrame(self.main_frame)
        self.nav_bar.pack(fill="x", padx=20, pady=(0, 20))

        self.create_tool_buttons()

    def create_tool_buttons(self):
        tools = [
            ("DDoS Tool", self.open_ddos_tool),
            ("Vulnerability Scanner", self.open_scan_vul_tool),
            ("SQL Injection", self.open_sql_injection_tool),
            ("Port Scanner", self.open_port_scanner_tool),
            ("Shoutbox", self.open_shoutbox),
            ("Forum", self.open_forum)
        ]

        for name, command in tools:
            ctk.CTkButton(
                self.nav_bar,
                text=name,
                command=command,
                font=("Roboto", 16),
                height=40,
                width=120
            ).pack(side="left", padx=10, pady=10)

    def open_ddos_tool(self):
        self.main_frame.pack_forget()
        ddos_tool.launch_ddos_tool(self.root, self.show_home)

    def open_scan_vul_tool(self):
        self.main_frame.pack_forget()
        scan_vul.launch_scan_vul_tool(self.root, self.show_home)

    def open_sql_injection_tool(self):
        self.main_frame.pack_forget()
        sql_injection.launch_sql_injection_tool(self.root, self.show_home)

    def open_port_scanner_tool(self):
        self.main_frame.pack_forget()
        scan_ports.launch_port_scanner_tool(self.root, self.show_home)

    def open_shoutbox(self):
        self.main_frame.pack_forget()
        ShoutboxClient(self.root, self.show_home)

    def open_forum(self):
        self.main_frame.pack_forget()
        from forum import ForumClient
        ForumClient(self.root, self.show_home)

    def show_home(self):
        self.setup_home()

if __name__ == "__main__":
    root = ctk.CTk()
    app = ModernSecurityApp(root)
    root.mainloop()