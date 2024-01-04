import tkinter
import random


def move_wrap(obj, move):
    canvas.move(obj, move[0], move[1])
    if canvas.coords(obj)[0] <= 0:
        canvas.move(obj, step * N_X, 0)
    if canvas.coords(obj)[0] >= step * N_X:
        canvas.move(obj, -step * N_X, 0)
    if canvas.coords(obj)[1] <= 0:
        canvas.move(obj, 0, step * N_Y)
    if canvas.coords(obj)[1] >= step * N_Y:
        canvas.move(obj, 0, -step * N_Y)


def do_nothing(x):
    pass


def check_move():
    if canvas.coords(player) == canvas.coords(exit):
        label.config(text="Победа!")
        master.bind("<KeyPress>", do_nothing)


def key_pressed(event):
    global flag, cnt
    if event.keysym == 'Up':
        move_wrap(player, (0, -step))
        if not flag:
            for enemy in enemies:
                direction = enemy[1](enemy[0])  # вызвать функцию перемещения у "врага"
                move_wrap(enemy[0], direction)  # произвести  перемещение
    if event.keysym == 'Down':
        move_wrap(player, (0, step))
        if not flag:
            for enemy in enemies:
                direction = enemy[1](enemy[0])  # вызвать функцию перемещения у "врага"
                move_wrap(enemy[0], direction)  # произвести  перемещение
    if event.keysym == 'Right':
        move_wrap(player, (step, 0))
        if not flag:
            for enemy in enemies:
                direction = enemy[1](enemy[0])  # вызвать функцию перемещения у "врага"
                move_wrap(enemy[0], direction)  # произвести  перемещение
    if event.keysym == 'Left':
        move_wrap(player, (-step, 0))
        if not flag:
            for enemy in enemies:
                direction = enemy[1](enemy[0])  # вызвать функцию перемещения у "врага"
                move_wrap(enemy[0], direction)  # произвести  перемещение
    check_move()
    if flag:
        if cnt > 1:
            cnt -= 1
            label1.config(text=f'У вас осталось {cnt} ходов, пока враги остановлены')
        else:
            label1.config(text=f'Больше вы не можете останавливать врагов')
            flag = False
    if event.char == 'w' and not flag:
        flag = True
        cnt = 3
        label1.config(text=f'У вас осталось {cnt} хода, пока враги остановлены')


def always_right(obj):
    return step, 0


def always_left(obj):
    return -step, 0


def always_up(obj):
    return 0, -step


def always_down(obj):
    return 0, step


def random_move(obj):
    return random.choice([(step, 0), (-step, 0), (0, step), (0, -step)])


def closer_to_player(obj):
    if abs(canvas.coords(obj)[0] - canvas.coords(player)[0]) > abs(canvas.coords(obj)[1] - canvas.coords(player)[1]):
        if canvas.coords(obj)[0] > canvas.coords(player)[0]:
            return -10, 0
        else:
            return 10, 0
    else:
        if canvas.coords(obj)[1] > canvas.coords(player)[1]:
            return 0, -10
        else:
            return 0, 10


def prepare_and_start():
    flag = False
    cnt = 3
    label1.config(text=f"Один раз за игру вы можете нажать клавишу 'W' и на {cnt} хода остановить врагов")
    global player, exit, fires, enemies, fires_coordinates, enemies_coordinates
    canvas.delete("all")
    N_FIRES = 6  # Число клеток, заполненных огнем
    fires = []
    fires_coordinates = []
    for i in range(N_FIRES):
        fire_pos = (random.randint(0, N_X - 1) * step,
                    random.randint(0, N_Y - 1) * step)
        fires_coordinates.append(fire_pos)
        fire = canvas.create_image(
            (fire_pos[0], fire_pos[1]),
            image=fire_pic, anchor='nw')
        fires.append(fire)
    N_ENEMIES = 4  # число врагов
    enemies = []
    enemies_coordinates = []
    for i in range(N_ENEMIES):
        enemy_pos = (random.randint(0, N_X - 1) * step,
                     random.randint(0, N_Y - 1) * step)
        while enemy_pos in fires_coordinates:
            enemy_pos = (random.randint(0, N_X - 1) * step,
                         random.randint(0, N_Y - 1) * step)
        enemies_coordinates.append(enemy_pos)
        enemy = canvas.create_image(
            (enemy_pos[0], enemy_pos[1]),
            image=enemy_pic, anchor='nw')
        enemies.append([enemy, random.choice([closer_to_player, always_right, always_left,
                                              always_up, always_down, random_move])])
    player_pos = (random.randint(0, N_X - 1) * step,
                  random.randint(0, N_Y - 1) * step)
    while player_pos in fires_coordinates or player_pos in enemies_coordinates:
        player_pos = (random.randint(0, N_X - 1) * step,
                      random.randint(0, N_Y - 1) * step)
    player = canvas.create_image(
        (player_pos[0], player_pos[1]),
        image=player_pic, anchor='nw')

    exit_pos = (random.randint(0, N_X - 1) * step,
                random.randint(0, N_Y - 1) * step)
    while exit_pos in fires_coordinates or exit_pos in enemies_coordinates or exit_pos == player_pos:
        exit_pos = (random.randint(0, N_X - 1) * step,
                    random.randint(0, N_Y - 1) * step)
    exit = canvas.create_image(
        (exit_pos[0], exit_pos[1]),
        image=exit_pic, anchor='nw')

    label.config(text="Найди выход!")
    master.bind("<KeyPress>", key_pressed)


def check_move():
    if canvas.coords(player) == canvas.coords(exit):
        label.config(text="Победа!")
        master.bind("<KeyPress>", do_nothing)
    for f in fires:
        if canvas.coords(player) == canvas.coords(f):
            label.config(text="Ты проиграл!")
            master.bind("<KeyPress>", do_nothing)
    for e in enemies:
        if canvas.coords(player) == canvas.coords(e[0]):
            label.config(text="Ты проиграл!")
            master.bind("<KeyPress>", do_nothing)


step = 60  # Размер клетки
N_X = 10
N_Y = 10  # Размер сетки
master = tkinter.Tk()
label = tkinter.Label(master, text="Найди выход")
label.pack()
label1 = tkinter.Label(master, text="Один раз за игру вы можете нажать клавишу 'W' и на 2 хода остановить врагов")
label1.pack()
flag = False
cnt = 3
canvas = tkinter.Canvas(master, bg='green',
                        width=step * N_X, height=step * N_Y)
canvas.pack()

player_pic = tkinter.PhotoImage(file="images/player.gif")
exit_pic = tkinter.PhotoImage(file="images/princess.gif")
fire_pic = tkinter.PhotoImage(file="images/fire.gif")
enemy_pic = tkinter.PhotoImage(file="images/villain.gif")

restart = tkinter.Button(master, text="Начать заново",
                         command=prepare_and_start)
restart.pack()
prepare_and_start()
master.mainloop()
