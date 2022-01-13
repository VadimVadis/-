import sqlite3
import pygame
import pygame_gui
from registration import signal_notification


class Shop:
    def __init__(self, id_player):
        pygame.init()
        pygame.display.set_caption('Prince Of Voronezh')
        self.window_surface = pygame.display.set_mode((800, 640))
        self.background = pygame.image.load('images/shop.jpg')
        self.manager = pygame_gui.UIManager((800, 640))
        self.buy_or_no = {'1': 'куплено',
                          '2': 'купить за 5 монет', '3': 'купить за 7 монет'}
        self.id_player = id_player
        self.con = sqlite3.connect('users.db')
        self.cur = self.con.cursor()
        self.buy_person, self.name_use_person, self.coins_user = \
            self.cur.execute(
                f"""SELECT buy_person, use_person, kolvo_money FROM users WHERE id='{self.id_player}'""").fetchone()
        for i in self.buy_person.split(';'):
            self.buy_or_no[i] = 'куплено'
        self.buy_or_no[str(self.name_use_person)] = 'используется'

        self.buy_platformer_num_1 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((50, 170), (150, 50)),
            text=self.buy_or_no['1'],
            manager=self.manager)
        self.buy_platformer_num_2 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((50, 250), (150, 50)),
            text=self.buy_or_no['2'],
            manager=self.manager)
        self.buy_platformer_num_3 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((50, 400), (150, 50)),
            text=self.buy_or_no['3'],
            manager=self.manager)
        self.return_back = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, 550), (150, 50)),
            text='Вернуться назад',
            manager=self.manager)
        self.con = sqlite3.connect('users.db')
        self.cur = self.con.cursor()
        self.clock = pygame.time.Clock()
        self.buy_platformer()

    def buy_platformer(self):
        running = True
        time_delta = self.clock.tick(60) / 1000.0
        while running:
            self.window_surface.blit(self.background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.updating_bd()
                    exit(0)
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.buy_platformer_num_1:
                            self.checking_for_status('1', 0)
                        elif event.ui_element == self.buy_platformer_num_2:
                            self.checking_for_status('2', 5)
                        elif event.ui_element == self.buy_platformer_num_3:
                            self.checking_for_status('3', 7)
                        elif event.ui_element == self.return_back:
                            running = False
                self.manager.process_events(event)
            self.buy_platformer_num_1.set_text(self.buy_or_no['1'])
            self.buy_platformer_num_2.set_text(self.buy_or_no['2'])
            self.buy_platformer_num_3.set_text(self.buy_or_no['3'])
            self.manager.update(time_delta)
            self.manager.draw_ui(self.window_surface)
            pygame.display.update()
        self.updating_bd()

    def checking_for_status(self, name, kolvo_money):
        if self.buy_or_no[name] == 'купить за 5 монет' or self.buy_or_no[name] == 'купить за 7 монет':
            if self.coins_user >= kolvo_money:
                self.buy_person += name + ';'
                signal_notification('Приобретено', self.manager)
                self.buy_or_no[name] = 'куплено'
                self.coins_user -= kolvo_money

            else:
                signal_notification('Недостаточно монет', self.manager)
        elif self.buy_or_no[name] != 'используется':
            for k, v in self.buy_or_no.items():
                if v == 'используется':
                    self.buy_or_no[k] = 'куплено'
                    break
            self.buy_or_no[name] = 'используется'
            self.name_use_person = name
        elif self.buy_or_no[name] == 'используется':
            signal_notification('Уже используется', self.manager)

    def updating_bd(self):
        self.cur.execute(
            f"""UPDATE users SET buy_person = '{self.buy_person}', kolvo_money = {self.coins_user},
            use_person = '{self.name_use_person}'
            WHERE id = '{self.id_player}'""")
        self.con.commit()
        self.con.close()
