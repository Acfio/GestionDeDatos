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

# Función para registrar un nuevo usuario
def registrar_usuario(username, password):
    # Hashear la contraseña
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    try:
        # Insertar el nuevo usuario en la base de datos
        cursor.execute('INSERT INTO usuarios (username, password_hash) VALUES (?, ?)', (username, password_hash))
        conn.commit()
        print(f"\n[bold green]Usuario {username} registrado correctamente.")
    except sqlite3.IntegrityError:
        print(f"\n[bold green]Error: El usuario {username} ya está registrado.")

# Función para iniciar sesión
def iniciar_sesion(username, password):
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
            main()
        else:
            clear()
            with console.status("[bold green]Iniciando sesión...[/]", spinner="dots"):
                time.sleep(2)
            print("Contraseña incorrecta.")
    else:
        with console.status("[bold green]Iniciando sesión...[/]", spinner="dots"):
            time.sleep(2)
        print("Usuario no encontrado.")

def login():
    while True:
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
    input()
if __name__ == "__main__":
    try:
        clear()
        login()
    except KeyboardInterrupt:
        print("\nSaliendo del programma...")
        time.sleep(2)
        sys.exit(0)
