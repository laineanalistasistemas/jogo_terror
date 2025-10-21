import time
import random
import sys

# Cores ANSI para terminal (funciona no VSCode)
RED = '\033[91m'
WHITE = '\033[97m'
GRAY = '\033[90m'
RESET = '\033[0m'

# Arte ASCII final
ASCII_SKULL = f"""
{RED}      _____
     /     \\
    | () () |
     \\  ^  /
      |||||
      |||||{RESET}
"""

# Perguntas da pesquisa
QUESTIONS = [
    "Você deseja começar a pesquisa?",
    "Você está confortável?",
    "Você gosta de responder perguntas?",
    "Você já fez uma pesquisa antes?",
    "Você lembra como chegou aqui?",
    "Você está sozinho agora?",
    "Você consegue ouvir algo além da minha voz?",
    "Você confia em mim?",
    "Você já mentiu para alguém que ama?",
    "Você se arrepende?",
    "Você acha que merece perdão?",
    "Você ama seu animal de estimação?",
    "Você ficaria triste se ele desaparecesse?",
    "Você já pensou que pode perdê-lo um dia?",
    "Você se sente no controle?",
    "Você gostaria de parar o jogo?",
    "Você tem certeza?",
    "Você gostaria de sair daqui?"
]

def slow_print(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def ask_input(prompt):
    slow_print(f"{WHITE}{prompt}{RESET}")
    return input(f"{GRAY}>> {RESET}").strip()

def main():
    slow_print(f"{RED}=== JOGO DE PESQUISA PSICOLÓGICA ==={RESET}", 0.07)
    name = ask_input("Novo usuário: Digite seu nome")
    slow_print(f"Olá, {name}.")
    
    for i in range(3):
        pwd = ask_input("Digite sua senha:")
        if pwd != "":
            slow_print(f"{RED}Senha incorreta.{RESET}")
        else:
            slow_print(f"{RED}Nada digitado... estranho.{RESET}")
        time.sleep(1)
    
    pet = ask_input("Pergunta de segurança: Qual é o nome do seu animal de estimação?")
    slow_print(f"{WHITE}Verificando...{RESET}")
    time.sleep(2)

    responses = []
    for q in QUESTIONS:
        slow_print(f"\n{WHITE}{q}{RESET}")
        while True:
            ans = input(f"{GRAY}[S/N] >> {RESET}").strip().upper()
            if ans in ['S', 'N']:
                responses.append(ans)
                break
            else:
                slow_print(f"{RED}Resposta inválida. Use apenas S ou N.{RESET}")
    
    slow_print(f"\n{RED}Acordando...{RESET}")
    time.sleep(2)
    slow_print(f"{WHITE}Você respondeu todas as perguntas.{RESET}")
    time.sleep(1)
    slow_print(ASCII_SKULL, 0.02)
    slow_print(f"{RED}Obrigado por participar.{RESET}")
    time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        slow_print(f"\n{RED}Interrompido... mas não deveria.{RESET}")
        sys.exit()
