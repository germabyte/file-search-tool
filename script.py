import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, Listbox
import os
import re
from docx import Document
from threading import Thread

class FileSearchApp:
    def __init__(self, window):
        self.window = window
        self.window.title("File Search Tool")
        self.window.geometry("800x600")
        self.create_widgets()
        self.search_thread = None
        self.running = False

    def create_widgets(self):
        options_frame = tk.Frame(self.window)
        options_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        tk.Label(options_frame, text="Directory:").grid(row=0, column=0, sticky='w')
        self.directory_entry = tk.Entry(options_frame, width=50)
        self.directory_entry.grid(row=0, column=1, sticky='we')
        tk.Button(options_frame, text="Browse...", command=self.select_directory).grid(row=0, column=2)

        tk.Label(options_frame, text="Search Text:").grid(row=1, column=0, sticky='w')
        self.content_entry = tk.Entry(options_frame, width=50)
        self.content_entry.grid(row=1, column=1, sticky='we')

        self.use_regex_var = tk.BooleanVar()
        self.include_subdirs_var = tk.BooleanVar()
        self.case_sensitive_var = tk.BooleanVar()
        tk.Checkbutton(options_frame, text="Use Regular Expression", variable=self.use_regex_var).grid(row=2, column=0, sticky='w')
        tk.Checkbutton(options_frame, text="Include Subdirectories", variable=self.include_subdirs_var).grid(row=2, column=1, sticky='w')
        tk.Checkbutton(options_frame, text="Case Sensitive", variable=self.case_sensitive_var).grid(row=2, column=2, sticky='w')

        self.search_button = tk.Button(options_frame, text="Search", command=self.start_search)
        self.search_button.grid(row=3, column=1, sticky='e')
        self.cancel_button = tk.Button(options_frame, text="Cancel", command=self.cancel_search, state='disabled')
        self.cancel_button.grid(row=3, column=2, sticky='w')

        self.reset_button = tk.Button(options_frame, text="Reset", command=self.reset_search)
        self.reset_button.grid(row=3, column=0, sticky='w')

        self.progress_label = tk.Label(self.window, text="Idle", anchor='w')
        self.progress_label.grid(row=1, column=0, sticky='ew', padx=10)

        self.results_frame = tk.Frame(self.window)
        self.results_frame.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)
        self.window.grid_rowconfigure(2, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        self.results_listbox = Listbox(self.results_frame, activestyle='none', font=('TkDefaultFont', 9), width=70, height=15)
        self.results_listbox.pack(side="left", fill="both", expand=True)
        self.results_listbox.bind("<<ListboxSelect>>", self.on_result_select)

        self.results_scrollbar = tk.Scrollbar(self.results_frame, orient="vertical", command=self.results_listbox.yview)
        self.results_scrollbar.pack(side="right", fill="y")
        self.results_listbox.config(yscrollcommand=self.results_scrollbar.set)

        context_label = tk.Label(self.window, text="Context Snippet:")
        context_label.grid(row=3, column=0, sticky='w', padx=10)

        self.context_text = scrolledtext.ScrolledText(self.window, height=10, wrap=tk.WORD, state='disabled')
        self.context_text.grid(row=4, column=0, sticky='nsew', padx=10, pady=10)

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory_entry.delete(0, tk.END)
            self.directory_entry.insert(0, directory)

    def start_search(self):
        directory = self.directory_entry.get()
        search_text = self.content_entry.get()
        use_regex = self.use_regex_var.get()
        include_subdirs = self.include_subdirs_var.get()
        case_sensitive = self.case_sensitive_var.get()

        if not directory:
            messagebox.showerror("Error", "Please specify a directory.")
            return

        if not search_text.strip():
            messagebox.showerror("Error", "Please enter the text to search.")
            return

        self.progress_label.config(text="Searching...")
        self.search_button.config(state='disabled')
        self.cancel_button.config(state='normal')
        self.running = True

        self.search_thread = Thread(target=self.search_files, args=(directory, search_text, use_regex, include_subdirs, case_sensitive), daemon=True)
        self.search_thread.start()

    def cancel_search(self):
        if self.search_thread:
            self.running = False
            self.search_thread.join()
            self.progress_label.config(text="Search Cancelled.")
            self.search_button.config(state='normal')
            self.cancel_button.config(state='disabled')

    def reset_search(self):
        self.results_listbox.delete(0, tk.END)
        self.display_context("")
        self.progress_label.config(text="Idle")
        self.directory_entry.delete(0, tk.END)
        self.content_entry.delete(0, tk.END)
        self.use_regex_var.set(False)
        self.include_subdirs_var.set(False)
        self.case_sensitive_var.set(False)

    def on_result_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            context = self.results_listbox.get(index)
            self.display_context(context)

    def search_files(self, directory, search_text, use_regex, include_subdirs, case_sensitive):
        allowed_extensions = ['.docx', '.txt', '.html', '.rtf']
        self.results_listbox.delete(0, tk.END)
        for root, dirnames, filenames in os.walk(directory):
            if not include_subdirs:
                dirnames[:] = []
            for filename in filenames:
                if not self.running:
                    return
                if not any(filename.endswith(ext) for ext in allowed_extensions):
                    continue

                filepath = os.path.join(root, filename)
                self.update_progress(f"Analyzing: {filepath}")
                try:
                    file_content = self.read_text_from_file(filepath)
                    contexts = self.extract_context(file_content, search_text, 30, use_regex, case_sensitive)
                    for context in contexts:
                        self.results_listbox.insert(tk.END, f"{filepath} - {context['text']}: {context['context']}")
                except Exception as e:
                    messagebox.showwarning("Warning", f"Could not read {filepath}: {e}")

        self.update_progress("Search Completed.")
        self.search_button.config(state='normal')
        self.cancel_button.config(state='disabled')

    def display_context(self, context):
        self.context_text.config(state='normal')
        self.context_text.delete(1.0, tk.END)
        self.context_text.insert(tk.END, context)
        self.context_text.config(state='disabled')

    def extract_context(self, content, search_text, num_words, use_regex, case_sensitive):
        contexts = []
        flags = 0 if case_sensitive else re.IGNORECASE
        pattern = re.escape(search_text) if not use_regex else search_text
        for match in re.finditer(pattern, content, flags):
            start_pos, end_pos = match.span()
            words_before = content[:start_pos].split()[-num_words//2:]
            words_after = content[end_pos:].split()[:num_words//2]
            context_text = ' '.join(words_before + [match.group()] + words_after)
            contexts.append({'text': match.group(), 'context': context_text})

        return contexts

    def update_progress(self, message):
        self.progress_label.config(text=message)
        self.window.update_idletasks()

    def read_text_from_file(self, filepath):
        if filepath.endswith('.docx'):
            try:
                doc = Document(filepath)
                return "\n".join(paragraph.text for paragraph in doc.paragraphs)
            except Exception as e:
                raise Exception(f"Error reading DOCX file: {e}")
        else:
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                    return file.read()
            except Exception as e:
                raise Exception(f"Error reading file: {e}")

# Run the GUI
window = tk.Tk()
app = FileSearchApp(window)
window.mainloop()
