import os
from dataclasses import dataclass


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


if __name__ == "__main__":
    my_resume = InteractiveResume()
    my_resume.run()
