from tkinter import *
from tkinter import ttk
import _tkinter
import webbrowser
from functools import partial
import tools
import time
import sqlite3
import winsound
import threading


def menu_animation(event=None):
    global menu_in_animation
    if not menu_in_animation:
        menu_in_animation = True
    else:
        menu_in_animation = False


def clic():
    if cache_bruit_state == 1:
        winsound.PlaySound("clic.wav", winsound.SND_FILENAME)


def leave_image_config(event=None):
    main_canvas.itemconfigure(config_image, state="hidden")


def remove(event=None):
    global in_configuration
    global button_data
    save_connection = sqlite3.connect("Visio.db")
    save_cursor = save_connection.cursor()
    save_cursor.execute("UPDATE button SET type = ?, link = ? WHERE id = ?",
                        (None, None, to_configure_button))
    save_connection.commit()
    save_connection.close()
    main_canvas.itemconfigure(button[to_configure_button], image=fond_none)
    button_data[to_configure_button] = [to_configure_button, None, None]
    in_configuration = False


def save(event):
    global in_configuration
    global button_data
    if config_entry.get() == "":
        remove()
        return
    try:
        button_type = type_list.index(type_menu_var.get())
    except ValueError:
        button_type = None
    save_connection = sqlite3.connect("Visio.db")
    save_cursor = save_connection.cursor()
    save_cursor.execute("UPDATE button SET type = ?, link = ? WHERE id = ?",
                        (button_type, config_entry.get(), to_configure_button))
    save_connection.commit()
    save_connection.close()
    main_canvas.itemconfigure(button[to_configure_button], image=fond_list[button_type])
    button_data[to_configure_button] = [to_configure_button, button_type, config_entry.get()]
    if type_list[button_type] != "Autre":
        main_canvas.itemconfigure(text[to_configure_button], text=type_list[button_type])
    in_configuration = False


def button_animation(button_id, event):
    global clic_thread
    global to_configure_button
    if "Enter" in str(event):
        if settings_mode and not in_configuration and main_canvas.coords(button[0])[0] == 50:
            to_configure_button = button_id
            main_canvas.itemconfigure(config_image, state="normal")
            main_canvas.coords(config_image,
                               main_canvas.coords(button[button_id])[0], main_canvas.coords(button[button_id])[1])
            if not clic_thread.is_alive():
                clic_thread = threading.Thread(target=clic)
                clic_thread.start()
        elif in_configuration and button_id is None:
            if not clic_thread.is_alive():
                clic_thread = threading.Thread(target=clic)
                clic_thread.start()
        elif button_data[button_id][1] is not None and not settings_mode:
            button_in_animation[button_id] = [button_id, True]
            if not clic_thread.is_alive():
                clic_thread = threading.Thread(target=clic)
                clic_thread.start()

    else:
        if not settings_mode and button_data[button_id][1] is not None:
            button_in_animation[button_id] = [button_id, False]


def run(button_id, event=None):
    global stop
    if button_data[button_id][2] is not None and not settings_mode:
        webbrowser.open(button_data[button_id][2])
        stop = True


def settings(event=None):
    global settings_mode
    global in_configuration
    if in_configuration:
        in_configuration = False
    elif settings_mode:
        for t in text:
            main_canvas.itemconfigure(t, state="normal")
        settings_mode = False
    elif not settings_mode:
        menu_animation()
        for t in text:
            main_canvas.itemconfigure(t, state="hidden")
        settings_mode = True


def config(event=None):
    global in_configuration
    in_configuration = True
    if button_data[to_configure_button][1] is not None:
        type_menu_var.set(type_list[button_data[to_configure_button][1]])
    else:
        type_menu_var.set("Autre")
    config_entry.delete(0, END)
    if button_data[to_configure_button][2] is not None:
        config_entry.insert(END, button_data[to_configure_button][2])
    main_canvas.itemconfigure(config_image, state="hidden")


def init():
    x = 50
    y = 150
    for bd in button_data:
        if bd[1] is None:
            text.append(main_canvas.create_text(x + 100, y + 40, text=""))
            transparent_button = main_canvas.create_image(x, y - 50, image=fond_transparent, anchor="nw")
            button.append(main_canvas.create_image(x, y, image=fond_none, anchor="nw"))
        elif type_list[bd[1]] == "Autre":
            text.append(main_canvas.create_text(x + 100, y + 40, text=""))
            transparent_button = main_canvas.create_image(x, y - 50, image=fond_transparent, anchor="nw")
            button.append(main_canvas.create_image(x, y, image=fond_list[bd[1]], anchor="nw"))
        else:
            text.append(main_canvas.create_text(x + 100, y + 40, text=type_list[bd[1]]))
            transparent_button = main_canvas.create_image(x, y - 50, image=fond_transparent, anchor="nw")
            button.append(main_canvas.create_image(x, y, image=fond_list[bd[1]], anchor="nw"))

        main_canvas.tag_bind(button[bd[0]], "<Button-1>", partial(run, bd[0]))
        main_canvas.tag_bind(button[bd[0]], "<Enter>", partial(button_animation, bd[0]))
        main_canvas.tag_bind(button[bd[0]], "<Leave>", partial(button_animation, bd[0]))
        main_canvas.tag_bind(transparent_button, "<Enter>", partial(button_animation, bd[0]))
        main_canvas.tag_bind(transparent_button, "<Leave>", partial(button_animation, bd[0]))

        if bd[0] == 3:
            x = 50
            y = 350
        elif bd[0] == 7:
            break
        else:
            x += 250

    # 400 650 900
    root.update()
    time.sleep(0.2)

    speed = 0.00002
    for t in range(50):
        speed += 0.00003
        for b in button:
            main_canvas.move(b, 0, -1)
        main_canvas.move(parametre_button, -1, 0)
        main_canvas.move(pearltrees_button, -1, 0)
        main_canvas.move(pronote_button, -1, 0)
        main_canvas.move(menu_button, -1, 0)

        root.update()
        time.sleep(speed)


root = Tk()
root.resizable(width=0, height=0)
root.title("Visio")
root.iconbitmap("Logo.ico")
# root.state("zoomed")

connection = sqlite3.connect("Visio.db")
cursor = connection.cursor()
button_data = []
try:
    for n in range(8):
        cursor.execute("SELECT * FROM button WHERE id = ?", (n,))
        button_data.append(cursor.fetchone())
except sqlite3.OperationalError:
    cursor.execute('CREATE TABLE "button" ("id" INTEGER, "type"	INTEGER, "link" TEXT)')
    for n in range(8):
        cursor.execute("INSERT INTO button VALUES(?,?,?)", (n, None, None))
        button_data.append((n, None, None))
    connection.commit()
connection.close()

clic_thread = threading.Thread(target=clic)

icon_parametre = tools.ImageTools.add("icon_parametre.png", 25, 25)
icon_pronote = tools.ImageTools.add("icon_pronote.png", 25, 25)
icon_pearltrees = tools.ImageTools.add("icon_pearltrees.png", 25, 25)
icon_retour = tools.ImageTools.add("retour.png", 25, 25)

fond_physique_chimie = tools.ImageTools.add("physique_chimie.png", 200, 100)
fond_svt = tools.ImageTools.add("svt.png", 200, 100)
fond_science_eco = tools.ImageTools.add("science_eco.png", 200, 100)
fond_allemand = tools.ImageTools.add("allemand.png", 200, 100)
fond_histoire_geo = tools.ImageTools.add("histoire_géo.png", 200, 100)
fond_none = tools.ImageTools.add("none.png", 200, 100)
icon_menu = tools.ImageTools.add("menu.png", 25, 25)
fond_configure = tools.ImageTools.add("back_configure.png")
fond_autre = tools.ImageTools.add("autre.png", 200, 100)
fond_valider = tools.ImageTools.add("valider.png", 100, 25)
fond_supprimer = tools.ImageTools.add("supprimer.png", 150, 25)
fond_transparent = tools.ImageTools.add("transparent.png", 200, 100)
fond_maths = tools.ImageTools.add("maths.png", 200, 100)
fond_espagnol = tools.ImageTools.add("espagnol.png", 200, 100)
fond_anglais = tools.ImageTools.add("anglais.png", 200, 100)
fond_francais = tools.ImageTools.add("francais.png", 200, 100)
fond_latin = tools.ImageTools.add("latin.png", 200, 100)
fond_art = tools.ImageTools.add("art.png", 200, 100)

fond_config = tools.ImageTools.add("config.png", 200, 100)

fond_list = [fond_autre,
             fond_physique_chimie,
             fond_svt,
             fond_histoire_geo,
             fond_allemand,
             fond_science_eco,
             fond_maths,
             fond_espagnol,
             fond_anglais,
             fond_francais,
             fond_latin,
             fond_art]

main_canvas = Canvas(root, bg="white", width=1050, height=500)
main_canvas.pack()

button_in_animation = []
for n in range(8):
    button_in_animation.append([n, False])

button = []
text = []
menu_in_animation = False
stop = False
settings_mode = False
to_configure_button = 0
in_configuration = False

parametre_button = main_canvas.create_image(1100, 10, image=icon_parametre, anchor="ne")
pearltrees_button = main_canvas.create_image(1100, 10, image=icon_pearltrees, anchor="ne")
pronote_button = main_canvas.create_image(1100, 10, image=icon_pronote, anchor="ne")
menu_button = main_canvas.create_image(1100, 10, image=icon_menu, anchor="ne")
retour_button = main_canvas.create_image(1100, 10, image=icon_retour, anchor="ne")
main_canvas.tag_bind(menu_button, "<Button-1>", menu_animation)
main_canvas.tag_bind(pronote_button, "<Button-1>",
                     partial(webbrowser.open, "https://lycees.netocentre.fr/portail/f/accueil/normal/render.uP"))
main_canvas.tag_bind(pearltrees_button, "<Button-1>", partial(webbrowser.open, "https://www.pearltrees.com"))
main_canvas.tag_bind(parametre_button, "<Button-1>", settings)
main_canvas.tag_bind(retour_button, "<Button-1>", settings)

config_label = main_canvas.create_text(525, -15, text="Configuration :", font=("Times New Roman", 20))

configure_canvas_ob = Canvas(main_canvas, width=300, height=400, bg="white", relief="flat")
configure_canvas = main_canvas.create_window(525, 800, window=configure_canvas_ob)
configure_canvas_ob.create_image(150, 200, image=fond_configure)
configure_canvas_ob.create_text(20, 20, text="Matière :", anchor="nw", font=("Times New Roman", 15))
type_menu_var = StringVar(configure_canvas_ob)
type_menu_var.set("Autre")
type_list = ["Autre",
             "Physique chimie",
             "S.V.T.",
             "Histoire géo",
             "Allemand",
             "S.E.S.",
             "Maths",
             "Espagnol",
             "Anglais",
             "Français",
             "Latin",
             "Art"]
type_menu = ttk.OptionMenu(configure_canvas_ob, type_menu_var, *type_list)
configure_canvas_ob.create_window(100, 30, window=type_menu, anchor="w")
preview_button = configure_canvas_ob.create_image(150, 125, image=fond_autre)
config_entry = ttk.Entry(configure_canvas_ob, justify=CENTER)
configure_canvas_ob.create_text(20, 200, text="Lien :", font=("Times New Roman", 15), anchor="w")
configure_canvas_ob.create_window(150, 250, window=config_entry, width=200, height=40)
validate_button = configure_canvas_ob.create_image(225, 350, image=fond_valider)
configure_canvas_ob.tag_bind(validate_button, "<Enter>", partial(button_animation, None))
configure_canvas_ob.tag_bind(validate_button, "<Button-1>", save)
delete_button = configure_canvas_ob.create_image(20, 350, image=fond_supprimer, anchor="w")
configure_canvas_ob.tag_bind(delete_button, "<Enter>", partial(button_animation, None))
configure_canvas_ob.tag_bind(delete_button, "<Button-1>", remove)

bruit_state = IntVar(main_canvas)
bruit_state_check = ttk.Checkbutton(main_canvas, text="Bruits", variable=bruit_state)
bruit_state_check_id = main_canvas.create_window(-50, 20, window=bruit_state_check, anchor="w")

try:
    fichier = open("bruit_state.c", "r")
    bruit_state.set(int(fichier.read()))
except FileNotFoundError:
    fichier = open("bruit_state.c", "w")
    fichier.write("0")
    bruit_state.set(0)
fichier.close()
cache_bruit_state = bruit_state.get()

init()
config_image = main_canvas.create_image(0, 0, image=fond_config, anchor="nw", state="hidden")
main_canvas.tag_bind(config_image, "<Leave>", leave_image_config)
main_canvas.tag_bind(config_image, "<Button-1>", config)

time_cache = 0
while True:
    try:
        if time_cache % 500 == 0:
            for i in button_in_animation:
                if i[0] < 4:
                    if main_canvas.coords(button[i[0]])[1] != 80 and i[1] and not settings_mode \
                            and str(button_data[i[0]][1]) != "None":
                        main_canvas.move(button[i[0]], 0, -1)
                        main_canvas.move(text[i[0]], 0, 1)
                    elif main_canvas.coords(button[i[0]])[1] != 100 and not i[1] and not settings_mode:
                        main_canvas.move(button[i[0]], 0, 1)
                        main_canvas.move(text[i[0]], 0, -1)
                if i[0] > 3:
                    if main_canvas.coords(button[i[0]])[1] != 280 and i[1] \
                            and not settings_mode and str(button_data[i[0]][1]) != "None":
                        main_canvas.move(button[i[0]], 0, -1)
                        main_canvas.move(text[i[0]], 0, 1)
                    elif main_canvas.coords(button[i[0]])[1] != 300 and not i[1] and not settings_mode:
                        main_canvas.move(button[i[0]], 0, 1)
                        main_canvas.move(text[i[0]], 0, -1)
            if menu_in_animation and main_canvas.coords(parametre_button)[0] != 1024:
                main_canvas.move(pronote_button, -8, 0)
                main_canvas.move(pearltrees_button, -5, 0)
                main_canvas.move(parametre_button, -2, 0)
            elif not menu_in_animation and main_canvas.coords(parametre_button)[0] != 1050:
                main_canvas.move(pronote_button, 8, 0)
                main_canvas.move(pearltrees_button, 5, 0)
                main_canvas.move(parametre_button, 2, 0)
        if time_cache % 150 == 0:
            if settings_mode and main_canvas.coords(retour_button)[0] > 1050:
                main_canvas.move(retour_button, -1, 0)
            elif not settings_mode and main_canvas.coords(retour_button)[0] < 1100:
                main_canvas.move(retour_button, 1, 0)
        if time_cache % 300 == 0:
            if settings_mode and main_canvas.coords(config_label)[1] != 40:
                main_canvas.move(config_label, 0, 1)
            elif not settings_mode and main_canvas.coords(config_label)[1] != -15:
                main_canvas.move(config_label, 0, -1)
            if settings_mode and main_canvas.coords(bruit_state_check_id)[0] != 10:
                main_canvas.move(bruit_state_check_id, 1, 0)
            elif not settings_mode and main_canvas.coords(bruit_state_check_id)[0] != -50:
                main_canvas.move(bruit_state_check_id, -1, 0)
        if in_configuration and main_canvas.coords(button[0])[0] != -198:
            main_canvas.move(button[0], -4, 0)
            main_canvas.move(button[1], -8, 0)
            main_canvas.move(button[2], 8, 0)
            main_canvas.move(button[3], 4, 0)
            main_canvas.move(button[4], -4, 0)
            main_canvas.move(button[5], -8, 0)
            main_canvas.move(button[6], 8, 0)
            main_canvas.move(button[7], 4, 0)
        elif not in_configuration and main_canvas.coords(button[0])[0] != 50:
            main_canvas.move(button[0], 4, 0)
            main_canvas.move(button[1], 8, 0)
            main_canvas.move(button[2], -8, 0)
            main_canvas.move(button[3], -4, 0)
            main_canvas.move(button[4], 4, 0)
            main_canvas.move(button[5], 8, 0)
            main_canvas.move(button[6], -8, 0)
            main_canvas.move(button[7], -4, 0)
        if in_configuration and main_canvas.coords(configure_canvas)[1] > 275:
            main_canvas.move(configure_canvas, 0, -8)
        elif not in_configuration and main_canvas.coords(configure_canvas)[1] < 800:
            main_canvas.move(configure_canvas, 0, 8)
        if in_configuration:
            configure_canvas_ob.itemconfigure(preview_button, image=fond_list[type_list.index(type_menu_var.get())])
        if settings_mode and cache_bruit_state != bruit_state.get():
            fichier = open("bruit_state.c", "w")
            fichier.write(str(bruit_state.get()))
            cache_bruit_state = bruit_state.get()
            fichier.close()
        time_cache += 1
        root.update()
    except _tkinter.TclError:
        break
    if stop:
        root.destroy()
        break
