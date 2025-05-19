import subprocess
import os
import sys
import time
import traceback
import platform
import threading

def start_flask():
    print("Verificando backend...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(base_dir, "backend")
    if platform.system() == "Windows":
        venv_python = os.path.join(backend_dir, "venv", "Scripts", "python.exe")
    else:
        venv_python = os.path.join(backend_dir, "venv", "bin", "python")
    server_path = os.path.join(backend_dir, "api.py")

    if not os.path.exists(backend_dir):
        print(f"Erro: Diretório backend não encontrado em {backend_dir}")
        sys.exit(1)
    if not os.path.exists(server_path):
        print(f"Erro: {os.path.basename(server_path)} não encontrado em {server_path}")
        sys.exit(1)
    # Só exige venv no Linux
    if platform.system() != "Windows" and not os.path.exists(venv_python):
        print(f"Erro: Python do ambiente virtual não encontrado em {venv_python}")
        print("Crie o ambiente virtual com: cd backend && python3 -m venv venv && source venv/bin/activate && pip install flask flask-cors pyserial")
        sys.exit(1)
    # No Windows, usa o Python global se o venv não existir
    if platform.system() == "Windows" and not os.path.exists(venv_python):
        venv_python = sys.executable

    print(f"Iniciando Flask com {venv_python} {server_path}")
    try:
        process = subprocess.Popen(
            [venv_python, server_path],
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return process
    except Exception as e:
        print(f"Erro ao iniciar Flask: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

def start_react():
    print("Verificando frontend...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    frontend_dir = os.path.join(base_dir, "frontend")

    if not os.path.exists(frontend_dir):
        print(f"Erro: Diretório frontend não encontrado em {frontend_dir}")
        sys.exit(1)

    print(f"Iniciando React (desenvolvimento) em {frontend_dir}")
    npm_cmd = "npm.cmd" if platform.system() == "Windows" else "npm"
    try:
        process = subprocess.Popen(
            [npm_cmd, "start"],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return process
    except Exception as e:
        print(f"Erro ao iniciar React: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

def log_output(process, name):
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(f"[{name}] {output.strip()}")
        error = process.stderr.readline()
        if error == '' and process.poll() is not None:
            break
        if error:
            print(f"[{name} ERRO] {error.strip()}")

def main():
    print(f"Diretório atual: {os.getcwd()}")
    print("Iniciando servidores...")

    flask_process = None
    react_process = None

    try:
        flask_process = start_flask()
        print("API Flask disponível em: http://localhost:5000")
        time.sleep(2)
        react_process = start_react()
        print("Site (React) disponível em: http://localhost:3000")

        flask_thread = threading.Thread(target=log_output, args=(flask_process, "Flask"))
        react_thread = threading.Thread(target=log_output, args=(react_process, "React"))
        flask_thread.start()
        react_thread.start()

        while True:
            if flask_process.poll() is not None:
                print("Erro: Servidor Flask terminou inesperadamente")
                break
            if react_process.poll() is not None:
                print("Erro: Servidor React terminou inesperadamente")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nEncerrando servidores...")
        if flask_process:
            flask_process.terminate()
            flask_process.wait()
        if react_process:
            react_process.terminate()
            react_process.wait()
        print("Servidores encerrados.")
    except Exception as e:
        print(f"Erro geral: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()