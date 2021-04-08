import tkinter
from tkinter import ttk
from tkinter import filedialog
import webbrowser
from functools import partial
import tools
import time
import json


def leave_image_config(event=None):
    main_canvas.itemconfigure(config_image, state="hidden")


def remove(event=None):
    global button_data
    global in_configuration
    button_data[button_to_configure] = [None, "Textures/none.png", None]
    main_canvas.itemconfigure(configure_canvas_id, state="hidden")
    main_canvas.itemconfigure(configure_frame_back_id, state="hidden")
    main_canvas.itemconfigure(pearltrees_button, state="normal")
    main_canvas.itemconfigure(pronote_button, state="normal")
    main_canvas.itemconfigure(menu_button, state="normal")
    in_configuration = False
    for n in range(8):
        main_canvas.itemconfigure(button[n], state="normal")
        main_canvas.itemconfigure(text[n], state="normal")
    reload()


def save(event=None):
    global button_data
    global in_configuration
    if url_entry.get() == "":
        remove()
        return
    button_data[button_to_configure] = [matiere_entry.get(), image_path, url_entry.get()]
    for n in range(8):
        main_canvas.itemconfigure(button[n], state="normal")
        main_canvas.itemconfigure(text[n], state="normal")
    main_canvas.itemconfigure(configure_canvas_id, state="hidden")
    main_canvas.itemconfigure(configure_frame_back_id, state="hidden")
    main_canvas.itemconfigure(pearltrees_button, state="normal")
    main_canvas.itemconfigure(pronote_button, state="normal")
    main_canvas.itemconfigure(menu_button, state="normal")
    in_configuration = False
    reload()


def button_animation(button_id, event):
    global button_to_configure
    if "Enter" in str(event):
        if settings_mode and not in_configuration:
            main_canvas.itemconfigure(config_image, state="normal")
            main_canvas.coords(config_image,
                               main_canvas.coords(button[button_id])[0], main_canvas.coords(button[button_id])[1])
            button_to_configure = button_id
        elif button_data[button_id][0] is not None and not settings_mode:
            main_canvas.move(button[button_id], 0, -10)
            main_canvas.move(text[button_id], 0, 10)
    else:
        if not settings_mode and button_data[button_id][0] is not None:
            main_canvas.move(button[button_id], 0, 10)
            main_canvas.move(text[button_id], 0, -10)


def menu_animation(event=None):
    global menu_open
    if not menu_open:
        menu_open = True
        for d in range(15):
            main_canvas.move(pearltrees_button, -2, 0)
            main_canvas.move(pronote_button, -4, 0)
            main_canvas.move(parametre_button, -6, 0)
            root.update()
            time.sleep(0.00002)
    else:
        menu_open = False
        main_canvas.coords(pearltrees_button, 1040, 10)
        main_canvas.coords(pronote_button, 1040, 10)
        main_canvas.coords(parametre_button, 1040, 10)


def run(button_id, event=None):
    if button_data[button_id][2] is not None:
        webbrowser.open(button_data[button_id][2])


def settings(event=None):
    global settings_mode
    global menu_open
    settings_mode = True
    main_canvas.itemconfigure(config_label, state="normal")
    main_canvas.itemconfigure(retour_button, state="normal")
    if menu_open:
        for d in range(15):
            main_canvas.move(pearltrees_button, 2, 0)
            main_canvas.move(pronote_button, 4, 0)
            main_canvas.move(parametre_button, 6, 0)
            root.update()
            time.sleep(0.00002)
        menu_open = False


def retour_action(event=None):
    global in_configuration
    global settings_mode
    if in_configuration:
        for n in range(8):
            main_canvas.itemconfigure(button[n], state="normal")
            main_canvas.itemconfigure(text[n], state="normal")
        main_canvas.itemconfigure(configure_canvas_id, state="hidden")
        main_canvas.itemconfigure(configure_frame_back_id, state="hidden")
        main_canvas.itemconfigure(pearltrees_button, state="normal")
        main_canvas.itemconfigure(pronote_button, state="normal")
        main_canvas.itemconfigure(menu_button, state="normal")
        in_configuration = False
    else:
        main_canvas.itemconfigure(config_label, state="hidden")
        main_canvas.itemconfigure(retour_button, state="hidden")
        main_canvas.itemconfigure(config_image, state="hidden")
        settings_mode = False


def config(event=None):
    global in_configuration
    global fond_preview_button
    global image_path
    in_configuration = True
    url_entry.delete(0, "end")
    matiere_entry.delete(0, "end")
    if button_data[button_to_configure][2] is not None:
        url_entry.insert(0, button_data[button_to_configure][2])
    if button_data[button_to_configure][0]:
        matiere_entry.insert(0, button_data[button_to_configure][0])
    if button_data[button_to_configure][1] != "Textures/none.png":
        try:
            fond_preview_button = tools.ImageTools.add(button_data[button_to_configure][1], 200, 100)
        except FileNotFoundError:
            fond_preview_button = tools.ImageTools.add("Textures/none.png", 200, 100)
        configure_canvas.itemconfigure(preview_button, image=fond_preview_button)
    else:
        fond_preview_button = tools.ImageTools.add("Textures/Fonds/autre.png")
        configure_canvas.itemconfigure(preview_button, image=fond_preview_button)
        image_path = "Textures/Fonds/autre.png"
    main_canvas.itemconfigure(config_image, state="hidden")
    main_canvas.itemconfigure(configure_canvas_id, state="normal")
    main_canvas.itemconfigure(configure_frame_back_id, state="normal")
    main_canvas.itemconfigure(pearltrees_button, state="hidden")
    main_canvas.itemconfigure(pronote_button, state="hidden")
    main_canvas.itemconfigure(menu_button, state="hidden")
    for n in range(8):
        main_canvas.itemconfigure(button[n], state="hidden")
        main_canvas.itemconfigure(text[n], state="hidden")


def reload():
    global button_fonds
    for button_n in range(len(button)):
        try:
            button_fonds[button_n] = tools.ImageTools.add(button_data[button_n][1], 200, 100)
        except FileNotFoundError:
            button_fonds[button_n] = tools.ImageTools.add("Textures/none.png", 200, 100)
        main_canvas.itemconfigure(button[button_n], image=button_fonds[button_n])
        if button_data[button_n][0] is not None:
            main_canvas.itemconfigure(text[button_n], text=button_data[button_n][0])
        else:
            main_canvas.itemconfigure(text[button_n], text="")


def hand_cursor(event=None):
    if "Enter" in str(event):
        root.configure(cursor="hand2")
    else:
        root.configure(cursor="arrow")


def select_image(event=None):
    global image_path
    global fond_preview_button
    image_path = tkinter.filedialog.askopenfilename()
    fond_preview_button = tools.ImageTools.add(image_path, 200, 100)
    configure_canvas.itemconfigure(preview_button, image=fond_preview_button)


root = tkinter.Tk()
root.resizable(width=0, height=0)
root.title("Visio")
root.iconbitmap("Textures/Logo.ico")

first_launch = False
try:
    fichier = open("data.json", "r")
    button_data = json.load(fichier)["data"]
except FileNotFoundError:
    fichier = open("data.json", "w")
    data = {"data": [[None, "Textures/none.png", None],
                     [None, "Textures/none.png", None],
                     [None, "Textures/none.png", None],
                     [None, "Textures/none.png", None],
                     [None, "Textures/none.png", None],
                     [None, "Textures/none.png", None],
                     [None, "Textures/none.png", None],
                     [None, "Textures/none.png", None]]}
    first_launch = True
    fichier.write(json.dumps(data))
    button_data = data["data"]
fichier.close()

icon_parametre = tools.ImageTools.add("Textures/icon_parametre.png", 25, 25)
icon_pronote = tools.ImageTools.add("Textures/icon_pronote.png", 25, 25)
icon_pearltrees = tools.ImageTools.add("Textures/icon_pearltrees.png", 25, 25)
icon_retour = tools.ImageTools.add("Textures/retour.png", 25, 25)
icon_menu = tools.ImageTools.add("Textures/menu.png", 25, 25)

fond_configure = tools.ImageTools.add("Textures/back_configure.png")
fond_transparent = tools.ImageTools.add("Textures/transparent.png", 200, 100)
fond_config = tools.ImageTools.add("Textures/config.png", 200, 100)
fond_preview_button = tools.ImageTools.add("Textures/Fonds/autre.png", 200, 100)
configure_frame_back = tools.ImageTools.add("Textures/cours-en-ligne.jpg", 1050, 500)

main_canvas = tkinter.Canvas(root, bg="white", width=1050, height=500)
main_canvas.pack()

button = []
text = []
settings_mode = False
in_configuration = False
button_to_configure = 0
button_fonds = [None, None, None, None, None, None, None, None]
image_path = ""
menu_open = False

# Initialisation du menu
configure_frame_back_id = main_canvas.create_image(0, 0, image=configure_frame_back, anchor="nw", state="hidden")
parametre_button = main_canvas.create_image(1040, 10, image=icon_parametre, anchor="ne")
pearltrees_button = main_canvas.create_image(1040, 10, image=icon_pearltrees, anchor="ne")
pronote_button = main_canvas.create_image(1040, 10, image=icon_pronote, anchor="ne")
menu_button = main_canvas.create_image(1040, 10, image=icon_menu, anchor="ne")
retour_button = main_canvas.create_image(1040, 10, image=icon_retour, anchor="ne", state="hidden")
main_canvas.tag_bind(menu_button, "<Button-1>", menu_animation)
main_canvas.tag_bind(pronote_button, "<Button-1>",
                     partial(webbrowser.open, "https://0280015p.index-education.net/pronote/eleve.html"))
main_canvas.tag_bind(pearltrees_button, "<Button-1>", partial(webbrowser.open, "https://www.pearltrees.com"))
main_canvas.tag_bind(parametre_button, "<Button-1>", settings)
main_canvas.tag_bind(retour_button, "<Button-1>", retour_action)

# Initialisation du mode configuration
config_label = main_canvas.create_text(525, 20, text="Configuration :", font=("Times New Roman", 20), state="hidden")

# Initialisation frame configuration
configure_canvas = tkinter.Canvas(main_canvas, width=300, height=400, bg="white", relief="flat")
configure_canvas_id = main_canvas.create_window(800, 250, window=configure_canvas, state="hidden")
configure_canvas.create_image(150, 200, image=fond_configure)
configure_canvas.create_text(20, 20, text="Matière :", anchor="nw", font=("Times New Roman", 15))

preview_button = configure_canvas.create_image(150, 125, image=fond_preview_button)
configure_canvas.tag_bind(preview_button, "<Enter>", hand_cursor)
configure_canvas.tag_bind(preview_button, "<Leave>", hand_cursor)
configure_canvas.tag_bind(preview_button, "<Button-1>", select_image)
url_entry = ttk.Entry(configure_canvas, justify="center")
matiere_entry = ttk.Entry(configure_canvas)
configure_canvas.create_window(100, 20, height=24, width=150, window=matiere_entry, anchor="nw")
configure_canvas.create_text(20, 200, text="Lien :", font=("Times New Roman", 15), anchor="w")
configure_canvas.create_window(150, 250, window=url_entry, width=200, height=40)
validate_button = ttk.Button(configure_canvas, text="Valider", command=save)
validate_button_id = configure_canvas.create_window(280, 350, window=validate_button, width=150, anchor="e")
delete_button = ttk.Button(configure_canvas, text="Supprimer", command=remove)
delete_button_id = configure_canvas.create_window(20, 350, window=delete_button, width=100, anchor="w")

# Création des boutons
x = 50
y = 150
n = 0
for bd in button_data:
    text.append(main_canvas.create_text(x + 100, y + 40, text=""))
    transparent_button = main_canvas.create_image(x, y - 50, image=fond_transparent, anchor="nw")
    main_canvas.tag_bind(transparent_button, "<Enter>", partial(button_animation, n))
    main_canvas.tag_bind(transparent_button, "<Leave>", partial(button_animation, n))
    if not first_launch:
        button.append(main_canvas.create_image(x, y, anchor="nw"))
    else:
        button.append(main_canvas.create_image(x, y-50, anchor="nw"))
    main_canvas.tag_bind(button[n], "<Button-1>", partial(run, n))
    main_canvas.tag_bind(button[n], "<Enter>", partial(button_animation, n))
    main_canvas.tag_bind(button[n], "<Leave>", partial(button_animation, n))

    if n == 3:
        x = 50
        y = 350
    elif n == 7:
        break
    else:
        x += 250
    n += 1

config_image = main_canvas.create_image(0, 0, image=fond_config, anchor="nw", state="hidden")
main_canvas.tag_bind(config_image, "<Leave>", leave_image_config)
main_canvas.tag_bind(config_image, "<Button-1>", config)

if not first_launch:
    # Animation au lancement
    reload()
    root.update()
    time.sleep(0.2)
    for t in range(25):
        for b in button:
            main_canvas.move(b, 0, -2)
        root.update()
        time.sleep(0.0005)
    reload()

else:
    reload()
    settings()
    button_to_configure = 0
    config()

root.mainloop()
fichier = open("data.json", "w")
fichier.write(json.dumps({"data": button_data}))
