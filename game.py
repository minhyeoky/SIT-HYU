import sys, pygame
from pygame.locals import *
from datetime import datetime
from time import sleep

pygame.init()
pygame.font.init()  # you have to call this at the start,

# if you want to use this module.
myfont = pygame.font.SysFont('Comic Sans MS', 60)

size = width, height = 640, 480
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
speed = [0, 5]  # horizontally, vertically
STOP = [0, 0]

NOTE_WIDTH = 70
NOTE_HEIGHT = 70
NOTE_CENTERS = [(55, 30), (125, 30), (195, 30), (265, 30),
                (375, 30), (445, 30), (515, 30), (585, 30)]
HIT_LINE = 380
DEAD_LINE = 480
DIV = 2.0
NUM_NOTES = 8

ARROWS = [pygame.image.load('./statics/{}.png'.format(i)) for i in range(4)]

NOTE_SOUND = './statics/note.wav'
hit_sound = pygame.mixer.Sound(NOTE_SOUND)
background = pygame.image.load('./statics/bg.jpg')
ARROWS_BAR = [pygame.transform.scale(pygame.image.load('./statics/{}_bar.png'.format(i)), (70, 70)) for i in range(4)]
PERFERCT = pygame.transform.scale(pygame.image.load('./statics/perfect.png'), (120, 120))
MISSED = pygame.transform.scale(pygame.image.load('./statics/miss.png'), (120, 120))
SELECTSPEED = pygame.transform.scale(pygame.image.load('./statics/select_speed.png'), (400, 400))
SELECTSONG = pygame.transform.scale(pygame.image.load('./statics/select_song.png'), (400, 400))

COUNTERS = [0, 0, 0, 0]  # perfect, miss, perfect, miss
COUNTERS_COUNT = 50

SONG_twinkletwinklelittlestar = [
    [0, 1, 14, 31, 32, 45],  # DO
    [12, 13, 22, 29, 43, 44],  # RE
    [10, 11, 20, 21, 27, 28, 41, 42, ],  # MI
    [8, 9, 18, 19, 25, 26, 39, 40],  # PA
    [2, 3, 6, 16, 17, 23, 24, 33, 34, 37],  # SOL
    [4, 5, 35, 36],  # LA
    [],  # SI
    [],  # DO
]

SONG_forElise = [
    [8, 10, 17, 25, 27, 32, 36, 46, 49, 58, 60],  # DO, C
    [2, 4, 7, 19, 21, 24, 37, 42, 45, 48, 52, 54, 57],  # RE, D
    [1, 3, 5, 11, 14, 18, 20, 22, 28, 31, 38, 41, 43, 44, 47, 50, 51, 53, 55, 56],  # MI, E
    [40],  # PA, F
    [39],  # SOL, G
    [9, 12, 15, 26, 29, 34, 59],  # LA, A
    [6, 13, 16, 23, 30, 33, 35],  # SI, B
    [],  # DO, C
]


def div(SONG):
    for i in range(len(SONG)):
        for j in range(len(SONG[i])):
            SONG[i][j] += 1
            SONG[i][j] /= DIV
    return SONG


SONGS = [div(SONG_twinkletwinklelittlestar), div(SONG_forElise)]
SONGS_NAME = ["TwinkleLittleStar", "ForElise"]

NOTES = None

POINT_1 = 0
POINT_2 = 0

ACTIVE_NOTES = [[] for _ in range(NUM_NOTES)]

RANKING = [
    ['AAA', 'def', 20],
    ['AAA', 'def', 19],
    ['AAA', 'def', 18],
    ['AAA', 'def', 17],
    ['AAA', 'def', 16],
    ['AAA', 'def', 15],
    ['AAA', 'def', 14],
    ['AAA', 'def', 13],
    ['AAA', 'def', 12],
    ['AAA', 'def', 11]
]

screen = pygame.display.set_mode(size)


def Note(center, idx):
    note = pygame.transform.scale(ARROWS[idx % 4], (NOTE_WIDTH, NOTE_HEIGHT))
    note_rect = note.get_rect()
    note_rect.center = center
    return note, note_rect


def reset_timer():
    sec_start = datetime.now().second
    min_start = datetime.now().minute
    return sec_start, min_start


def generate_note(N, start_from, center, idx, fps):
    LEN_NOTES = range(len(N))
    for i in LEN_NOTES:
        t = (fps / 50.0 + fps * (1 / 50))
        if t <= N[i] < t + 0.05:
            note, note_rect = Note(center, idx)
            ACTIVE_NOTES[idx].append([note, note_rect])
            print("GENERATED {}".format(idx))


def remove_dead_notes(active_notes):
    alive_notes = []

    for i in range(len(active_notes)):
        temp = []
        for j in range(len(active_notes[i])):
            if active_notes[i][j] is not None:

                if active_notes[i][j][1].y > DEAD_LINE:
                    if i >= 4:
                        COUNTERS[3] = COUNTERS_COUNT
                    elif i < 4:
                        COUNTERS[1] = COUNTERS_COUNT
                else:
                    temp.append(active_notes[i][j])
        alive_notes.append(temp)

    return alive_notes


def check_songLength(idx):
    length = 0
    num_note = 0
    for each in SONGS[idx]:
        for i in each:
            if length < i:
                length = i
            num_note += 1
    song_length = int(length) + 1
    print("LENGTH OF SONG: ", song_length)
    print("NUMBER OF NOTES: ", num_note)
    return song_length, num_note


def get_key():
    key_table = ['1', '1', '1', '1', '1', '1', '1', '1']
    with open('pressed', mode='r') as f:
        data = f.read().split(',')
    with open('pressed', mode='w') as f:
        f.write(','.join(key_table))
    if data == ['']:
        return key_table
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == KEYDOWN:
            if event.key == ord('a'):
                data[0] = '0'
            if event.key == ord('s'):
                data[1] = '0'
            if event.key == ord('d'):
                data[2] = '0'
            if event.key == ord('f'):
                data[3] = '0'
            if event.key == ord('h'):
                data[4] = '0'
            if event.key == ord('j'):
                data[5] = '0'
            if event.key == ord('k'):
                data[6] = '0'
            if event.key == ord('l'):
                data[7] = '0'
    return data


def press_key(idx, point, active_notes):
    for i in range(len(active_notes[idx])):

        if active_notes[idx][i] is None:
            continue
        rect = active_notes[idx][i][1]
        if rect.y > 500:
            active_notes[idx][i] = None
            if idx >= 4:
                COUNTERS[3] = COUNTERS_COUNT
            else:
                COUNTERS[1] = COUNTERS_COUNT
        elif rect.y > HIT_LINE:
            point += 1
            if idx >= 4:
                COUNTERS[2] = COUNTERS_COUNT
            else:
                COUNTERS[0] = COUNTERS_COUNT
            pygame.mixer.Sound.play(hit_sound)
            active_notes[idx][i] = None

    return point, active_notes


def is_pressed(key_table, idx):
    if key_table[idx] == '0':
        return True
    return False


# NEW GAME STATES
gameState = 0
song_num = 0
song_name_flow = 0
song_length = 0
num_note = 0
first_player_name = [65, 65, 65]
second_player_name = [65, 65, 65]
pick_1 = 0
pick_2 = 0
picked_1 = False
picked_2 = False
start_from_ = None
milli_start_from = 0

while True:
    GLOBAL_TIME = datetime.now()

    if gameState == 0:
        # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # SELECT SPEED# # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # #

        screen.fill(BLACK)
        screen.blit(SELECTSPEED, (120, -20))
        key = get_key()
        if is_pressed(key, 3):
            speed[1] += 1
        if is_pressed(key, 1):
            speed[1] -= 1
            if speed[1] < 1:
                speed[1] = 1
        if is_pressed(key, 0):
            gameState += 1
        sfont = pygame.font.SysFont('Comic Sans MS', 300)
        speed3 = sfont.render(str(speed[1]), False, (255, 255, 255))
        screen.blit(speed3, (250, 260))
    if gameState == 1:
        # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # #SELECT SONG# # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # #

        screen.fill(BLACK)
        screen.blit(SELECTSONG, (120, -20))
        key = get_key()

        if is_pressed(key, 3):
            song_num += 1
            if song_num >= len(SONGS_NAME):
                song_num = 0
            song_name_flow = 0
        if is_pressed(key, 1):
            song_name_flow = 0
            song_num -= 1
            if song_num < 0:
                song_num = len(SONGS_NAME) - 1
        if is_pressed(key, 0):
            temp = []
            for i in range(len(SONGS[song_num])):
                temp2 = []
                for j in range(len(SONGS[song_num][i])):
                    temp2.append(SONGS[song_num][i][j])
                temp.append(temp2)

            NOTES = temp
            song_length, num_note = check_songLength(song_num)
            gameState = 2
            sec_start, min_start = reset_timer()

        sfont = pygame.font.SysFont('Comic Sans MS', 100)
        song_name = sfont.render(str(SONGS_NAME[song_num]), False, (255, 255, 255))
        song_name_flow += 1
        if song_name_flow > 900:
            song_name_flow = 0
        screen.blit(song_name, (song_name_flow, 260))
        pygame.display.flip()

    if gameState == 2:
        # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # START GAME# # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # #

        sec_now = datetime.now().second
        min_now = datetime.now().minute

        start_from = sec_now - sec_start + (min_now - min_start) * 60
        milli_start_from += 1
        for i in range(NUM_NOTES):
            generate_note(NOTES[i], start_from, NOTE_CENTERS[i], i, milli_start_from)

        screen.blit(background, (0, 0))
        for i in range(len(ACTIVE_NOTES)):
            for j in range(len(ACTIVE_NOTES[i])):
                if ACTIVE_NOTES[i][j] is None:
                    continue
                ACTIVE_NOTES[i][j][1] = ACTIVE_NOTES[i][j][1].move(speed)
                screen.blit(ACTIVE_NOTES[i][j][0], ACTIVE_NOTES[i][j][1])

        ## ScoreBoard
        pygame.draw.rect(screen, (255, 255, 255), [270, 150, 100, 50], 3)  # left, top, width, height

        ## PLAYER 1
        [(pygame.draw.rect(screen, WHITE, [20 + 70 * i, 410, 70, 70], 3),
          screen.blit(ARROWS_BAR[i], (20 + i * 70, 410))) for i in range(4)]

        ## PLAYER 2
        [(pygame.draw.rect(screen, WHITE, [340 + 70 * i, 410, 70, 70], 3),
          screen.blit(ARROWS_BAR[i], (340 + i * 70, 410))) for i in range(4)]

        key = get_key()
        for i in range(NUM_NOTES):
            try:
                if key[i] == '0' and i < 4:
                    POINT_1, ACTIVE_NOTES = press_key(i, POINT_1, ACTIVE_NOTES)
                if key[i] == '0' and i >= 4:
                    POINT_2, ACTIVE_NOTES = press_key(i, POINT_2, ACTIVE_NOTES)
            except:
                pass

        ACTIVE_NOTES = remove_dead_notes(ACTIVE_NOTES)

        point_text_1 = myfont.render(str(POINT_1), True, (255, 255, 255))
        point_text_2 = myfont.render(str(POINT_2), True, (255, 255, 255))
        screen.blit(point_text_1, (280, 160))
        screen.blit(point_text_2, (340, 160))

        if song_length  < start_from:
            sfont = pygame.font.SysFont('Comic Sans MS', 100)
            sfont2 = pygame.font.SysFont('Comic Sans MS', 50)
            end_game = sfont.render('WELL PLAYED!', False, (255, 255, 255))
            score_1 = sfont2.render('POINT is {}/{}'.format(POINT_1, num_note), False, (255, 255, 255))
            score_2 = sfont2.render('POINT is {}/{}'.format(POINT_2, num_note), False, (255, 255, 255))
            screen.blit(end_game, (70, 200))
            screen.blit(score_1, (50, 300))
            screen.blit(score_2, (360, 300))
            sleep(2)
            gameState = 3

    if gameState == 3:

        # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # #SELECT NAME# # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # #

        screen.fill(BLACK)

        highscore = POINT_1 + POINT_2
        key = get_key()

        if key[0] == '0':
            pick_1 += 1
            if pick_1 >= 3:
                picked_1 = True
                pick_1 = 3
        if key[1] == '0' and not picked_1:
            first_player_name[pick_1] += 1
        if key[3] == '0' and not picked_1:
            first_player_name[pick_1] -= 1

        if key[4] == '0':
            pick_2 += 1
            if pick_2 >= 3:
                picked_2 = True
                pick_2 = 3
        if key[5] == '0' and not picked_2:
            second_player_name[pick_2] += 1
        if key[7] == '0' and not picked_2:
            second_player_name[pick_2] -= 1

        if picked_2 and picked_1:
            gameState = 4
            for i in range(10):
                if RANKING[i][2] <= highscore:
                    RANKING[i] = ['{}{}{}'.format(str(chr(first_player_name[0])),
                                                  str(chr(first_player_name[1])),
                                                  str(chr(first_player_name[2]))),
                                  '{}{}{}'.format(str(chr(second_player_name[0])),
                                                  str(chr(second_player_name[1])),
                                                  str(chr(second_player_name[2]))),
                                  highscore]
                    break
        if (GLOBAL_TIME.microsecond / 1000) % 1000 > 500:
            if not picked_1:
                rect_1 = pygame.draw.rect(screen, WHITE, (80 + pick_1 * 30, 400, 30, 40), 3)
            if not picked_2:
                rect_2 = pygame.draw.rect(screen, WHITE, (410 + pick_2 * 30, 400, 30, 40), 3)
        screen.blit(myfont.render('SCORE: {}'.format(highscore), False, WHITE), (200, 220))
        screen.blit(myfont.render(
            '{}{}{}'.format(str(chr(first_player_name[0])), str(chr(first_player_name[1])),
                            str(chr(first_player_name[2]))), False, (255, 255, 255)), (80, 400))
        screen.blit(myfont.render(
            '{}{}{}'.format(str(chr(second_player_name[0])), str(chr(second_player_name[1])),
                            str(chr(second_player_name[2]))), False, (255, 255, 255)), (410, 400))

    if gameState == 4:

        # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # #RANKING BOARD# # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # #
        screen.fill(BLACK)
        screen.blit(myfont.render('Ranking', False, (255, 255, 255)), (265, 40))

        for x in range(10):
            temp = RANKING[x]
            screen.blit(
                myfont.render('{}. {} & {} SCORE {}'.format(x + 1, temp[0], temp[1], temp[2]), False, (255, 255, 255)),
                (50, x * 30 + 80))

        screen.blit(myfont.render('Any button to start game', False, (255, 255, 255)), (50, 400))

    if COUNTERS[0] > COUNTERS[1]:
        screen.blit(PERFERCT, (110, 300))
        COUNTERS[0] -= 1
        COUNTERS[1] = 0
    if COUNTERS[1] > COUNTERS[0]:
        screen.blit(MISSED, (110, 300))
        COUNTERS[1] -= 1
        COUNTERS[0] = 0
    if COUNTERS[2] > COUNTERS[3]:
        screen.blit(PERFERCT, (430, 300))
        COUNTERS[2] -= 1
        COUNTERS[3] = 0
    if COUNTERS[3] > COUNTERS[2]:
        screen.blit(MISSED, (430, 300))
        COUNTERS[3] -= 1
        COUNTERS[2] = 0
    pygame.display.flip()  # Update the full display Surface to the screen
    # pygame.time.delay(1)

    if gameState == 4:

        key = get_key()
        sleep(2)
        a = 0
        for each in key:
            a += int(each)
        if a < 8:
            song_name_flow = 0
            song_num = 0
            song_length = 0
            POINT_1 = 0
            POINT_2 = 0
            gameState = 0
            first_player_name = [65, 65, 65]
            second_player_name = [65, 65, 65]
            pick_1 = 0
            pick_2 = 0
            milli_start_from = 0
            picked_1 = False
            picked_2 = False
