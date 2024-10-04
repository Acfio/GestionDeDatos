import sys, time, os, subprocess, bcrypt, sqlite3
from getpass import getpass
from rich.console import Console
from rich.progress import track

console = Console()

# Conectar a la base de datos (si no existe, se creará)
conn = sqlite3.connect('login.db')
cursor = conn.cursor()

# Crear la tabla de usuarios (si no existe)
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
)
''')

conn.commit()

verificacion = False
sesion_iniciada = False

# Función para registrar un nuevo usuario
def registrar_usuario(username, password):
    # Hashear la contraseña
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    try:
        # Insertar el nuevo usuario en la base de datos
        cursor.execute('INSyERT INTO usuarios (username, password_hash) VALUES (?, ?)', (username, password_hash))
        conn.commit()
        clear()
        with console.status("[bold green]Registrando...[/]", spinner="dots"):
            time.sleep(2)
        input(f"Usuario {username} registrado correctamente...")
    except sqlite3.IntegrityError:
        clear()
        with console.status("[bold green]Registrando...[/]", spinner="dots"):
            time.sleep(2)
        input(f"Error: El usuario {username} ya está registrado...")
    except valueError:
        clear()
        with console.status("[bold green]Registrando...[/]", spinner="dots"):
            time.sleep(2)
        input(f"Introduce unos valores validos...")

# Función para iniciar sesión
def iniciar_sesion(username, password):
    global sesion_iniciada
    cursor.execute('SELECT password_hash FROM usuarios WHERE username = ?', (username,))
    row = cursor.fetchone()

    if row:
        password_hash = row[0]
        # Verificar si la contraseña coincide
        if bcrypt.checkpw(password.encode(), password_hash):
            clear()
            with console.status("[bold green]Iniciando sesión...[/]", spinner="dots"):
                time.sleep(2)
            print("Inicio de sesión exitoso")
            time.sleep(1)
            sesion_iniciada = True
        else:
            clear()
            with console.status("[bold green]Iniciando sesión...[/]", spinner="dots"):
                time.sleep(2)
            print("Contraseña incorrecta.")
            time.sleep(1)
    else:
        clear()
        with console.status("[bold green]Iniciando sesión...[/]", spinner="dots"):
            time.sleep(2)
        print("Usuario no encontrado.")
        time.sleep(1)
def login():
    global sesion_iniciada
    while not sesion_iniciada:
        clear()
        print("Elige una opción para continuar.")
        print("\n 1) Register")
        print(" 2) Login")
        print(" 3) Exit")

        option = input("\nElige una opción: ")

        if option == '1':
            clear()
            username = input("Introduce el nombre de usuario: ")
            password = getpass("Introduce la contrsaeña: ")
            registrar_usuario(username, password)
            time.sleep(1)
        
        elif option == '2':
            clear()
            username = input("Introduce el nombre de usuario: ")
            password = getpass("Introduce la contaseña: ")
            iniciar_sesion(username, password)

        elif option == '3':
            clear()
            print("Saliendo del programa...")
            time.sleep(1)
            sys.exit(0)
        else:
            input("\nIntroduce una de las tres opciones anteriores...")

def clear():
    while True:
        if os.name == 'nt':
            subprocess.run('cls')
            break
        else:
            subprocess.run('clear')
            break

def main():
    clear()
    global verificacion
    while not verificacion:
        with console.status("[bold green]Iniciando el entorno de trabajo"):
            time.sleep(1.7)
        if os.path.exists('datos.txt'):
            print("Encontrado el archivo con los datos del satelite, procediendo a su apertura y analisis...")
            time.sleep(2.4)
            with console.status("[bold green]Analizando el archivo"):
                time.sleep(1.54)
            verificacion = True
        else:
            print("No se ha encontrado el archivo 'datos.txt', por favor, cuando genere el archivo presione enter...")
            input()
    
    with open ('datos.txt', 'r') as archivo:
        lineas = archivo.readlines()

    datos = []

    for linea in lineas:
        
        valores = linea.strip().split(',')
        datos.append(valores)
    for fila in datos:
        print(fila)
if __name__ == "__main__":
    try:
        clear()
        login()
        main()
    except KeyboardInterrupt:
        print("\nSaliendo del programma...")
        time.sleep(2)
        sys.exit(0)
