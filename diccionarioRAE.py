import json
import sys
import os
import mechanicalsoup
from random import randrange as rr

browser = mechanicalsoup.StatefulBrowser(
        soup_config={'features': 'lxml'},  # Use the lxml HTML parser
        raise_on_404=True,
        user_agent='MyBot/0.1: mysite.example.com/bot_info',
    )

def parse_palabra(palabra):
    url = "https://dle.rae.es/"
    definiciones = []
    enlace = url + palabra
    browser.open(enlace)
    paragraphs = browser.page.find_all("p", class_="j")
    pass_this = browser.page.find_all("abbr", class_="g")
    pass_this.extend(browser.page.find_all("abbr", title="nombre masculino"))
    pass_this.extend(browser.page.find_all("abbr", title="nombre femenino"))
    pass_this.extend(browser.page.find_all("abbr", title="nombre masculino y femenino"))
    pass_this.extend(browser.page.find_all("abbr", class_="c"))
    pass_this.extend(browser.page.find_all("span", class_="n_acep"))
    for paragraph in paragraphs:
        texto = ""
        for elemento in paragraph:
            if elemento in pass_this:
                pass
            else:
                texto += elemento.text
        definiciones.append(texto.replace("  ", "").replace("‖ ", "").strip())
    return definiciones


def pasapalabra(d):
    wrdLst = d.keys()
    rndWrd = randomWord(list(wrdLst))
    definiciones = parse_palabra(rndWrd)
    rndDef = rr(len(definiciones))
    definicion = definiciones[rndDef]
    print("\nCon la ", rndWrd[0].upper())
    print(definicion)
    intentos = 1
    tip1 = "La palabra tiene "+str(len(rndWrd))+" letras."
    tip2 = "La palabra termina por", rndWrd[len(rndWrd)-1]
    tips = [tip1, tip2]
    while True:
        if intentos <= 3:
            res = input("¿Cuál es la palabra?\n").lower().strip()
        if res == rndWrd:
            print("¡Acertaste!")
            break
        elif intentos > 2:
            print("Has perdido... la palabra era", rndWrd)
            break
        else:
            print("No es correcto, te quedan "+str(3-intentos)+" intentos.")
            print(tips[intentos-1])
            intentos += 1


def cincoJson(d):
    nd = {}
    for k, v in d.items():
        if v == 5:
            nd[k] = v
    saveDict("json/5.json", nd)
    menu()


def equisJson(d, n):
    nd = {}
    for k, v in d.items():
        if v == n:
            nd[k] = v
    saveDict(str(n)+".json", nd)
    menu()


def frecuencias(d):
    frecuencia_palabras = {}
    frecuencia_palabras_relativas = {}
    for k, v in d.items():
        if len(k) in frecuencia_palabras.keys():
            frecuencia_palabras[len(k)] += 1
        else:
            frecuencia_palabras[len(k)] = 1

    for wrd, frq in frecuencia_palabras.items():
        frecuencia_palabras_relativas[wrd] = frq / len(d) * 100
    saveDict("json/wrd_frq.json", dict(sorted(frecuencia_palabras.items(), key=lambda item: item[1])))
    saveDict("json/wrd_frq_rel.json", dict(sorted(frecuencia_palabras_relativas.items(), key=lambda item: item[1])))
    menu()


def cincoVocalesJson(d):
    nd = {}
    vowels = set("aeiou")
    for k, v in d.items():
        vowels_mirror = set()
        for c in k.replace(
                "á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ü", "u"):
            if c in vowels:
                vowels_mirror.add(c)
            else:
                pass
        if vowels_mirror == vowels:
            nd[k] = v
    saveDict("json/5vocales.json", nd)
    menu()


def longestWord(numbers_list):
    return max(numbers_list)


def randomWord(words_list):
    rand = rr(len(words_list))
    return words_list[rand]


def magicRAE():
    with open('diccionario.txt', encoding='UTF-8') as f1:
        for linea in f1:
            dicc[linea.rstrip()] = len(linea) - 1
        saveDict("json/RAE.json", dicc)
        menu()


def loadDict(file):
    global dicc
    try:
        with open(f"json/{file}") as f1:
            data = json.load(f1)
        dicc = data
    except:
        print("No se pudo cargar el archivo.")


def saveDict(file, d):
    try:
        js = json.dumps(d, indent=4)

        with open(file, "w") as f1:
            f1.write(js)
            print("Diccionario guardado.")
    except:
        print("\nNo se pudo crear el archivo.\n")
    finally:
        input("\nInserte cualquier cosa para continuar...")


def showDict(d):
    max_len = 0
    print("\n El diccionario contiene:")
    for cantidad_letras in d.values():
        if cantidad_letras > max_len:
            max_len = cantidad_letras
    for w, m in d.items():
        print(f"\t {w:{cantidad_letras}s}, tiene {m:3d} letras")


def chkWrd():
    print("\nSi desea salir escriba QUIT")

    wrd = input("Inserte una palabra: ").lower().strip()
    if wrd == "quit":
        menu()
    else:
        if wrd in dicc:
            print(f"\t {wrd} ya existe y tiene {dicc[wrd]} letras.")

        else:
            print(dicc)
            print(f"{wrd} NO está en el diccionario.")
            print("¿Quieres añadirla al diccionario? (Escriba sí o cualquier cosa para no)")
            chk = input("").lower().strip()
            if chk.replace("í", "i") == "si":
                dicc[wrd] = len(wrd)
        chkWrd()


def menu():
    if sys.platform == "win32":
        os.system("cls")
    elif sys.platform == "linux":
        os.system("clear")
    elif sys.platform == "darwin":
        print("Búscate la vida en el appel store")

    print("\n $$ Bienvenido al gestor de diccionarios. $$\n")
    print("\t MAGIC) Genera el archivo RAE.json\n")
    print("\t Cargar) Cargar diccionario")
    print("\t Mostrar) Mostrar diccionario")
    print("\t Insertar) Insertar palabras")
    print("\t Guardar) Guardar diccionario\n")
    print("\t Random) Carga una palabra aleatoria del diccionario en uso.")
    print("\t Longest) Muestra la palabra (o palabras) con el mayor número de letras  del diccionario en uso.")
    print("\t Pasapalabra) Intenta adivinar una palabra por su definición en 3 intentos.")
    print("\t Def) Muestra definiciones de la palabra que quieras.\n")

    print("\t FRQ) Genera los archivos wrd_frq.json y wrd_frq_rel.json")
    print("\t 5) Guarda las palabras de 5 letras en cinco.json")
    print("\t X) Guarda las palabras de X letras en X.json")
    print("\t 5v) Genera el archivo 5vocales.json\n")

    print("\t HELP) Sácame de aquí\n")

    chk = input("Inserte una opción: ").lower().strip()

    if chk == "cargar":
        print("Inserte el nombre del json que desea cargar (ej: diccionario.json)")
        file = input("Nombre del archivo: ").strip()
        loadDict(file)
    elif chk == "mostrar":
        showDict(dicc)
    elif chk == "insertar":
        chkWrd()
    elif chk == "guardar":
        file = input("Nombre del archivo: ").strip()
        saveDict(file, dicc)
        menu()
    elif chk == "longest":
        if len(list(dicc.keys())) == 0:
            print("\nDebe cargar un diccionario o insertar palabras en el actual.")
        else:
            len_wrd = longestWord(list(dicc.values()))
            print("\nLas palabras más largas son:\n")
            for k, v in dicc.items():
                if v >= len_wrd:
                    print(k)
    elif chk == "help":
        exit()
    elif chk == "magic":
        magicRAE()
    elif chk == "def":
        inpWrd = input("¿Qué palabra quieres buscar?\n").lower().strip()
        if parse_palabra(inpWrd):
            counter = 1
            for definicion in parse_palabra(inpWrd):
                print(str(counter) + ". - "+definicion.capitalize()+"\n")
                counter += 1
        else:
            print("No se ha encontrado la palabra", inpWrd.capitalize())
    elif chk == "frq":
        if len(dicc) > 0:
            try:
                frecuencias(dicc)
            except:
                print("Carga un diccionario válido.")
        else:
            print("El diccionario está vacío.")
    elif chk == "5v":
        cincoVocalesJson(dicc)
    elif chk == "5":
        cincoJson(dicc)
    elif chk == "pasapalabra":
        try:
            pasapalabra(dicc)
        except:
            print("Carga un diccionario válido")
    elif chk == "random":
        claves = dicc.keys()
        if len(list(claves)) == 0:
            print("\nDebe cargar un diccionario o insertar palabras en el actual.")
        else:
            chk = False
            while not chk:
                try:
                    i = int(input("¿Cuántas palabras quieres?\n").strip())
                    chk = True
                except:
                    print("\n Inserte un número válido.")

            while i > 0:
                print(randomWord(list(claves)))
                i -= 1
    else:
        print("No entiendo que quieres decirme.")
    input("\nInserte cualquier cosa para continuar...")
    menu()


if __name__ == '__main__':
    dicc = {}
    menu()
