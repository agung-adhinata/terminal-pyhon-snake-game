from random import randint
import threading
from time import sleep
import keyboard
from os import system


class MainMenu:
    def __init__(self) -> None:
        self.display_size = [21, 42]
        self.canvas = [[0]*self.display_size[1]]*self.display_size[0]
        self.middlewware = [11, 21]

    def game_over(self, score):
        print(f"game over, your score is {score} ")
        print("-"*self.display_size[0])
        print("\n press any key to close")


main_menu = MainMenu()


class Game():
    def __init__(self) -> None:
        self.keys = ''
        self.is_game_over = False
        self.is_player_eat = False
        self.display_size = [42, 21]
        self.display_list = [[0] * self.display_size[0]] * self.display_size[1]
        self.time_iteration_current = 0
        self.time_iteration_limit = 100
        self.time_iteration_increment = 1
        self.player_score = 0
        self.player_start = [10, 7]
        self.player_segment = [list.copy(self.player_start), [9, 7], [8, 7]]
        self.player_direction = [1, 0]
        self.player_speed_in_second = 0.2
        self.food_coordinate = [
            randint(1, self.display_size[0]-2), randint(1, self.display_size[1]-2)]
        print(f"food coordinate: {self.food_coordinate}")
        print(
            f" size x: {len(self.display_list[0])} , y: {len(self.display_list)}")
        sleep(2)

    def shuffle_food_coordinate(self):
        self.food_coordinate = [
            randint(1, self.display_size[0]-2), randint(1, self.display_size[1]-2)]

    def display(self):
        system('cls')
        display_item = []
        display_item = list.copy(self.display_list)
        length_y = len(display_item)-1
        length_x = len(display_item[0])-1

        for y in range(length_y):
            x_ray = ['.'] * length_x
            for x in range(length_x):
                for item in self.player_segment:
                    if(item[0] == x and item[1] == y):
                        x_ray[x] = "O"
                if self.food_coordinate[0] == x and self.food_coordinate[1] == y:
                    x_ray[x] = "X"
            for item in x_ray:
                print(item, end="", sep="")
            print()
        print(
            f"score: {self.player_score} - food_coordinate: {self.food_coordinate}")

    def keyboard_controller(self):
        # print("thread")
        while True:
            key_before = self.keys
            key_pressed:str = keyboard.read_key()
            self.keys = key_pressed
            if(key_pressed != key_before):
                if key_pressed == "a" or key_pressed == "left":
                    self.player_direction = [-1, 0]
                if key_pressed == "d" or key_pressed == "right":
                    self.player_direction = [1, 0]
                if key_pressed == "w" or key_pressed == "up":
                    self.player_direction = [0, -1]
                if key_pressed == "s" or key_pressed == "down":
                    self.player_direction = [0, 1]
                # print(f"thread 2 input : {key_pressed}")
                if(self.keys == 'esc'):
                    print("thread keyboard listener terminated")
                    break
                if(self.is_game_over):
                    print("game over signed")
                    break

    def multilist_shifter(self, multilist):
        new_list = []
        new_list = list.copy(multilist)
        new_list.insert(0, [0, 0])
        if(self.is_player_eat):
            self.is_player_eat = False
        else:
            new_list.pop(-1)
        return new_list

    def player_movement(self):
        # tail go forward
        head_list = list.copy(self.player_segment[0])
        head_list[0] += self.player_direction[0]
        head_list[1] += self.player_direction[1]
        temp_list = self.multilist_shifter(self.player_segment)
        temp_list[0] = list.copy(head_list)
        head_list = []
        self.player_segment = []
        self.player_segment = temp_list

    def food_handler(self):
        for item in self.player_segment:
            if(item[0] == self.food_coordinate[0] and item[1] == self.food_coordinate[1]):
                self.shuffle_food_coordinate()
                self.is_player_eat = True
                self.player_score += 1

    def player_collision(self):
        for i, item in enumerate(self.player_segment):
            if item == self.player_segment[0] and i != 0:
                print(
                    f"collide with self, {item} and {self.player_segment[i]} ")
                self.is_game_over = True

    def main(self):
        global main_menu
        while True:
            self.player_movement()
            self.player_collision()
            if(self.is_game_over):
                main_menu.game_over(self.player_score)
                break
            self.food_handler()
            self.display()

            sleep(self.player_speed_in_second)
            if(self.keys == 'esc'):
                print("esc key detected, main thread terminated")
                break


if __name__ == "__main__":
    app = Game()
    t_key_listener = threading.Thread(target=app.keyboard_controller)
    t_main = threading.Thread(target=app.main)
    t_main.start()
    t_key_listener.start()
    t_key_listener.join()
