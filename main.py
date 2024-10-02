import sys, time, os, subprocess, hashlib

usuarios = []

def hash_password(user, password):
    return hashlib.sha256(password.encode()).hexdigest()

def decode_password(usuarios):
    return hashlib.sha256(password.decode())

def resgistrar_usuario(user, password):
    usuario_decript = decode_password(usuarios)
    if user in usuarios:
        print("El usuario ya está registrado")
    else:
        usuarios = hash_password(user, password)
        print(usuario_decript)

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
            user = input("Introduce el nombre de usuario: ")
            password = input("Introduce la contrsaeña: ")
            usuarios = resgistrar_usuario(user, password)
            input()
            login()
        elif option == '2':
            clear()
            input("\nExito 2")
        elif option == '3':
            clear()
            print("Saliendo del programa...")
            time.sleep(1)
            sys.exit(0)
        else:
            input("\nIntroduce una de las tres opciones anteriores...")
            main()
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
    login()
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSaliendo del programma...")
        time.sleep(2)
        sys.exit(0)
