import os
import random
import pygame
import time
import shelve
from threading import Timer

pygame.init()

run = True
is_writing = False
capitals_allowed = False
auto_enter = False
backspace_allowed = True
written = ''
to_write = ''
total_letters = 0
time_left = 60
words = 1
correct = 0
wrong = 0 
previous_word_x = 50
previous_word_y = 400
font = pygame.font.Font('freesansbold.ttf', 20) # Font for wanted word and typed word
font2 = pygame.font.Font('freesansbold.ttf', 80) # Font for countdown
font3 = pygame.font.Font('freesansbold.ttf', 17) # Font for previous words
font4 = pygame.font.Font('freesansbold.ttf', 40) # Font for countdown timer

win = pygame.display.set_mode((1040, 600))
pygame.display.set_caption('Ten Fingers - Fast Typing')
pygame.draw.rect(win, (100,100,100), (0,0,800,800))
pygame.draw.rect(win, (0,0,0), (145,220,510,60))
pygame.draw.rect(win, (0,0,0), (195,120,410,60))
textBox = pygame.draw.rect(win, (255,255,255), (200,125,400,50))
input_box = pygame.draw.rect(win, (255,255,255), (150,225,500,50))
# Setting up the start button
start_button = pygame.draw.rect(win, (30,30,30), (180,325,200,50))
button_text = font.render('Start', True, (255, 255, 255))
win.blit(button_text, (255, 340))
# Setting up the button that controls number of words
number_button = pygame.draw.rect(win, (30,30,30), (410,325,200,50))
number_button_text = font.render(str(words) + ' Word', True, (255, 255, 255))
win.blit(number_button_text, (473, 340))
# Setting up the labels for correct and wrong scores
correct_text = font.render('Correct : ', True, (255, 255, 255))
win.blit(correct_text, (20, 20))
wrong_text = font.render('Wrong : ', True, (255, 255, 255))
win.blit(wrong_text, (20, 60))
# Setting up the capital letters button
random_capitals_button = pygame.draw.rect(win, (70,70,70), (820,50,200,50))
random_capitals_text = font3.render('Capital Letters : Off', True, (255, 255, 255))
win.blit(random_capitals_text, (840, 67))
# Setting up the button that controls backspace 
backspace_button = pygame.draw.rect(win, (70,70,70), (820,150,200,50))
backspace_button_text = font3.render('Backspace : Allowed', True, (255, 255, 255))
win.blit(backspace_button_text, (835, 167))
# Setting up the button that auto enter 
auto_enter_button = pygame.draw.rect(win, (70,70,70), (820,250,200,50))
auto_enter_button_text = font3.render('Auto - Enter : Off', True, (255, 255, 255))
win.blit(auto_enter_button_text, (835, 267))


class ToWrite():
    def CreateRandomSentence(self,number):
        self.writing = ''
        self.number = number
        with open ("words.txt", "r") as textFile:
            lines = textFile.readlines()
            x = 1
            while x <= self.number:
                randomLine = random.randint(0,len(lines)-1)
                if self.number > x:
                    if capitals_allowed and random.randint(1,10) < 7:
                        self.writing += str(lines[randomLine]).strip().capitalize()+' '   
                    else:
                        self.writing += str(lines[randomLine]).strip()+' '
                else:
                    if capitals_allowed and random.randint(1,10) < 7:
                        self.writing += str(lines[randomLine]).strip().capitalize()
                    else:
                        self.writing += str(lines[randomLine]).strip()  
                x += 1
        return self.writing
 

def ChangeTheGivenText():
    global to_write, words
    textBox = pygame.draw.rect(win, (255,255,255), (200,125,400,50))
    to_write = ToWrite().CreateRandomSentence(words)
    to_write_Text = font.render(to_write, True, (0, 0, 0))
    win.blit(to_write_Text, (210, 140))
    pygame.display.update()

def RefreshInputBox(text,color):
    input_box = pygame.draw.rect(win, (255,255,255), (150,225,500,50))
    writtenText = font.render(text, True, color)
    win.blit(writtenText, (160, 240))
    pygame.display.update()

def DisplayPreviousWords(text):
    global previous_word_x, previous_word_y
    if previous_word_x == 650: # If it is the last row, the grey backround fill will be smaller due to the black screen on right
        pygame.draw.rect(win, (100,100,100), (previous_word_x,previous_word_y,150,20))
        pygame.draw.rect(win, (0,0,0), (800,previous_word_y,300,20))
    else:
        pygame.draw.rect(win, (100,100,100), (previous_word_x,previous_word_y,200,20))
    if text == to_write:
        writtenText = font3.render(text, True, (0, 209, 69))
    else:
        writtenText = font3.render(text, True, (220, 0, 0))
    win.blit(writtenText, (previous_word_x, previous_word_y))
    previous_word_y += 50
    if previous_word_x == 650 and previous_word_y == 600: # If all lines have been used
        previous_word_x = 50
        previous_word_y = 400
    if previous_word_y == 600:
        previous_word_y = 400
        previous_word_x += 200

def PressedEnterKey():
    global written, correct, wrong, total_letters
    DisplayPreviousWords(written)
    if written == to_write: 
        correct += words
        total_letters += len(written)
    else:
        wrong += 1
    DisplayScore()
    written = ''
    RefreshInputBox(written,(0, 0, 0))
    ChangeTheGivenText()

def DisplayLettersWordsPerSecond():
    if time_left != 60:
        letters_per_second = total_letters/(60-time_left)
    else:
        letters_per_second = 0
    pygame.draw.rect(win, (0,0,0), (800,350,240,500))
    win.blit(font4.render(str(letters_per_second)[:4], True, (255,255,255)), (885, 380))
    win.blit(font.render('Letters Per Second', True, (255,255,255)), (830, 440))

def DisplayHighScore():
    pygame.draw.rect(win,(0,0,0),(845,500,200,25)) # Clears the previous high score text (useful when user gets a new high score)
    try:    
        win.blit(font3.render(f'High Score : {str(GetHighScore())[:4]}', True, (255,255,255)), (845, 500))
    except:
        pass
def DisplayScore():
    pygame.draw.rect(win, (100,100,100), (115,20,150,20))
    pygame.draw.rect(win, (100,100,100), (115,60,150,20))
    correctScoreText = font.render(f'{str(correct)} ({str(total_letters)})', True, (255,255,255))
    wrongScoreText = font.render(str(wrong), True, (255,255,255))
    win.blit(correctScoreText, (115, 20))
    win.blit(wrongScoreText, (115, 60))
DisplayScore()

def GetHighScore():
    d = shelve.open('score.txt')
    high_score = d['HighScore'] 
    d.close()
    return high_score

def SaveHighScore(score):
    d = shelve.open('score.txt')     
    d['HighScore'] = score/60
    print(d['HighScore'])           
    d.close()

def DisplayStartingCountDown():
    i = 3
    while i > 0:
        countdownText = font2.render(str(i), True, (255,255,255))
        pygame.draw.rect(win, (100,100,100), (370,450,80,80)) #Clears the previous displayed number 
        win.blit(countdownText, (370, 450))
        pygame.display.update()
        pygame.time.delay(750)
        i -= 1
    pygame.draw.rect(win, (100,100,100), (350,450,80,80)) #Clears the last displayed number 

def StartGame():
    global total_letters,time_left,is_writing
    pygame.draw.rect(win, (0,0,0), (800,350,300,600))
    total_letters = 0
    DisplayScore()
    time_left = 60
    pygame.draw.rect(win, (100,100,100), (50,400,750,200))
    DisplayStartingCountDown()
    start_button = pygame.draw.rect(win, (30,30,30), (180,325,200,50))
    button_text = font.render('End', True, (255, 255, 255))
    win.blit(button_text, (255, 340))
    is_writing = True
    ChangeTheGivenText()
    DisplayTimer()

def EndGame():
    global is_writing,wrong,correct,written,previous_word_x,previous_word_y,total_letters
    start_button = pygame.draw.rect(win, (30,30,30), (180,325,200,50))
    button_text = font.render('Start', True, (255, 255, 255))
    win.blit(button_text, (255, 340))
    is_writing = False
    wrong = 0
    correct = 0
    pygame.draw.rect(win, (255,255,255), (200,125,400,50))
    previous_word_x = 50
    previous_word_y = 400
    written = ''
    try:
        if GetHighScore() < total_letters/60:
            SaveHighScore(total_letters)
    except:
        SaveHighScore(total_letters)
    DisplayHighScore()
def DisplayTimer():
    global time_left, is_writing
    pygame.draw.rect(win, (100,100,100), (380,40,60,50))
    timer_text = font4.render(str(time_left), True, (255, 255, 255))
    win.blit(timer_text, (380, 40))
    time_left -= 1
    t = Timer(1,DisplayTimer)
    if time_left == -1:
        t.cancel()
        EndGame()
    if is_writing:
        t.start()
    else:
        t.cancel()
    
while run:
    pygame.time.delay(100)
    if is_writing:
        DisplayLettersWordsPerSecond()
        DisplayHighScore()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
                if is_writing:
                    if event.key == pygame.K_RETURN:
                        if written != '':
                            PressedEnterKey()
                    elif event.key == pygame.K_BACKSPACE:
                        if backspace_allowed:
                            written = written[:-1]
                    else:
                        written += event.unicode
                        if auto_enter:
                            if written == to_write:
                                PressedEnterKey()
        if written == to_write[0:len(written)]:
            RefreshInputBox(written,(0, 209, 69))
        else:
            RefreshInputBox(written,(220, 0, 0))

        if event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            if start_button.collidepoint(position):
                if not is_writing:
                    StartGame()
                else:
                    EndGame()
            if number_button.collidepoint(position):
                words += 1
                if words == 4:
                    words = 1
                number_button = pygame.draw.rect(win, (30,30,30), (410,325,200,50))
                number_button_text = font.render(str(words) + ' Word', True, (255, 255, 255))
                win.blit(number_button_text, (473, 340))
            if random_capitals_button.collidepoint(position):
                capitals_allowed = not capitals_allowed
                random_capitals_button = pygame.draw.rect(win, (70,70,70), (820,50,200,50))
                if capitals_allowed:
                    random_capitals_text = font3.render('Capital Letters : On', True, (255, 255, 255))
                else:
                    random_capitals_text = font3.render('Capital Letters : Off', True, (255, 255, 255))
                win.blit(random_capitals_text, (840, 67))
            if backspace_button.collidepoint(position):
                backspace_allowed = not backspace_allowed
                backspace_button = pygame.draw.rect(win, (70,70,70), (820,150,200,50))
                if backspace_allowed:
                    backspace_button_text = font3.render('Backspace : Allowed', True, (255, 255, 255))
                else:
                    backspace_button_text = font3.render('Backspace : Disabled', True, (255, 255, 255))
                win.blit(backspace_button_text, (835, 167))
            if auto_enter_button.collidepoint(position):
                auto_enter = not auto_enter
                auto_enter_button = pygame.draw.rect(win, (70,70,70), (820,250,200,50))
                if auto_enter:
                    win.blit(font3.render('Auto - Enter : On', True, (255, 255, 255)), (835, 267))
                else:
                    win.blit(font3.render('Auto - Enter : Off', True, (255, 255, 255)), (835, 267))

pygame.quit()