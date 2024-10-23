import pygame
import sys

# EXACTLY ONE OCCURRENCE OF "BBA"
pygame.init()
WIDTH, HEIGHT = 1200, 600  
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Exactly One Occurrence of BBA Visualization")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

#asa ibutang nag circles x,y
circle_placement = {
    0: (100, 500),
    1: (250, 500),
    2: (400, 500),
    3: (550, 500),
    4: (700, 500),
    5: (850, 500),
    6: (1000, 500),
}

transition_table = [
    [0, 1], 
    [0, 2], 
    [3, 2],  
    [3, 4],  
    [3, 5],
    [6, 5],  
    [6, 6],  #Dead state
]

final_states = [3, 4, 5]  #Accepting states i color green
dead_state = 6

font = pygame.font.SysFont(None, 36)

def draw_line(start_pos, end_pos, color=BLACK):
    pygame.draw.line(screen, color, start_pos, end_pos, 2)  #line connectors

#pwede raman jud ni wala hahaha
def draw_transition_table():
    header = font.render("Transition Table", True, BLACK)
    screen.blit(header, (50, 110))

    startX = 350
    startY = 110
    width = 120
    height = 40
    pygame.draw.rect(screen, BLACK, (startX, startY, width * 3, height * 8), 2)

    screen.blit(font.render("STATE", True, BLACK), (startX + 10, startY + 5))
    screen.blit(font.render("0 (a)", True, BLACK), (startX + width + 10, startY + 5))
    screen.blit(font.render("1 (b)", True, BLACK), (startX + width * 2 + 10, startY + 5))

    #kuti ra kaayo 
    for i, row in enumerate(transition_table):
        y = startY + height * (i + 1)
        screen.blit(font.render(str(i), True, BLACK), (startX + 10, y + 5))
        screen.blit(font.render(str(row[0]), True, BLACK), (startX + width + 10, y + 5))
        screen.blit(font.render(str(row[1]), True, BLACK), (startX + width * 2 + 10, y + 5))
        pygame.draw.line(screen, BLACK, (startX + width, y), (startX + width, y + height))  # Vertical lines
        pygame.draw.line(screen, BLACK, (startX + width * 2, y), (startX + width * 2, y + height))

    pygame.draw.line(screen, BLACK, (startX, startY + height), (startX + width * 3, startY + height))

def draw_dfa(curr):
    for i, row in enumerate(transition_table):
        for input_symbol in range(2):
            next = row[input_symbol]
            if next != i:
                draw_line(circle_placement[i], circle_placement[next])

    #circle for each state
    for state, pos in circle_placement.items():
        color = GREEN if state in final_states else RED if state == dead_state else BLUE
        pygame.draw.circle(screen, color, pos, 40)
        pygame.draw.circle(screen, BLACK, pos, 40, 2)  # Circle border
        text = font.render(f"q{state}", True, BLACK)
        screen.blit(text, (pos[0] - 20, pos[1] - 20))

    #highlight purposes
    pygame.draw.circle(screen, (255, 255, 0), circle_placement[curr], 40, 5)

def validate_string(input_string):
    state = 0  
    state_sequence = []  #para sa na visit
    for symbol in input_string:
        #same rajud but in python lang haha
        state_sequence.append(state)
        input_index = 0 if symbol == 'a' or symbol == 'A' else 1 if symbol == 'b' or symbol == 'B' else None

        if input_index is None: 
            return "Rejected", state_sequence

        state = transition_table[state][input_index]
        draw_dfa(state)  
        pygame.display.update()
        pygame.time.delay(1000)

    state_sequence.append(state)
    result = "String is Accepted" if state in final_states else "String is Rejected"
    
    return result, state_sequence

def main():
    input_string = ""
    running = True
    result_text = ""
    state_sequence = ""
    while running:
        screen.fill(WHITE)
        draw_dfa(0)  #qo initial state
        draw_transition_table()

        name_display = font.render(f"Paul Thomas M. Abellana", True, BLACK)
        screen.blit(name_display, (50, 20))

        input_text = font.render(f"Input: {input_string}", True, BLACK)
        screen.blit(input_text, (50, 40))

        state_display = font.render(f"State Sequence: {state_sequence}", True, BLACK)
        screen.blit(state_display, (50, 80))

        result_display = font.render(f"Result of String: {result_text}", True, BLACK)
        screen.blit(result_display, (700, 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_string = input_string[:-1]
                elif event.key == pygame.K_RETURN:
                    result_text, state_sequence = validate_string(input_string)  # Validate and get result
                    input_string = ""
                else:
                    input_string += event.unicode

    pygame.quit()

if __name__ == "__main__":
    main()
