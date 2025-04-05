import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess
import json
import shutil
import threading
import sys
from PIL import Image
import requests
import webbrowser
from packaging import version

class UpdateDialog(ctk.CTkToplevel):
    def __init__(self, parent, current_version, latest_version, release_url):
        super().__init__(parent)
        
        # Configure window
        self.title("Update Available")
        self.geometry("400x250")
        self.resizable(False, False)
        
        # Make it modal
        self.transient(parent)
        self.grab_set()
        
        # Center the dialog
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')
        
        # Content
        header = ctk.CTkLabel(
            self,
            text="🚀 New Version Available!",
            font=ctk.CTkFont(size=20, weight="bold", family="Segoe UI")
        )
        header.pack(pady=(20, 10))
        
        version_info = ctk.CTkLabel(
            self,
            text=f"Current version: {current_version}\nLatest version: {latest_version}",
            font=ctk.CTkFont(size=14, family="Consolas")
        )
        version_info.pack(pady=10)
        
        message = ctk.CTkLabel(
            self,
            text="A new version of Web2Exe is available.\nWould you like to download it?",
            font=ctk.CTkFont(size=14, family="Consolas")
        )
        message.pack(pady=10)
        
        # Buttons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=20)
        
        download_btn = ctk.CTkButton(
            button_frame,
            text="Download Update",
            command=lambda: self.open_release(release_url),
            font=ctk.CTkFont(size=14, family="Consolas"),
            fg_color="#2ECC71",
            hover_color="#27AE60"
        )
        download_btn.pack(side="left", padx=10)
        
        remind_btn = ctk.CTkButton(
            button_frame,
            text="Remind Me Later",
            command=self.destroy,
            font=ctk.CTkFont(size=14, family="Consolas"),
            fg_color="#95A5A6",
            hover_color="#7F8C8D"
        )
        remind_btn.pack(side="left", padx=10)
    
    def open_release(self, url):
        webbrowser.open(url)
        self.destroy()

class Web2ExeApp(ctk.CTk):
    VERSION = "1.0.0"
    GITHUB_REPO = "MurShidM01/Web2Exe-Python-Tool"

    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Web2Exe Tool")
        self.geometry("960x640")
        self.resizable(False, False)
        # self.minsize(960, 640)
        # self.maxsize(960, 640)
        
        # Set application icon
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_icon.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

        # Set custom colors for professional theme
        self.primary_color = "#0066CC"      # Professional blue
        self.secondary_color = "#3498DB"    # Lighter blue
        self.accent_color = "#2ECC71"       # Success green
        self.warning_color = "#F1C40F"      # Warning yellow
        self.error_color = "#E74C3C"        # Error red
        self.bg_color = "#F5F7FA"           # Light gray background
        self.card_color = "#FFFFFF"         # White for cards
        self.text_color = "#2C3E50"         # Dark blue-gray for text
        self.border_color = "#f00759"       # Border color
        self.hover_color = "#13f007"        # Hover blue

        # Set default appearance mode to light
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create main scrollable frame
        self.main_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=self.bg_color,
            corner_radius=0,
            scrollbar_button_hover_color=self.hover_color
        )
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Create gradient header
        self.header_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.primary_color,
            height=120,
            corner_radius=0,
            border_width=3,
            border_color=self.border_color
        )
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 25))
        self.header_frame.grid_columnconfigure(0, weight=1)

        # App logo/title with enhanced styling
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Web2Exe",
            font=ctk.CTkFont(size=36, weight="bold", family="Cooper Black"),
            text_color="white"
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(30, 5))

        self.subtitle_label = ctk.CTkLabel(
            self.header_frame,
            text="Professional Web Application Converter",
            font=ctk.CTkFont(size=14, family="Consolas"),
            text_color="#E8F0FE"
        )
        self.subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 30))

        self.version_label = ctk.CTkLabel(
            self.header_frame,
            text="Version 1.0.0",
            font=ctk.CTkFont(size=12, family="Consolas"),
            text_color="#E8F0FE"
        )
        self.version_label.grid(row=2, column=0, padx=20, pady=(0, 40))

        # Main content container with shadow effect
        self.content_container = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        self.content_container.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.content_container.grid_columnconfigure(0, weight=1)

        # Check for updates
        self.after(1000, self.check_for_updates)  # Check after 1 second

        # Project section
        self.create_project_section()
        
        # Settings section
        self.create_settings_section()
        
        # Build section
        self.create_build_section()

    def create_project_section(self):
        # Project Section
        project_frame = ctk.CTkFrame(
            self.content_container,
            fg_color=self.card_color,
            corner_radius=10,
            border_width=3,
            border_color=self.border_color
        )
        project_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        project_frame.grid_columnconfigure(1, weight=1)

        # Section Title
        section_label = ctk.CTkLabel(
            project_frame,
            text="📂 Project Configuration",
            font=ctk.CTkFont(size=16, weight="bold", family="Segoe UI"),
            text_color=self.text_color
        )
        section_label.grid(row=0, column=0, columnspan=2, padx=15, pady=(15, 5), sticky="w")

        # Project folder
        folder_frame = self.create_input_group(project_frame, "Project Folder:", 1)
        self.folder_entry = ctk.CTkEntry(
            folder_frame,
            height=36,
            placeholder_text="Select your web project folder",
            font=ctk.CTkFont(size=13, family="Consolas"),
            corner_radius=5,
            border_width=3,
            border_color=self.border_color
        )
        self.folder_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.folder_button = ctk.CTkButton(
            folder_frame,
            text="Browse",
            width=90,
            height=36,
            command=self.select_folder,
            fg_color=self.secondary_color,
            hover_color=self.hover_color,
            corner_radius=5,
            font=ctk.CTkFont(size=13),
            border_width=2,
            border_color=self.border_color
        )
        self.folder_button.grid(row=0, column=2, padx=(5, 10), pady=5)

        # App name
        name_frame = self.create_input_group(project_frame, "App Name:", 2)
        self.name_entry = ctk.CTkEntry(
            name_frame,
            height=36,
            placeholder_text="Enter your application name",
            font=ctk.CTkFont(size=13, family="Consolas"),
            corner_radius=5,
            border_width=3,
            border_color=self.border_color
        )
        self.name_entry.grid(row=0, column=1, columnspan=2, padx=(5, 10), pady=5, sticky="ew")

        # Icon file
        icon_frame = self.create_input_group(project_frame, "Icon File:", 3)
        self.icon_entry = ctk.CTkEntry(
            icon_frame,
            height=36,
            placeholder_text="Optional: Select an .ico file",
            font=ctk.CTkFont(size=13, family="Consolas"),
            corner_radius=5,
            border_width=3,
            border_color=self.border_color
        )
        self.icon_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.icon_button = ctk.CTkButton(
            icon_frame,
            text="Browse",
            width=90,
            height=36,
            command=self.select_icon,
            fg_color=self.secondary_color,
            hover_color=self.hover_color,
            corner_radius=5,
            font=ctk.CTkFont(size=13, family="Consolas"),
            border_width=2,
            border_color=self.border_color
        )
        self.icon_button.grid(row=0, column=2, padx=(5, 10), pady=5)

    def create_settings_section(self):
        # Settings Section
        settings_frame = ctk.CTkFrame(
            self.content_container,
            fg_color=self.card_color,
            corner_radius=10,
            border_width=3,
            border_color=self.border_color
        )
        settings_frame.grid(row=1, column=0, padx=5, pady=10, sticky="ew")
        settings_frame.grid_columnconfigure(0, weight=1)

        # Section Title
        section_label = ctk.CTkLabel(
            settings_frame,
            text="⚙️ Application Settings",
            font=ctk.CTkFont(size=16, weight="bold", family="Segoe UI"),
            text_color=self.text_color
        )
        section_label.grid(row=0, column=0, padx=15, pady=(15, 10), sticky="w")

        # Settings Grid
        settings_grid = ctk.CTkFrame(settings_frame, fg_color="transparent")
        settings_grid.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        settings_grid.grid_columnconfigure((0, 1), weight=1)

        # Window Size
        size_frame = ctk.CTkFrame(settings_grid, fg_color=self.bg_color, corner_radius=5)
        size_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(
            size_frame,
            text="Window Size",
            font=ctk.CTkFont(size=13, weight="bold", family="Consolas"),
            text_color=self.text_color
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=(5, 0), sticky="w")

        # Width input
        ctk.CTkLabel(
            size_frame,
            text="Width:",
            font=ctk.CTkFont(size=12, family="Consolas")
        ).grid(row=1, column=0, padx=(10, 5), pady=5)

        self.width_entry = ctk.CTkEntry(
            size_frame,
            width=70,
            height=32,
            placeholder_text="1200"
        )
        self.width_entry.grid(row=1, column=1, padx=5, pady=5)
        self.width_entry.insert(0, "1200")

        # Height input
        ctk.CTkLabel(
            size_frame,
            text="Height:",
            font=ctk.CTkFont(size=12, family="Consolas")
        ).grid(row=1, column=2, padx=(10, 5), pady=5)

        self.height_entry = ctk.CTkEntry(
            size_frame,
            width=70,
            height=32,
            placeholder_text="800"
        )
        self.height_entry.grid(row=1, column=3, padx=(5, 10), pady=5)
        self.height_entry.insert(0, "800")

        # Window Options
        options_frame = ctk.CTkFrame(settings_grid, fg_color=self.bg_color, corner_radius=5)
        options_frame.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(
            options_frame,
            text="Window Options",
            font=ctk.CTkFont(size=13, weight="bold", family="Consolas"),
            text_color=self.text_color
        ).grid(row=0, column=0, columnspan=3, padx=10, pady=(5, 0), sticky="w")

        # Checkboxes with icons
        self.resizable_var = tk.BooleanVar(value=True)
        self.resizable_check = self.create_checkbox(
            options_frame, "↔️ Resizable", self.resizable_var, 1, 0
        )

        self.frame_var = tk.BooleanVar(value=True)
        self.frame_check = self.create_checkbox(
            options_frame, "🔲 Window Frame", self.frame_var, 1, 1
        )

        self.kiosk_var = tk.BooleanVar(value=False)
        self.kiosk_check = self.create_checkbox(
            options_frame, "🖥️ Kiosk Mode", self.kiosk_var, 1, 2
        )

        # Advanced Options
        advanced_frame = ctk.CTkFrame(settings_grid, fg_color=self.bg_color, corner_radius=5)
        advanced_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(
            advanced_frame,
            text="Advanced Options",
            font=ctk.CTkFont(size=13, weight="bold", family="Consolas"),
            text_color=self.text_color
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=(5, 0), sticky="w")

        # Advanced checkboxes
        self.dev_tools_var = tk.BooleanVar(value=False)
        self.dev_tools_check = self.create_checkbox(
            advanced_frame, "🛠️ DevTools", self.dev_tools_var, 1, 0
        )

        self.single_instance_var = tk.BooleanVar(value=True)
        self.single_instance_check = self.create_checkbox(
            advanced_frame, "📌 Single Instance", self.single_instance_var, 1, 1
        )

        # Build options
        build_frame = ctk.CTkFrame(advanced_frame, fg_color="transparent")
        build_frame.grid(row=1, column=2, columnspan=2, padx=10, pady=5, sticky="e")

        # Compression dropdown
        ctk.CTkLabel(
            build_frame,
            text="Compression:",
            font=ctk.CTkFont(size=12, family="Consolas")
        ).grid(row=0, column=0, padx=(0, 5))

        self.compression_var = tk.StringVar(value="maximum")
        self.compression_menu = ctk.CTkOptionMenu(
            build_frame,
            values=["maximum", "normal"],
            variable=self.compression_var,
            width=100,
            height=32,
            font=ctk.CTkFont(size=12, family="Consolas"),
            fg_color=self.secondary_color,
            button_color=self.hover_color,
            button_hover_color=self.primary_color
        )
        self.compression_menu.grid(row=0, column=1, padx=5)

        # Build type dropdown
        ctk.CTkLabel(
            build_frame,
            text="Build Type:",
            font=ctk.CTkFont(size=12, family="Consolas")
        ).grid(row=0, column=2, padx=(10, 5))

        self.build_type_var = tk.StringVar(value="nsis")
        self.build_type_menu = ctk.CTkOptionMenu(
            build_frame,
            values=["nsis", "portable"],
            variable=self.build_type_var,
            width=100,
            height=32,
            font=ctk.CTkFont(size=12, family="Consolas"),
            fg_color=self.secondary_color,
            button_color=self.hover_color,
            button_hover_color=self.primary_color
        )
        self.build_type_menu.grid(row=0, column=3, padx=5)

    def create_build_section(self):
        # Build Section
        build_frame = ctk.CTkFrame(
            self.content_container,
            fg_color=self.card_color,
            corner_radius=10,
            border_width=3,
            border_color=self.border_color
        )
        build_frame.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        build_frame.grid_columnconfigure(0, weight=1)

        # Build button
        self.build_button = ctk.CTkButton(
            build_frame,
            text="🚀 Build Application",
            command=self.start_build,
            height=44,
            font=ctk.CTkFont(size=15, weight="bold", family="Segoe UI"),
            fg_color=self.accent_color,
            hover_color="#27AE60",
            corner_radius=5,
            border_width=2,
            border_color=self.border_color
        )
        self.build_button.grid(row=0, column=0, padx=15, pady=15)

        # Progress log
        log_label = ctk.CTkLabel(
            build_frame,
            text="📋 Build Progress",
            font=ctk.CTkFont(size=14, weight="bold", family="Segoe UI"),
            text_color=self.text_color
        )
        log_label.grid(row=1, column=0, padx=15, pady=(5, 0), sticky="w")

        # Log frame with custom styling
        self.log_frame = ctk.CTkFrame(
            build_frame,
            fg_color=self.bg_color,
            corner_radius=5
        )
        self.log_frame.grid(row=2, column=0, padx=15, pady=10, sticky="nsew")
        self.log_frame.grid_columnconfigure(0, weight=1)
        self.log_frame.grid_rowconfigure(0, weight=1)

        self.log_text = ctk.CTkTextbox(
            self.log_frame,
            height=150,
            wrap="word",
            font=ctk.CTkFont(family="Consolas", size=12),
            corner_radius=5,
            border_spacing=10,
            fg_color=self.bg_color,
            border_color=self.border_color,
            border_width=3
        )
        self.log_text.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Show in folder button
        self.show_folder_button = ctk.CTkButton(
            build_frame,
            text="📂 Show in Folder",
            command=self.show_in_folder,
            state="disabled",
            height=36,
            font=ctk.CTkFont(size=13, family="Consolas"),
            fg_color=self.secondary_color,
            hover_color=self.hover_color,
            corner_radius=5,
            border_width=2,
            border_color=self.border_color
        )
        self.show_folder_button.grid(row=3, column=0, padx=15, pady=(0, 15))

        # Add copyright footer
        footer_frame = ctk.CTkFrame(
            build_frame,
            fg_color="transparent"
        )
        footer_frame.grid(row=4, column=0, padx=15, pady=(0, 10), sticky="ew")
        footer_frame.grid_columnconfigure(0, weight=1)

        copyright_label = ctk.CTkLabel(
            footer_frame,
            text="@Copyright 2025 Developed By Ali Khan Jalbani",
            font=ctk.CTkFont(size=12, family="Consolas", slant="italic"),
            text_color=self.text_color
        )
        copyright_label.grid(row=0, column=0, sticky="s")

    def create_input_group(self, parent, label_text, row):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=row, column=0, columnspan=2, padx=10, pady=2, sticky="ew")
        frame.grid_columnconfigure(1, weight=1)

        label = ctk.CTkLabel(
            frame,
            text=label_text,
            font=ctk.CTkFont(size=13, family="Consolas"),
            width=100,
            anchor="e"
        )
        label.grid(row=0, column=0, padx=(5, 10), pady=5)

        return frame

    def create_checkbox(self, parent, text, variable, row, column):
        return ctk.CTkCheckBox(
            parent,
            text=text,
            variable=variable,
            font=ctk.CTkFont(size=12, family="Consolas"),
            checkbox_height=20,
            checkbox_width=20,
            corner_radius=3,
            border_width=3,
            fg_color=self.secondary_color,
            hover_color=self.hover_color
        ).grid(row=row, column=column, padx=10, pady=5, sticky="w")

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder)

    def select_icon(self):
        icon = filedialog.askopenfilename(
            filetypes=[("Icon files", "*.ico"), ("All files", "*.*")]
        )
        if icon:
            self.icon_entry.delete(0, tk.END)
            self.icon_entry.insert(0, icon)

    def log(self, message):
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")
        self.update_idletasks()

    def check_requirements(self):
        try:
            # List of common Node.js installation paths on Windows
            possible_node_paths = [
                r"C:\Program Files\nodejs\node.exe",
                r"C:\Program Files (x86)\nodejs\node.exe",
                os.path.expandvars(r"%APPDATA%\Local\Programs\node\node.exe"),
                os.path.expandvars(r"%ProgramFiles%\nodejs\node.exe"),
                os.path.expandvars(r"%ProgramFiles(x86)%\nodejs\node.exe"),
                "node"  # Try the PATH version as last resort
            ]

            node_found = False
            node_path = None
            node_version = ""
            npm_version = ""

            # Try to find Node.js
            for path in possible_node_paths:
                try:
                    if path == "node":
                        # Try using PATH
                        result = subprocess.run(["node", "--version"], 
                                             capture_output=True, 
                                             text=True, 
                                             shell=True)
                    else:
                        # Try specific path
                        if os.path.exists(path):
                            result = subprocess.run([path, "--version"], 
                                                 capture_output=True, 
                                                 text=True)
                    
                    if result.returncode == 0:
                        node_found = True
                        node_path = path
                        node_version = result.stdout.strip()
                        self.log(f"Found Node.js: {node_version}")
                        break
                except Exception:
                    continue

            if not node_found:
                self.log("Error: Node.js not found in common installation paths")
                raise FileNotFoundError("Node.js not found")

            # Once we have Node.js, try to find npm in the same directory
            npm_path = "npm"  # Default to PATH version
            if node_path and node_path != "node":
                node_dir = os.path.dirname(node_path)
                possible_npm = os.path.join(node_dir, "npm.cmd")
                if os.path.exists(possible_npm):
                    npm_path = possible_npm

            # Check npm
            try:
                result = subprocess.run([npm_path, "--version"], 
                                     capture_output=True, 
                                     text=True,
                                     shell=True)
                if result.returncode == 0:
                    npm_version = result.stdout.strip()
                    self.log(f"Found npm: {npm_version}")
                    return True
                else:
                    raise FileNotFoundError("npm check failed")
            except Exception as e:
                self.log(f"Error checking npm: {str(e)}")
                raise FileNotFoundError("npm not found")

        except Exception as e:
            self.log(f"Error during requirements check: {str(e)}")
            messagebox.showerror(
                "Requirements Error",
                "Node.js and npm are required but not found. Please ensure they are properly installed and available in your system PATH.\n\n"
                f"Your current Node.js and npm versions from terminal:\n"
                f"node -v: {node_version if node_version else 'Not found'}\n"
                f"npm -v: {npm_version if npm_version else 'Not found'}\n\n"
                "Please try the following:\n"
                "1. Close and reopen the application\n"
                "2. If that doesn't work, restart your computer\n"
                "3. If still not working, try repairing your Node.js installation"
            )
            return False

    def create_electron_files(self, project_path, app_name):
        # Create package.json with optimized settings
        package_json = {
            "name": app_name.lower().replace(" ", "-"),
            "version": "1.0.0",
            "description": f"{app_name} - Created with Web2Exe",
            "main": "main.js",
            "scripts": {
                "start": "electron .",
                "build": "electron-builder"
            },
            "build": {
                "appId": f"com.web2exe.{app_name.lower().replace(' ', '')}",
                "win": {
                    "target": self.build_type_var.get(),
                    "icon": self.icon_entry.get() if self.icon_entry.get() else os.path.join("build", "icon.ico"),
                    "compression": self.compression_var.get()
                },
                "files": [
                    "**/*",
                    "!**/node_modules/*/{CHANGELOG.md,README.md,README,readme.md,readme}",
                    "!**/node_modules/*/{test,__tests__,tests,powered-test,example,examples}",
                    "!**/node_modules/*.d.ts",
                    "!**/node_modules/.bin",
                    "!**/*.{iml,o,hprof,orig,pyc,pyo,rbc,swp,csproj,sln,xproj}",
                    "!.editorconfig",
                    "!**/._*",
                    "!**/{.DS_Store,.git,.hg,.svn,CVS,RCS,SCCS,.gitignore,.gitattributes}",
                    "!**/{__pycache__,thumbs.db,.flowconfig,.idea,.vs,.nyc_output}",
                    "!**/{appveyor.yml,.travis.yml,circle.yml}",
                    "!**/{npm-debug.log,yarn.lock,.yarn-integrity,.yarn-metadata.json}"
                ],
                "asar": True,
                "removePackageScripts": True,
                "removePackageKeywords": True
            },
            "devDependencies": {
                "electron": "^28.1.0",
                "electron-builder": "^24.9.1"
            }
        }

        # Get window settings
        try:
            width = int(self.width_entry.get() or 1200)
            height = int(self.height_entry.get() or 800)
        except ValueError:
            width, height = 1200, 800

        # Handle icon path
        icon_path = self.icon_entry.get()
        if icon_path:
            # Create build directory if it doesn't exist
            build_dir = os.path.join(project_path, "build")
            if not os.path.exists(build_dir):
                os.makedirs(build_dir)
            
            # Copy icon to build directory
            icon_dest = os.path.join("build", "icon.ico")
            try:
                shutil.copy2(icon_path, os.path.join(project_path, icon_dest))
            except Exception as e:
                self.log(f"Warning: Could not copy icon file: {str(e)}")
                icon_dest = "build/icon.ico"
        else:
            icon_dest = "build/icon.ico"

        # Create main.js with custom settings
        main_js = f'''const {{ app, BrowserWindow }} = require('electron')
const path = require('path')

{"""const gotTheLock = app.requestSingleInstanceLock()
if (!gotTheLock) {
    app.quit()
    return
}""" if self.single_instance_var.get() else ""}

function createWindow() {{
    const win = new BrowserWindow({{
        width: {width},
        height: {height},
        webPreferences: {{
            nodeIntegration: true,
            contextIsolation: false,
            devTools: {str(self.dev_tools_var.get()).lower()}
        }},
        resizable: {str(self.resizable_var.get()).lower()},
        kiosk: {str(self.kiosk_var.get()).lower()},
        frame: {str(self.frame_var.get()).lower()},
        icon: path.join(__dirname, '{icon_dest.replace(os.sep, "/")}')
    }})
    win.loadFile('index.html')
    
    {f"win.maximize()" if self.kiosk_var.get() else ""}
    {f"win.webContents.openDevTools()" if self.dev_tools_var.get() else ""}
}}

app.whenReady().then(() => {{
    createWindow()
    
    app.on('activate', () => {{
        if (BrowserWindow.getAllWindows().length === 0) {{
            createWindow()
        }}
    }})
}})

app.on('window-all-closed', () => {{
    if (process.platform !== 'darwin') {{
        app.quit()
    }}
}})'''

        # Create temporary directory using a more robust path
        temp_dir = os.path.abspath(os.path.join(os.path.dirname(project_path), f"{app_name}_electron_build"))
        if os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except Exception as e:
                self.log(f"Warning: Could not remove existing build directory: {str(e)}")
                # Try to use a unique name
                temp_dir = os.path.abspath(os.path.join(os.path.dirname(project_path), f"{app_name}_electron_build_{os.urandom(4).hex()}"))
        
        os.makedirs(temp_dir, exist_ok=True)

        # Copy web project files
        try:
            for item in os.listdir(project_path):
                source = os.path.join(project_path, item)
                dest = os.path.join(temp_dir, item)
                try:
                    if os.path.isdir(source):
                        shutil.copytree(source, dest)
                    else:
                        shutil.copy2(source, dest)
                except Exception as e:
                    self.log(f"Warning: Could not copy {item}: {str(e)}")
        except Exception as e:
            self.log(f"Error copying project files: {str(e)}")
            raise

        # Write Electron files
        try:
            with open(os.path.join(temp_dir, "package.json"), "w", encoding='utf-8') as f:
                json.dump(package_json, f, indent=2)

            with open(os.path.join(temp_dir, "main.js"), "w", encoding='utf-8') as f:
                f.write(main_js)
        except Exception as e:
            self.log(f"Error writing electron files: {str(e)}")
            raise

        return temp_dir

    def build_exe(self):
        electron_dir = None
        try:
            # Validate inputs
            project_path = self.folder_entry.get().strip()
            app_name = self.name_entry.get().strip()

            if not project_path or not app_name:
                raise ValueError("Project folder and app name are required.")

            if not os.path.exists(project_path):
                raise ValueError("Selected project folder does not exist.")

            index_html = os.path.join(project_path, "index.html")
            if not os.path.exists(index_html):
                raise ValueError("Project folder must contain an index.html file.")

            # Validate icon if provided
            icon_path = self.icon_entry.get().strip()
            if icon_path:
                if not os.path.exists(icon_path):
                    raise ValueError("Specified icon file does not exist.")
                if not icon_path.lower().endswith('.ico'):
                    raise ValueError("Icon file must be in .ico format.")

            # Create Electron project
            self.log("Creating Electron project structure...")
            electron_dir = self.create_electron_files(project_path, app_name)

            # Install dependencies
            self.log("Installing dependencies (this may take a few minutes)...")
            npm_install = subprocess.run(
                "npm install",
                cwd=electron_dir,
                shell=True,
                capture_output=True,
                text=True
            )
            
            if npm_install.returncode != 0:
                self.log("Error during npm install:")
                self.log(npm_install.stdout)
                self.log(npm_install.stderr)
                raise subprocess.CalledProcessError(
                    npm_install.returncode,
                    "npm install",
                    npm_install.stdout,
                    npm_install.stderr
                )

            # Build executable
            self.log("Building executable...")
            npm_build = subprocess.run(
                "npm run build",
                cwd=electron_dir,
                shell=True,
                capture_output=True,
                text=True
            )
            
            if npm_build.returncode != 0:
                self.log("Error during npm run build:")
                self.log(npm_build.stdout)
                self.log(npm_build.stderr)
                raise subprocess.CalledProcessError(
                    npm_build.returncode,
                    "npm run build",
                    npm_build.stdout,
                    npm_build.stderr
                )

            # Get output path
            dist_dir = os.path.join(electron_dir, "dist")
            if not os.path.exists(dist_dir):
                raise ValueError("Build completed but dist directory was not created.")

            exe_files = [f for f in os.listdir(dist_dir) if f.endswith(".exe")]
            if not exe_files:
                raise ValueError("Build completed but no .exe file was found in the dist directory.")

            self.output_exe_path = os.path.join(dist_dir, exe_files[0])
            if not os.path.exists(self.output_exe_path):
                raise ValueError(f"Expected executable not found at: {self.output_exe_path}")

            self.log(f"\nBuild completed successfully!\nExecutable created at:\n{self.output_exe_path}")
            self.show_folder_button.configure(state="normal")

        except subprocess.CalledProcessError as e:
            error_msg = f"Command '{e.cmd}' failed with return code {e.returncode}.\n"
            if e.stdout:
                error_msg += f"\nOutput:\n{e.stdout}"
            if e.stderr:
                error_msg += f"\nError:\n{e.stderr}"
            self.log(f"Error during build process:\n{error_msg}")
            messagebox.showerror("Build Error", "An error occurred during the build process. Check the log for details.")
        
        except Exception as e:
            self.log(f"Error: {str(e)}")
            messagebox.showerror("Error", str(e))
        
        finally:
            self.build_button.configure(state="normal")
            
            # Clean up temporary directory if it exists and build was successful
            if electron_dir and os.path.exists(electron_dir) and hasattr(self, 'output_exe_path'):
                try:
                    shutil.rmtree(electron_dir)
                except Exception as e:
                    self.log(f"Warning: Could not clean up temporary directory: {str(e)}")

    def start_build(self):
        if not self.check_requirements():
            return

        self.build_button.configure(state="disabled")
        self.log_text.delete("1.0", tk.END)
        self.show_folder_button.configure(state="disabled")
        
        self.build_thread = threading.Thread(target=self.build_exe)
        self.build_thread.start()

    def show_in_folder(self):
        if self.output_exe_path and os.path.exists(self.output_exe_path):
            # Fix for Windows explorer select
            path = os.path.normpath(self.output_exe_path)
            subprocess.run(['explorer', '/select,', path], shell=True)

    def check_for_updates(self):
        try:
            # Get latest release info from GitHub
            response = requests.get(f"https://api.github.com/repos/{self.GITHUB_REPO}/releases/latest")
            if response.status_code == 200:
                release_info = response.json()
                latest_version = release_info["tag_name"].lstrip('v')  # Remove 'v' prefix if present
                
                # Compare versions
                if version.parse(latest_version) > version.parse(self.VERSION):
                    # Show update dialog
                    UpdateDialog(
                        self,
                        self.VERSION,
                        latest_version,
                        release_info["html_url"]
                    )
        except Exception as e:
            print(f"Failed to check for updates: {str(e)}")

if __name__ == "__main__":
    app = Web2ExeApp()
    app.mainloop() 