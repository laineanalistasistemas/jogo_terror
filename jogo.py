import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 1280, 720
FPS = 60
FONT_NAME = pygame.font.get_default_font()
BG_COLOR = (5, 5, 8)
TEXT_COLOR = (220, 220, 220)
ACCENT = (255, 30, 30)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Survey - Psychological Horror")
clock = pygame.time.Clock()
font = pygame.font.Font(FONT_NAME, 28)
large_font = pygame.font.Font(FONT_NAME, 48)
small_font = pygame.font.Font(FONT_NAME, 22)

ENTER_NAME = 'enter_name'
ENTER_PASS = 'enter_pass'
ENTER_PET = 'enter_pet'
SURVEY = 'survey'
FINAL = 'final'
state = ENTER_NAME

player_name = ''
pass_errors = 0
pet_name = ''
password_attempt = ''
current_q = 0
responses = []
show_pass_error = False
shake_offset = (0, 0)
survey_shake_offset = (0, 0)
no_click_count = 0

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

class Button:
    def __init__(self, rect, text, onclick=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.onclick = onclick
        self.hover = False

    def draw(self, surf, offset=(0, 0)):
        color = ACCENT if self.hover else (100, 100, 100)
        pygame.draw.rect(surf, color, (self.rect.x + offset[0], self.rect.y + offset[1], self.rect.width, self.rect.height), border_radius=6)
        txt = font.render(self.text, True, (0, 0, 0))
        r = txt.get_rect(center=(self.rect.centerx + offset[0], self.rect.centery + offset[1]))
        surf.blit(txt, r)

    def handle(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.onclick:
                self.onclick()

class InputBox:
    def __init__(self, rect, text=''):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return 'enter'
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < 32:
                    self.text += event.unicode
        return None

    def draw(self, surf, offset=(0, 0)):
        pygame.draw.rect(surf, (30, 30, 30), (self.rect.x + offset[0], self.rect.y + offset[1], self.rect.width, self.rect.height), border_radius=6)
        txt = font.render(self.text, True, TEXT_COLOR)
        surf.blit(txt, (self.rect.x + 10 + offset[0], self.rect.y + 10 + offset[1]))
        pygame.draw.rect(surf, (180, 180, 180), (self.rect.x + offset[0], self.rect.y + offset[1], self.rect.width, self.rect.height), 2, border_radius=6)

name_box = InputBox((WIDTH // 2 - 300, HEIGHT //2 - 40, 600, 60))
pass_box = InputBox((WIDTH // 2 - 300, HEIGHT //2 - 40, 600, 60))
pet_box = InputBox((WIDTH // 2 - 300, HEIGHT //2 - 40, 600, 60))

def press_yes():
    global current_q, responses, survey_shake_offset, state, final_message, final_timer
    responses.append(True)
    current_q += 1
    survey_shake_offset = (random.randint(-12, 12), random.randint(-12, 12))
    if current_q >= len(QUESTIONS):
        state = FINAL
        final_message = f"Acordando...\nVocê respondeu todas as perguntas."
        final_timer = pygame.time.get_ticks()

def press_no():
    global current_q, responses, survey_shake_offset, no_click_count, no_button, state, final_message, final_timer
    if current_q == 0:
        no_click_count += 1
        survey_shake_offset = (random.randint(-12, 12), random.randint(-12, 12))
        if no_click_count >= 2:
            no_button = None
        return
    responses.append(False)
    current_q += 1
    survey_shake_offset = (random.randint(-12, 12), random.randint(-12, 12))
    if current_q >= len(QUESTIONS):
        state = FINAL
        final_message = f"Acordando...\nVocê respondeu todas as perguntas."
        final_timer = pygame.time.get_ticks()

yes_button = Button((WIDTH // 2 - 200, HEIGHT // 2 + 160, 180, 70), 'SIM', onclick=press_yes)
no_button  = Button((WIDTH // 2 + 20, HEIGHT // 2 + 160, 180, 70), 'NÃO', onclick=press_no)

def draw_centered_text(lines, y_start=200, line_height=50, offset=(0, 0)):
    y = y_start + offset[1]
    for line, f in lines:
        txt = f.render(line, True, TEXT_COLOR)
        r = txt.get_rect(center=(WIDTH // 2 + offset[0], y))
        screen.blit(txt, r)
        y += line_height

final_message = ''
final_timer = 0

def main():
    global running, state, player_name, pass_errors, pet_name, show_pass_error, shake_offset, survey_shake_offset, no_button, final_timer

    running = True
    while running:
        dt = clock.tick(FPS)
        shake_offset = (0, 0)
        survey_shake_offset = (0, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if state == ENTER_NAME:
                res = name_box.handle_event(event)
                if res == 'enter':
                    player_name = name_box.text.strip() or 'Jogador'
                    state = ENTER_PASS
            elif state == ENTER_PASS:
                res = pass_box.handle_event(event)
                if res == 'enter':
                    if pass_box.text.strip():
                        shake_offset = (random.randint(-10, 10), random.randint(-10, 10))
                        show_pass_error = True
                    pass_box.text = ''
                    pass_errors += 1
                    if pass_errors >= 3:
                        state = ENTER_PET
            elif state == ENTER_PET:
                res = pet_box.handle_event(event)
                if res == 'enter':
                    pet_name = pet_box.text.strip() or 'seu pet'
                    state = SURVEY
            elif state == SURVEY:
                yes_button.handle(event)
                if no_button:
                    no_button.handle(event)
            elif state == FINAL:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    running = False

        screen.fill(BG_COLOR)

        if state == ENTER_NAME:
            draw_centered_text([
                ("Novo Usuário: Digite seu nome", large_font),
                ("(pressione Enter quando terminar)", small_font)
            ])
            name_box.draw(screen)

        elif state == ENTER_PASS:
            draw_centered_text([("Digite sua senha:", large_font)], offset=shake_offset)
            pass_box.draw(screen, offset=shake_offset)
            if show_pass_error:
                error_txt = small_font.render("Senha incorreta", True, ACCENT)
                screen.blit(error_txt, (WIDTH // 2 - error_txt.get_width() // 2, pass_box.rect.y + pass_box.rect.height + 10 + shake_offset[1]))

        elif state == ENTER_PET:
            draw_centered_text([
                ("Confirme que é você.", large_font),
                ("Pergunta de segurança: Qual é o nome do seu animal de estimação?", font)
            ])
            pet_box.draw(screen)

        elif state == SURVEY:
            question = QUESTIONS[current_q]
            draw_centered_text([
                ("Pesquisa em andamento", small_font),
                (question, large_font)
            ], offset=survey_shake_offset)
            instr = small
