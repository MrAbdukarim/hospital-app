import customtkinter as ctk
from tkinter import messagebox
import re

uzbek_name_dic = {"Doston", "Abdukarim", "Shohruh", "Sevinch", "Arofat", "Bekzod", "Hamidulloh", "Jasorat",
                  "MuhammadAli"}
patients = []
doctors = [
    {"name": "Dr.Aliyev", "experience": "Psixiatr (Ruhiy kasalliklar bo'yicha)", "room": 101},
    {"name": "Dr.Karimova", "experience": "Nevropatolog (Nerv kasalliklari bo'yicha)", "room": 104},
    {"name": "Dr.Pardayev", "experience": "Stomatolog (Tish va og'iz bo'shlig'i kasalliklari bo'yicha)", "room": 108},
    {"name": "Dr.Rahimov", "experience": "Onkolog (O'sma kasalliklari bo'yicha)", "room": 105},
]


def add_patient():
    name = name_enter.get().strip().capitalize()
    age = age_enter.get().strip()
    illness = illness_enter.get().strip()

    if not all([name, age, illness]):
        messagebox.showwarning("Xatolik bor!", "Hamma maydonlarni to'ldirish shart!")
        return

    if name not in uzbek_name_dic and not messagebox.askyesno("Ogohlantirish",
                                                              f"{name} O'zbek ismlari orasida topilmadi. Davom etasizmi?"):
        return

    if not age.isdigit() or int(age) <= 0 or int(age) > 100:
        messagebox.showerror("Xatolik bo", "Yoshni 1 dan 100 gacha raqam kiriting!")
        return

    patients.append({"name": name, "age": int(age), "illness": illness})
    messagebox.showinfo("Bajarildi!", f"Bemor {name} muvaffaqiyatli qo'shildi!")
    clear_input()


def find_doctor():
    if not patients:
        messagebox.showinfo("Ma'lumot yo'q!", "Bemorlar ro'yxati bo'sh.")
        return

    output = ""
    for patient in patients:
        illness = patient["illness"].lower()
        assigned = False
        for doctor in doctors:
            if any(keyword in illness for keyword in re.findall(r'\w+', doctor["experience"].lower())):
                output += f"{patient['name']} uchun {doctor['name']} (Xona: {doctor['room']})\n"
                assigned = True
                break
        if not assigned:
            output += f"{patient['name']} uchun mos shifokor topilmadi.\n"

    messagebox.showinfo("Shifokorlar", output)


def show_statistic():
    if not patients:
        messagebox.showinfo("Statistika", "Bemorlar ro'yxati bo'sh.")
        return

    total_patients = len(patients)
    specialties = {doctor["experience"]: 0 for doctor in doctors}

    for patient in patients:
        illness = patient["illness"].lower()
        for doctor in doctors:
            if any(keyword in illness for keyword in re.findall(r'\w+', doctor["experience"].lower())):
                specialties[doctor["experience"]] += 1
                break

    output = f"Umumiy bemorlar soni: {total_patients}\n\n"
    for experience, count in specialties.items():
        output += f"{experience}: {count} bemor\n"

    messagebox.showinfo("Statistika", output)


def clear_input():
    for entry in [name_enter, age_enter, illness_enter]:
        entry.delete(0, ctk.END)


def window_app():
    global name_enter, age_enter, illness_enter

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    window = ctk.CTk()
    window.title("Shifoxona Tizimi")
    window.geometry("350x450")

    for text, var in [("Bemor ismi:", "name_enter"), ("Yoshi:", "age_enter"), ("Kasalligi:", "illness_enter")]:
        label = ctk.CTkLabel(window, text=text)
        label.pack(pady=(20 if var == "name_enter" else 10, 0), padx=20, anchor="w")
        entry = ctk.CTkEntry(window, width=310)
        entry.pack(pady=(0, 10), padx=20)
        globals()[var] = entry

    for text, color, command in [
        ("Bemor qo'shish", "#ADD8E6", add_patient),
        ("Shifokor va xona topish", "#90EE90", find_doctor),
        ("Statistika ko'rish", "#F0E68C", show_statistic)
    ]:
        btn = ctk.CTkButton(window, text=text, fg_color=color, text_color="black", width=310, command=command)
        btn.pack(pady=10, padx=20)

    window.mainloop()

window_app()
