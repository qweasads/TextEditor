import tkinter as tk
import tkinter.scrolledtext as scrolledtext
from tkinter import filedialog, messagebox, simpledialog

def save_file():
    text = text_editor.get("1.0", tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text)

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            text = file.read()
            text_editor.delete("1.0", tk.END)
            text_editor.insert(tk.END, text)

def cut_text():
    text_editor.event_generate("<<Cut>>")

def copy_text():
    text_editor.event_generate("<<Copy>>")

def paste_text():
    text_editor.event_generate("<<Paste>>")

def find_text():
    target = simpledialog.askstring("Найти", "Введите текст, чтобы найти:")
    if target:
        start_idx = text_editor.search(target, "1.0", stopindex=tk.END)
        if start_idx:
            end_idx = f"{start_idx}+{len(target)}c"
            text_editor.tag_remove("found", "1.0", tk.END)
            text_editor.tag_add("found", start_idx, end_idx)
            text_editor.see(start_idx)
        else:
            messagebox.showinfo("Не найдено", "Текст не найден")

def replace_text():
    target = simpledialog.askstring("Заменить", "Введите текст для замены:")
    replace = simpledialog.askstring("Заменить", "Введите текст замены:")
    if target and replace:
        content = text_editor.get("1.0", tk.END)
        new_content = content.replace(target, replace)
        text_editor.delete("1.0", tk.END)
        text_editor.insert("1.0", new_content)

def undo_action(event=None):
    text_editor.edit_undo()

root = tk.Tk()
root.title("Текстовый редактор")

line_numbers = tk.Text(root, width=4, padx=4, bg="lightgrey", state="disabled", wrap="none")
line_numbers.pack(side="left", fill="y")

text_editor = scrolledtext.ScrolledText(root, width=40, height=10, wrap=tk.WORD)
text_editor.pack(padx=10, pady=10)
text_editor.bind("<Control-z>", undo_action)

def update_line_numbers(event=None):
    lines = text_editor.get("1.0", "end-1c").count("\n") + 1
    line_numbers.config(state="normal")
    line_numbers.delete("1.0", "end")
    line_numbers.insert("1.0", "\n".join(str(i) for i in range(1, lines+1)))
    line_numbers.config(state="disabled")

text_editor.bind("<Key>", update_line_numbers)

menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Открыть", command=open_file)
file_menu.add_command(label="Сохранить", command=save_file)
menu_bar.add_cascade(label="Файл", menu=file_menu)

edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Вырезать", command=cut_text)
edit_menu.add_command(label="Копировать", command=copy_text)
edit_menu.add_command(label="Вставить", command=paste_text)
edit_menu.add_command(label="Найти", command=find_text)
edit_menu.add_command(label="Заменить", command=replace_text)
menu_bar.add_cascade(label="Правка", menu=edit_menu)

root.config(menu=menu_bar)
root.mainloop()