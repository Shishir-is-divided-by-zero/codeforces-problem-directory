import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import json
import os
from collections import defaultdict
import webbrowser
import threading
import time
import datetime
import shutil

class CodeforcesProblemDirectory:
    def __init__(self, root):
        self.root = root
        self.root.title("Codeforces Problem Directory Generator")
        self.root.geometry("850x650")
        
        # Set theme and colors
        self.primary_color = "#1a73e8"
        self.accent_color = "#ff8f00"
        self.bg_color = "#f5f5f7"
        self.card_bg = "white"
        
        # Configure root background
        self.root.configure(bg=self.bg_color)
        
        # Create custom styles
        self.setup_styles()
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, style="Main.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Create header
        self.create_header()
        
        # Create tab control
        self.tab_control = ttk.Notebook(self.main_frame)
        
        # Create tabs
        self.setup_tab = ttk.Frame(self.tab_control, style="Tab.TFrame")
        self.output_tab = ttk.Frame(self.tab_control, style="Tab.TFrame")
        
        self.tab_control.add(self.setup_tab, text="Setup")
        self.tab_control.add(self.output_tab, text="Output")
        self.tab_control.pack(expand=1, fill=tk.BOTH, padx=5, pady=5)
        
        # Create setup tab content
        self.create_setup_tab()
        
        # Create output tab content
        self.create_output_tab()
        
        # Initialize variables
        self.generated_file_path = None
        
    def setup_styles(self):
        # Configure style for all widgets
        self.style = ttk.Style()
        
        # Try to use a modern theme if available
        available_themes = self.style.theme_names()
        if 'clam' in available_themes:
            self.style.theme_use('clam')
        
        # Configure frame styles
        self.style.configure('Main.TFrame', background=self.bg_color)
        self.style.configure('Tab.TFrame', background=self.bg_color)
        self.style.configure('Card.TFrame', background=self.card_bg,
                           relief='raised', borderwidth=1)
        
        # Configure label styles
        self.style.configure('TLabel', background=self.bg_color, font=('Segoe UI', 10))
        self.style.configure('Header.TLabel', font=('Segoe UI', 16, 'bold'))
        self.style.configure('Subheader.TLabel', font=('Segoe UI', 12, 'bold'))
        self.style.configure('CardTitle.TLabel', background=self.card_bg, font=('Segoe UI', 11, 'bold'))
        
        # Configure button styles
        self.style.configure('TButton', font=('Segoe UI', 10))
        self.style.configure('Primary.TButton', background=self.primary_color)
        
        # Configure entry styles
        self.style.configure('TEntry', font=('Segoe UI', 10))
        
        # Create a style for card labels
        self.style.configure('Card.TLabel', background=self.card_bg)
        
    def create_header(self):
        header_frame = ttk.Frame(self.main_frame, style='Main.TFrame')
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Logo/Icon would go here if available
        
        # Title
        title_label = ttk.Label(header_frame, text="Codeforces Problem Directory Generator",
                               style='Header.TLabel')
        title_label.pack(pady=10)
        
        # Description 
        desc_text = "Generate an organized directory of problems you've solved on Codeforces"
        desc_label = ttk.Label(header_frame, text=desc_text)
        desc_label.pack(pady=5)
    
    def create_setup_tab(self):
        # Input frame with card-like appearance
        input_frame = ttk.Frame(self.setup_tab, style='Card.TFrame')
        input_frame.pack(fill=tk.X, padx=20, pady=15, ipady=10)
        
        # User Input Section
        ttk.Label(input_frame, text="User Configuration", style='Subheader.TLabel').grid(row=0, column=0, columnspan=3, padx=15, pady=(15, 10), sticky=tk.W)
        
        # Codeforces Username
        ttk.Label(input_frame, text="Codeforces Username:", style='Card.TLabel').grid(
            row=1, column=0, sticky=tk.W, padx=15, pady=8)
        
        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(input_frame, textvariable=self.username_var, width=30)
        username_entry.grid(row=1, column=1, sticky=tk.W, pady=8)
        
        # Compare Handle
        ttk.Label(input_frame, text="Compare with (optional):", style='Card.TLabel').grid(
            row=2, column=0, sticky=tk.W, padx=15, pady=8)
        
        self.compare_handle_var = tk.StringVar()
        compare_handle_entry = ttk.Entry(input_frame, textvariable=self.compare_handle_var, width=30)
        compare_handle_entry.grid(row=2, column=1, sticky=tk.W, pady=8)
        
        # Output directory
        ttk.Label(input_frame, text="Output Directory:", style='Card.TLabel').grid(
            row=3, column=0, sticky=tk.W, padx=15, pady=8)
        
        dir_frame = ttk.Frame(input_frame, style='Card.TFrame')
        dir_frame.grid(row=3, column=1, columnspan=2, sticky=tk.W, pady=8)
        
        self.output_dir_var = tk.StringVar(value=os.path.expanduser("~/codeforces_problems"))
        output_dir_entry = ttk.Entry(dir_frame, textvariable=self.output_dir_var, width=30)
        output_dir_entry.pack(side=tk.LEFT)
        
        browse_button = ttk.Button(dir_frame, text="Browse...", command=self.browse_output_dir)
        browse_button.pack(side=tk.LEFT, padx=5)
        
        # Spacer
        ttk.Frame(input_frame, height=10, style='Card.TFrame').grid(row=4, column=0, columnspan=3)
        
        # Generate Button
        button_frame = ttk.Frame(input_frame, style='Card.TFrame')
        button_frame.grid(row=5, column=0, columnspan=3, pady=15)
        
        self.generate_button = ttk.Button(button_frame, text="Generate Directory", 
                                       command=self.start_generation, style='Primary.TButton',
                                       width=20)
        self.generate_button.pack()
        
        # Status frame
        status_frame = ttk.Frame(self.setup_tab, style='Card.TFrame')
        status_frame.pack(fill=tk.X, padx=20, pady=15, ipady=10)
        
        ttk.Label(status_frame, text="Generation Status", style='Card.TLabel').grid(row=0, column=0, padx=15, pady=(15, 10), sticky=tk.W)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        progress_frame = ttk.Frame(status_frame, style='Card.TFrame')
        progress_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=15, pady=5)
        
        self.progress = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                     maximum=100, length=400)
        self.progress.pack(fill=tk.X)
        
        # Status message
        status_msg_frame = ttk.Frame(status_frame, style='Card.TFrame')
        status_msg_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), padx=15, pady=5)
        
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(status_msg_frame, textvariable=self.status_var,
                                style='Card.TLabel')
        status_label.pack(anchor=tk.W)
        
        # Results info (appears after generation)
        self.results_frame = ttk.Frame(self.setup_tab, style='Card.TFrame')
        
    def create_output_tab(self):
        # Create output text frame
        output_frame = ttk.Frame(self.output_tab)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Output log title
        ttk.Label(output_frame, text="Process Log", style='Subheader.TLabel').pack(anchor=tk.W, pady=(0, 5))
        
        # Output text with scrollbar
        text_frame = ttk.Frame(output_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.output_text = tk.Text(text_frame, wrap=tk.WORD, font=('Consolas', 10))
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.output_text.config(state=tk.DISABLED)
        
        scrollbar = ttk.Scrollbar(text_frame, command=self.output_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.config(yscrollcommand=scrollbar.set)

        # Button to open file (initially hidden)
        self.open_file_button = ttk.Button(output_frame, text="Open Generated Directory", 
                                        command=lambda: self.open_generated_file(self.generated_file_path),
                                        state=tk.DISABLED)
        self.open_file_button.pack(pady=10)
    
    def browse_output_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir_var.set(directory)
    
    def start_generation(self):
        self.tab_control.select(1)  # Switch to output tab
        username = self.username_var.get().strip()
        compare_handle = self.compare_handle_var.get().strip()
        
        if not username:
            messagebox.showerror("Error", "Please enter a Codeforces username")
            return
            
        output_dir = self.output_dir_var.get().strip()
        if not output_dir:
            messagebox.showerror("Error", "Please select an output directory")
            return
            
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                messagebox.showerror("Error", f"Could not create output directory: {str(e)}")
                return
        
        self.generate_button.configure(state=tk.DISABLED)
        self.status_var.set("Generating problem directory...")
        self.progress_var.set(0)
        
        # Clear output text
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)
        
        # Run generation in a separate thread
        threading.Thread(target=self.generate_directory, 
                        args=(username, compare_handle, output_dir), 
                        daemon=True).start()
    
    def update_status(self, message):
        self.root.after(0, lambda: self.status_var.set(message))
        time.sleep(0.5)  # Small delay to show progress
    
    def append_output(self, message):
        self.root.after(0, lambda: self._append_output(message))
    
    def _append_output(self, message):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
    
    def generate_directory(self, username, compare_handle, output_dir):
        try:
            # Step 1: Fetch user's solved problems
            self.progress_var.set(10)
            self.update_status(f"Fetching submissions for {username}...")
            self.append_output(f"Fetching submissions for {username}...")
            
            submissions = self.fetch_user_submissions(username)
            if not submissions:
                self.root.after(0, lambda: messagebox.showerror(
                    "Error", f"No submissions found for {username}"))
                self.root.after(0, lambda: self.reset_ui())
                return
            
            # Step 2: Fetch compare handle's submissions if provided
            compare_submissions = []
            if compare_handle:
                self.progress_var.set(20)
                self.update_status(f"Fetching submissions for comparison handle {compare_handle}...")
                self.append_output(f"Fetching submissions for comparison handle {compare_handle}...")
                compare_submissions = self.fetch_user_submissions(compare_handle)
                if not compare_submissions:
                    self.append_output(f"Warning: No submissions found for comparison handle {compare_handle}")
            
            # Step 3: Extract solved problems and organize by tags
            self.progress_var.set(30)
            self.update_status("Organizing problems by tags...")
            self.append_output("Organizing problems by tags...")
            
            problems_by_tag, compare_solved_set = self.organize_problems_by_tags(
                submissions, compare_submissions)
            
            # Step 4: Generate the directory files
            self.progress_var.set(60)
            self.update_status("Generating directory files...")
            self.append_output("Generating directory files...")
            
            # Create site directory
            site_dir = os.path.join(output_dir, f"codeforces_{username}")
            if os.path.exists(site_dir):
                shutil.rmtree(site_dir)  # Remove old directory if exists
            os.makedirs(site_dir)
            
            # Copy CSS file to site directory
            self.create_css_file(site_dir)
            
            # Generate the index and tag pages
            index_path = self.generate_multi_page_site(
                username, compare_handle if compare_handle else None, 
                problems_by_tag, compare_solved_set, site_dir)
            
            self.generated_file_path = index_path
            
            # Step 5: Complete
            self.progress_var.set(100)
            self.update_status(f"Directory generated successfully at {index_path}")
            self.append_output(f"Directory generated successfully!")
            self.append_output(f"Main page saved at: {index_path}")
            
            # Enable open file button
            self.root.after(0, lambda: self.open_file_button.configure(state=tk.NORMAL))
            
            # Show success message
            self.root.after(0, lambda: self.show_success_message(index_path))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror(
                "Error", f"An error occurred: {str(e)}"))
            self.append_output(f"Error: {str(e)}")
        finally:
            self.root.after(0, lambda: self.reset_ui())
    
    def fetch_user_submissions(self, username):
        try:
            response = requests.get(f"https://codeforces.com/api/user.status?handle={username}")
            response.raise_for_status()
            data = response.json()
            
            if data["status"] == "OK" and data.get("result"):
                return data["result"]
            return []
        except Exception as e:
            self.append_output(f"Error fetching submissions: {e}")
            return []
    
    def organize_problems_by_tags(self, submissions, compare_submissions=None):
        problems_by_tag = defaultdict(list)
        solved_problems = set()  # To avoid duplicates
        
        # Create a set of problems solved by the compare handle
        compare_solved_set = set()
        if compare_submissions:
            for submission in compare_submissions:
                if submission.get("verdict") == "OK" and "problem" in submission:
                    problem = submission["problem"]
                    problem_id = f"{problem.get('contestId', 0)}_{problem.get('index', '')}"
                    compare_solved_set.add(problem_id)
        
        for submission in submissions:
            if submission.get("verdict") == "OK" and "problem" in submission:
                problem = submission["problem"]
                problem_id = f"{problem.get('contestId', 0)}_{problem.get('index', '')}"
                
                if problem_id not in solved_problems:
                    solved_problems.add(problem_id)
                    
                    # Extract problem details
                    problem_info = {
                        "name": problem.get("name", "Unknown"),
                        "contestId": problem.get("contestId", 0),
                        "index": problem.get("index", ""),
                        "rating": problem.get("rating", 0),
                        "link": f"https://codeforces.com/problemset/problem/{problem.get('contestId', 0)}/{problem.get('index', '')}"
                    }
                    
                    # Check if this problem was also solved by compare handle
                    problem_info["solved_by_compare"] = problem_id in compare_solved_set
                    
                    # Add to each tag category
                    if "tags" in problem and problem["tags"]:
                        for tag in problem["tags"]:
                            problems_by_tag[tag].append(problem_info)
                    else:
                        problems_by_tag["Uncategorized"].append(problem_info)
        
        # Sort problems by rating within each tag
        for tag in problems_by_tag:
            problems_by_tag[tag].sort(key=lambda x: (x["rating"] if x["rating"] > 0 else 999999, 
                                                   x["contestId"], x["index"]))
        
        # Sort tags alphabetically
        return dict(sorted(problems_by_tag.items())), compare_solved_set
    
    def create_css_file(self, site_dir):
        # Create a CSS file with improved styling
        css_file = os.path.join(site_dir, "style.css")
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write("""
/* General Styles */
:root {
    --primary-color: #1a73e8;
    --primary-dark: #0d47a1;
    --accent-color: #ff8f00;
    --text-color: #333;
    --light-bg: #f8f9fa;
    --card-shadow: 0 4px 6px rgba(0,0,0,0.1);
    --solved-color: #4caf50;
}

body {
    font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    line-height: 1.6;
    color: var(--text-color);
    background-color: var(--light-bg);
    margin: 0;
    padding: 0;
}

.container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

/* Header Styles */
header {
    background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
    color: white;
    padding: 30px 0;
    margin-bottom: 30px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.header-content {
    text-align: center;
    padding: 0 20px;
}

h1 {
    margin: 0;
    font-size: 2.2rem;
    font-weight: 600;
}

.comparison-info {
    margin-top: 10px;
    background: rgba(255,255,255,0.2);
    display: inline-block;
    padding: 5px 15px;
    border-radius: 20px;
}

.timestamp {
    font-style: italic;
    opacity: 0.8;
    margin-top: 10px;
}

/* Card Styles */
.cards-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
    margin-top: 30px;
}

.card {
    background: white;
    border-radius: 8px;
    box-shadow: var(--card-shadow);
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.12);
}

.card-header {
    background: var(--primary-color);
    color: white;
    padding: 15px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.card-title {
    font-size: 1.1rem;
    font-weight: 600;
    margin: 0;
}

.card-count-container {
    display: flex;
    gap: 10px;
    align-items: center;
}

.card-count, .comparison-count {
    border-radius: 50%;
    width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
}

.card-count {
    background: white;
    color: var(--primary-color);
}

.comparison-count {
    background: var(--solved-color);
    color: white;
    font-size: 0.8rem;
}

.card-body {
    padding: 20px;
}

.card-link {
    display: inline-block;
    padding: 10px 20px;
    background: var(--primary-color);
    color: white;
    text-decoration: none;
    border-radius: 4px;
    font-weight: 500;
    margin-top: 10px;
    transition: background-color 0.2s ease;
}

.card-link:hover {
    background: var(--primary-dark);
}

/* Table Styles */
.problem-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
    box-shadow: var(--card-shadow);
}

.problem-table th,
.problem-table td {
    padding: 15px;
    text-align: left;
    border-bottom: 1px solid #e0e0e0;
}

.problem-table th {
    background-color: var(--primary-color);
    color: white;
    font-weight: 500;
}

.problem-table tr:nth-child(even) {
    background-color: rgba(0,0,0,0.02);
}

.problem-table tr:hover {
    background-color: rgba(26, 115, 232, 0.05);
}

.problem-link {
    color: var(--primary-color);
    text-decoration: none;
    font-weight: 500;
}

.problem-link:hover {
    text-decoration: underline;
}

.rating {
    font-weight: bold;
    color: var(--accent-color);
}

/* Solved by compare styles */
.solved-by-compare {
    position: relative;
}

.solved-by-compare:after {
    content: "✓";
    color: var(--solved-color);
    margin-left: 8px;
    font-weight: bold;
}

/* Back button */
.back-link {
    display: inline-block;
    margin-bottom: 20px;
    color: var(--primary-color);
    text-decoration: none;
    font-weight: 500;
}

.back-link:before {
    content: '←';
    margin-right: 5px;
}

.back-link:hover {
    text-decoration: underline;
}

/* Footer */
footer {
    text-align: center;
    margin-top: 50px;
    padding: 20px;
    color: #666;
    font-size: 0.9rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .cards-container {
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    }
    
    h1 {
        font-size: 1.8rem;
    }
    
    .card-header {
        padding: 12px 15px;
    }
}

@media (max-width: 480px) {
    .cards-container {
        grid-template-columns: 1fr;
    }
    
    .container {
        padding: 15px;
    }
}
""")
    
    def generate_multi_page_site(self, username, compare_handle, problems_by_tag, compare_solved_set, site_dir):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Generate index page
        index_file = os.path.join(site_dir, "index.html")
        
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Codeforces Problems - {username}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <div class="header-content">
            <h1>Codeforces Problems Solved by {username}</h1>
            {f'<div class="comparison-info">Comparing with: {compare_handle}</div>' if compare_handle else ''}
            <p class="timestamp">Generated on: {timestamp}</p>
        </div>
    </header>
    
    <div class="container">
        <h2>Problem Categories</h2>
        
        <div class="cards-container">
""")
            
            # Generate cards for each tag
            for tag, problems in problems_by_tag.items():
                tag_id = tag.replace(' ', '-').replace('*', '').replace('/', '-').lower()
                tag_file = f"{tag_id}.html"
                
                # Count problems also solved by comparison handle
                compare_count = sum(1 for p in problems if p.get("solved_by_compare", False))
                
                # Generate the card for this tag
                f.write(f"""            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">{tag}</h3>
                    <div class="card-count-container">
                        <span class="card-count">{len(problems)}</span>
                        {f'<span class="comparison-count" title="Problems also solved by {compare_handle}">{compare_count}</span>' if compare_handle else ''}
                    </div>
                </div>
                <div class="card-body">
                    <p>View {len(problems)} problems in this category</p>
                    <a href="{tag_file}" class="card-link">View Problems</a>
                </div>
            </div>
""")
                
                # Create the tag-specific page
                self.create_tag_page(username, compare_handle, tag, problems, site_dir, tag_file)
            
            f.write("""        </div>
    </div>
    
    <footer>
        <p>Generated using Codeforces Problem Directory Generator</p>
        <p>Generated on: {timestamp}</p>
    </footer>
</body>
</html>
""".format(timestamp=timestamp))
        
        return index_file
    
    def create_tag_page(self, username, compare_handle, tag, problems, site_dir, tag_file):
        tag_path = os.path.join(site_dir, tag_file)
        
        # Count problems also solved by comparison handle
        compare_count = sum(1 for p in problems if p.get("solved_by_compare", False))
        
        with open(tag_path, 'w', encoding='utf-8') as f:
            f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{tag} Problems - {username}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <div class="header-content">
            <h1>{tag} Problems</h1>
            <p class="timestamp">Problems solved by {username}</p>
            {f'<div class="comparison-info">Comparing with: {compare_handle} ({compare_count}/{len(problems)} also solved)</div>' if compare_handle else ''}
        </div>
    </header>
    
    <div class="container">
        <a href="index.html" class="back-link">Back to Categories</a>
        
        <h2>{tag} Problems ({len(problems)})</h2>
        
        <table class="problem-table">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Problem</th>
                    <th>Rating</th>
                    {f'<th>Solved by {compare_handle}</th>' if compare_handle else ''}
                </tr>
            </thead>
            <tbody>
""")
            
            for i, problem in enumerate(problems, 1):
                rating_str = str(problem["rating"]) if problem["rating"] > 0 else "Unknown"
                problem_name_with_id = f"{problem['contestId']}{problem['index']} - {problem['name']}"
                
                solved_class = " solved-by-compare" if problem.get("solved_by_compare", False) else ""
                
                f.write(f"""                <tr{' class="solved-row"' if problem.get("solved_by_compare", False) else ''}>
                    <td>{i}</td>
                    <td class="{solved_class}"><a href="{problem['link']}" target="_blank" class="problem-link">{problem_name_with_id}</a></td>
                    <td class="rating">{rating_str}</td>
                    {f'<td>{"✓" if problem.get("solved_by_compare", False) else ""}</td>' if compare_handle else ''}
                </tr>
""")
            
            f.write("""            </tbody>
        </table>
    </div>
    
    <footer>
        <p>Generated using Codeforces Problem Directory Generator</p>
    </footer>
</body>
</html>
""")
    
    def reset_ui(self):
        self.generate_button.configure(state=tk.NORMAL)
    
    def show_success_message(self, file_path):
        # Create a results frame if not already showing
        if not self.results_frame.winfo_ismapped():
            self.results_frame.pack(fill=tk.X, padx=20, pady=15, ipady=10)
            
            ttk.Label(self.results_frame, text="Generation Results", style='Card.TLabel').grid(row=0, column=0, padx=15, pady=(15, 10), sticky=tk.W)
            
            success_icon = "✓ "  # Could be replaced with an image
            success_msg = ttk.Label(self.results_frame, 
                                  text=f"{success_icon}Directory generated successfully!", 
                                  style='Card.TLabel',
                                  foreground="#4caf50",
                                  font=('Segoe UI', 11, 'bold'))
            success_msg.grid(row=1, column=0, padx=15, pady=5, sticky=tk.W)
            
            path_msg = ttk.Label(self.results_frame, 
                              text=f"Output saved at:",
                              style='Card.TLabel')
            path_msg.grid(row=2, column=0, padx=15, pady=(5, 0), sticky=tk.W)
            
            path_value = ttk.Label(self.results_frame, 
                                text=file_path,
                                style='Card.TLabel',
                                foreground="#1a73e8")
            path_value.grid(row=3, column=0, padx=25, pady=(0, 10), sticky=tk.W)
            
            button_frame = ttk.Frame(self.results_frame, style='Card.TFrame')
            button_frame.grid(row=4, column=0, padx=15, pady=10)
            
            open_button = ttk.Button(button_frame, text="Open Directory", 
                                  command=lambda: self.open_generated_file(file_path))
            open_button.pack(side=tk.LEFT, padx=5)
            
            new_button = ttk.Button(button_frame, text="Generate Another", 
                                  command=self.reset_results_frame)
            new_button.pack(side=tk.LEFT, padx=5)
    
    def reset_results_frame(self):
        """Hide the results frame to start a new generation"""
        self.results_frame.pack_forget()
        self.tab_control.select(0)  # Switch back to setup tab
    
    def open_generated_file(self, file_path):
        if os.path.exists(file_path):
            webbrowser.open(f"file://{os.path.abspath(file_path)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeforcesProblemDirectory(root)
    root.mainloop()