#updated by Amaan - testing git workflow
import tkinter as tk
from tkinter import font
from tkinter import filedialog

root = tk.Tk()
root.title("NoTToday")
root.geometry("900x650")


file_path = None
dark_mode = False

current_font_family = "Arial"
current_font_size = 14

text_area = tk.Text(root, wrap="word", undo=True)
text_area.pack(expand=True, fill="both")


status_bar = tk.Label(root, text="Words: 0 | Characters: 0", anchor="e")
status_bar.pack(fill="x", side="bottom")


def new_file():
    global file_path
    text_area.delete(1.0, tk.END)
    file_path = None
    root.title("Untitled - NoTToday")

def open_file():
    global file_path
    file_path = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt"),("C File", ".c"),("C++ File",".cpp"),("Python File", ".py"),("All Files", "*.*")]
    )
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, file.read())
        root.title(f"{file_path} - NoTToday")

def save_file():
    global file_path
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text_area.get(1.0, tk.END))
    else:
        save_as_file()

def save_as_file():
    global file_path
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"),("C File", ".c"),("C++ File",".cpp"),("Python File", ".py"),("All Files", "*.*")]
    )
    if file_path:
        save_file()
        root.title(f"{file_path} - NoTToday")



def apply_theme():
    if dark_mode:
        text_area.config(bg="#1e1e1e", fg="white", insertbackground="white")
        status_bar.config(bg="#2e2e2e", fg="white")
    else:
        text_area.config(bg="white", fg="black", insertbackground="black")
        status_bar.config(bg="#f0f0f0", fg="black")

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode

    if dark_mode:
        view_menu.entryconfig(0, label="Light Mode")
    else:
        view_menu.entryconfig(0, label="Dark Mode")

    apply_theme()


def update_status(event=None):
    content = text_area.get("1.0", tk.END)
    words = len(content.split())
    chars = len(content) - 1
    status_bar.config(text=f"Words: {words} | Characters: {chars}")

text_area.bind("<KeyRelease>", update_status)
root.bind("<Control-s>", lambda event: save_file())
root.bind("<Control-o>", lambda event: open_file())
root.bind("<Control-f>", lambda event: find_replace())


def change_font_family(family):
    global current_font_family
    current_font_family = family
    update_font()

def change_font_size(size):
    global current_font_size
    current_font_size = size
    update_font()

def update_font():
    new_font = font.Font(family=current_font_family, size=current_font_size)
    text_area.config(font=new_font)

def toggle_bold(event=None):
    try:
        current_tags = text_area.tag_names("sel.first")

        if "bold" in current_tags:
            text_area.tag_remove("bold", "sel.first", "sel.last")
        else:
            bold_font = font.Font(text_area, text_area.cget("font"))
            bold_font.configure(weight="bold")
            text_area.tag_configure("bold", font=bold_font)
            text_area.tag_add("bold", "sel.first", "sel.last")

    except:
        pass
root.bind("<Control-b>", toggle_bold)

def find_replace():
    find_window = tk.Toplevel(root)
    find_window.title("Find & Replace")
    find_window.geometry("320x180")

    tk.Label(find_window, text="Find:").pack()
    find_entry = tk.Entry(find_window, width=30)
    find_entry.pack()

    tk.Label(find_window, text="Replace:").pack()
    replace_entry = tk.Entry(find_window, width=30)
    replace_entry.pack()

    def find_text():
        text_area.tag_remove("highlight", "1.0", tk.END)
        word = find_entry.get()

        if word:
            start = "1.0"
            while True:
                start = text_area.search(word, start, stopindex=tk.END)
                if not start:
                    break
                end = f"{start}+{len(word)}c"
                text_area.tag_add("highlight", start, end)
                start = end

            
            text_area.tag_config("highlight", background="orange", foreground="black")

    def replace_text():
        word = find_entry.get()
        replace = replace_entry.get()
        content = text_area.get("1.0", tk.END)
        new_content = content.replace(word, replace)
        text_area.delete("1.0", tk.END)
        text_area.insert("1.0", new_content)

    tk.Button(find_window, text="Find", command=find_text).pack(pady=4)
    tk.Button(find_window, text="Replace All", command=replace_text).pack(pady=4)



menu_bar = tk.Menu(root)


file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)


edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Find & Replace", command=find_replace)
menu_bar.add_cascade(label="Edit", menu=edit_menu)


view_menu = tk.Menu(menu_bar, tearoff=0)
view_menu.add_command(label="Dark Mode", command=toggle_theme)
menu_bar.add_cascade(label="View", menu=view_menu)


font_menu = tk.Menu(menu_bar, tearoff=0)


font_family_menu = tk.Menu(font_menu, tearoff=0)
for f in ["Arial", "Calibri", "Courier", "Times New Roman"]:
    font_family_menu.add_command(label=f, command=lambda f=f: change_font_family(f))


font_size_menu = tk.Menu(font_menu, tearoff=0)
for s in [10, 12, 14, 16, 18, 20]:
    font_size_menu.add_command(label=str(s), command=lambda s=s: change_font_size(s))

font_menu.add_cascade(label="Font Family", menu=font_family_menu)
font_menu.add_cascade(label="Font Size", menu=font_size_menu)

menu_bar.add_cascade(label="Format", menu=font_menu)

root.config(menu=menu_bar)

apply_theme()
update_font()

root.mainloop()