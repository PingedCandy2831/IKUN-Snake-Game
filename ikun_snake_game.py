import tkinter as tk
import random
import json  # 导入json模块
import os  # 添加os模块导入
try:
    import pygame  # 导入pygame库
    print("pygame库已成功导入")  # 添加调试信息
except ModuleNotFoundError:
    print("请安装pygame库，可以使用以下命令安装：pip install pygame")
    exit()

# 确保已安装pygame库，可以使用以下命令安装：
# pip install pygame

from PIL import Image, ImageTk  # 导入PIL库

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Ikun贪吃蛇")
        
        # 创建左侧按钮框架
        self.left_frame = tk.Frame(root)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")
        
        # 创建右侧按钮框架
        self.right_frame = tk.Frame(root)
        self.right_frame.grid(row=0, column=2, padx=10, pady=10, sticky="ns")
        
        self.canvas = tk.Canvas(root, width=400, height=400, bg="black")
        self.canvas.grid(row=0, column=1, padx=10, pady=10)  # 将画布放置在中间
        
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.snake_direction = "Right"
        self.food = self.create_food()
        self.game_over = False
        self.canvas.bind("<KeyPress>", self.change_direction)
        self.canvas.focus_set()
        pygame.mixer.init()  # 初始化pygame.mixer
        self.game_over_sound = pygame.mixer.Sound(os.path.join("sounds", "game_over.wav"))  # 加载音效文件
        self.global_sound = pygame.mixer.Sound(os.path.join("sounds", "global_sound.wav"))  # 加载全局音效文件
        self.game_start_sound = pygame.mixer.Sound(os.path.join("sounds", "game_start.wav"))  # 加载游戏开始音效文件
        # 初始化分数
        self.score = 0
        # 添加历史分数属性
        self.high_score = self.load_high_score()  # 加载历史分数
        # 添加声音开关属性
        self.load_settings()  # 加载保存的声音设置
        # 添加按钮
        self.start_sound_toggle_button = tk.Button(self.left_frame, text="开关开始音效", command=self.toggle_start_sound)
        self.start_sound_toggle_button.pack(side=tk.TOP, padx=10, pady=5, anchor=tk.W)  # 将按钮放置在左侧，并添加间距

        self.sound_button = tk.Button(self.left_frame, text="开关声音", command=self.toggle_sound)
        self.sound_button.pack(side=tk.TOP, padx=10, pady=5, anchor=tk.W)  # 将按钮放置在左侧，并添加间距

        self.global_sound_button = tk.Button(self.left_frame, text="开关全局音效", command=self.toggle_global_sound)  # 添加全局音效开关按钮
        self.global_sound_button.pack(side=tk.TOP, padx=10, pady=5, anchor=tk.W)  # 将按钮放置在左侧，并添加间距

        self.reset_high_score_button = tk.Button(self.left_frame, text="重置最高分", command=self.reset_high_score)
        self.reset_high_score_button.pack(side=tk.TOP, padx=10, pady=5, anchor=tk.W)  # 将按钮放置在左侧，并添加间距

        self.start_pause_button = tk.Button(self.left_frame, text=">>开始游戏<<", command=self.toggle_game_state)
        self.start_pause_button.pack(side=tk.TOP, padx=10, pady=5)  # 将按钮放置在左侧，并添加间距

        self.restart_button = tk.Button(self.left_frame, text=">>重新开始<<", command=self.restart_game)
        self.restart_button.pack(side=tk.TOP, padx=10, pady=5)  # 将按钮放置在左侧，并添加间距
        self.restart_button.pack_forget()  # 隐藏“重新开始”按钮

        # 加载自定义图像并调整尺寸
        original_image = Image.open(os.path.join("images", "ikun.png"))  # 加载自定义图像并调整尺寸
        resized_image = original_image.resize((50, 50))  # 调整图像尺寸为50x50
        self.custom_image = ImageTk.PhotoImage(resized_image)

        self.custom_image_button = tk.Button(self.right_frame, image=self.custom_image, command=self.play_ikun_ji_sound)  # 修改command参数
        self.custom_image_button.pack(side=tk.TOP, padx=10, pady=5)  # 将按钮放置在右侧，并添加间距

        # 添加新的标签来显示“点击头像有鸡叫”
        self.click_avatar_label = tk.Label(self.right_frame, text="点击头像有惊喜", fg="white", bg="black", font=("Arial", 12))
        self.click_avatar_label.pack(side=tk.TOP, padx=10, pady=5)

        # 播放全局音效
        if self.global_sound_enabled:
            self.global_sound.play()

        self.high_score_label = tk.Label(self.right_frame, text=f"最高分: {self.high_score}", fg="white", bg="black", font=("Arial", 14))
        self.high_score_label.pack(side=tk.TOP, padx=10, pady=5)

        self.score_label = tk.Label(self.right_frame, text=f"分数: {self.score}", fg="white", bg="black", font=("Arial", 14))
        self.score_label.pack(side=tk.TOP, padx=10, pady=5)

        self.reset_high_score_button = tk.Button(self.right_frame, text="重置最高分", command=self.reset_high_score)
        self.reset_high_score_button.pack(side=tk.TOP, padx=10, pady=5)  # 将按钮放置在右侧，并添加间距

        self.update_id = None  # 添加一个属性来存储定时器ID

        # 设置主窗口的行和列权重，使内容居中偏上
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.columnconfigure(2, weight=1)
        
        # 注释掉 self.update() 调用，确保游戏开始时贪吃蛇是静止的
        # self.update()
        self.update_sound_button_text()  # 设置初始按钮文本
        self.update_global_sound_button_text()  # 设置初始全局音效开关按钮文本
        self.update_start_sound_button_text()  # 设置初始开始音效开关按钮文本
        # 添加分数和历史分数显示

    def create_food(self):
        x = random.randint(1, 39) * 10
        y = random.randint(1, 39) * 10
        return (x, y)

    def change_direction(self, event):
        if event.keysym in ["Left", "Right", "Up", "Down"]:
            if event.keysym == "Left" and self.snake_direction != "Right":
                self.snake_direction = "Left"
            elif event.keysym == "Right" and self.snake_direction != "Left":
                self.snake_direction = "Right"
            elif event.keysym == "Up" and self.snake_direction != "Down":
                self.snake_direction = "Up"
            elif event.keysym == "Down" and self.snake_direction != "Up":
                self.snake_direction = "Down"

    def load_settings(self):
        try:
            with open('settings.json', 'r') as file:
                settings = json.load(file)
                self.sound_enabled = settings.get('sound_enabled', True)
                self.global_sound_enabled = settings.get('global_sound_enabled', True)  # 加载全局音效开关设置
                self.start_sound_enabled = settings.get('start_sound_enabled', True)  # 加载开始音效开关设置
        except FileNotFoundError:
            self.sound_enabled = True
            self.global_sound_enabled = True  # 默认全局音效开关开启
            self.start_sound_enabled = True  # 默认开始音效开关开启

    def save_settings(self):
        with open('settings.json', 'w') as file:
            json.dump({'sound_enabled': self.sound_enabled, 'global_sound_enabled': self.global_sound_enabled, 'start_sound_enabled': self.start_sound_enabled}, file)  # 保存开始音效开关设置

    def load_high_score(self):
        try:
            with open('high_score.json', 'r') as file:
                return json.load(file).get('high_score', 0)
        except FileNotFoundError:
            return 0

    def save_high_score(self):
        with open('high_score.json', 'w') as file:
            json.dump({'high_score': self.high_score}, file)

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        self.save_settings()  # 保存声音开关设置
        self.update_sound_button_text()  # 更新声音开关按钮文本
        if self.sound_enabled:
            self.game_over_sound.play()  # 播放音效

    def toggle_global_sound(self):
        self.global_sound_enabled = not self.global_sound_enabled
        self.save_settings()  # 保存全局音效开关设置
        self.update_global_sound_button_text()  # 更新全局音效开关按钮文本
        if self.global_sound_enabled:
            self.global_sound.play()  # 点击开时立即播放音效
        else:
            self.global_sound.stop()  # 点击关时立即停止音效

    def toggle_start_sound(self):
        self.start_sound_enabled = not self.start_sound_enabled
        self.save_settings()  # 保存开始音效开关设置
        self.update_start_sound_button_text()  # 更新开始音效开关按钮文本
        if self.start_sound_enabled:
            self.game_start_sound.play()  # 播放音效
        else:
            self.game_start_sound.stop()  # 点击关时立即停止音效

    def update(self):
        if self.game_over:
            self.canvas.create_text(200, 200, text="游戏结束", fill="red", font=("Arial", 24))
            # 根据声音开关属性决定是否播放音效
            if self.sound_enabled:
                self.game_over_sound.play()  # 播放音效
            # 保存当前分数为历史分数
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()
            return

        new_head = self.snake[0]
        if self.snake_direction == "Right":
            new_head = (new_head[0] + 10, new_head[1])
        elif self.snake_direction == "Left":
            new_head = (new_head[0] - 10, new_head[1])
        elif self.snake_direction == "Up":
            new_head = (new_head[0], new_head[1] - 10)
        elif self.snake_direction == "Down":
            new_head = (new_head[0], new_head[1] + 10)

        if new_head in self.snake or new_head[0] < 0 or new_head[0] >= 400 or new_head[1] < 0 or new_head[1] >= 400:
            self.game_over = True
        else:
            self.snake.insert(0, new_head)
            if new_head == self.food:
                self.food = self.create_food()
                # 更新分数
                self.score += 10
                # 根据全局音效开关属性决定是否播放音效

            else:
                self.snake.pop()

        self.canvas.delete("all")
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 10, segment[1] + 10, fill="green")
        self.canvas.create_rectangle(self.food[0], self.food[1], self.food[0] + 10, self.food[1] + 10, fill="red")
        self.update_score_labels()  # 更新分数和历史分数标签
        if self.update_id:  # 取消之前的定时器
            self.root.after_cancel(self.update_id)
        self.update_id = self.root.after(100, self.update)  # 重新设置定时器

    def update_score_labels(self):
        self.high_score_label.config(text=f"最高分: {self.high_score}")
        self.score_label.config(text=f"分数: {self.score}")

    def update_sound_button_text(self):
        if self.sound_enabled:
            self.sound_button.config(text="游戏结束音效：开")
        else:
            self.sound_button.config(text="游戏结束音效：关")

    def update_global_sound_button_text(self):
        if self.global_sound_enabled:
            self.global_sound_button.config(text="全局音效：开")
        else:
            self.global_sound_button.config(text="全局音效：关")

    def update_start_sound_button_text(self):
        if self.start_sound_enabled:
            self.start_sound_toggle_button.config(text="游戏开始音效：开")
        else:
            self.start_sound_toggle_button.config(text="游戏开始音效：关")

    def restart_game(self):
        # 重置游戏状态
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.snake_direction = "Right"
        self.food = self.create_food()
        self.game_over = False
        self.score = 0
        self.update_score_labels()  # 更新分数和历史分数标签
        self.canvas.delete("all")  # 清空画布重新开始
        if self.update_id:  # 取消之前的定时器
            self.root.after_cancel(self.update_id)
        self.update_id = self.root.after(100, self.update)  # 重新设置定时器
        # 播放游戏开始音效
        if self.start_sound_enabled:
            self.game_start_sound.play()
        self.restart_button.pack()  # 显示“重新开始”按钮
        self.start_pause_button.config(text=">>暂停游戏<<")  # 修改开始游戏按钮的文本

    def reset_high_score(self):
        # 重置最高分
        self.high_score = 0
        self.save_high_score()
        self.update_score_labels()  # 更新分数和历史分数标签

    def play_ikun_ji_sound(self):
        pygame.mixer.Sound(os.path.join("sounds", "Ikun_Ji.wav")).play()  # 添加新方法，播放Ikun_Ji.wav文件

    def toggle_game_state(self):
        if self.start_pause_button["text"] == ">>开始游戏<<":
            self.start_game()
        elif self.start_pause_button["text"] == ">>暂停游戏<<":
            self.pause_game()
        elif self.start_pause_button["text"] == ">>继续游戏<<":
            self.resume_game()

    def start_game(self):
        self.game_over = False
        self.start_pause_button.config(text=">>暂停游戏<<")
        self.update_id = self.root.after(100, self.update)  # 重新设置定时器
        if self.start_sound_enabled:
            self.game_start_sound.play()
        self.restart_button.pack()  # 显示“重新开始”按钮

    def pause_game(self):
        self.start_pause_button.config(text=">>继续游戏<<")
        if self.update_id:  # 取消之前的定时器
            self.root.after_cancel(self.update_id)
            self.update_id = None

    def resume_game(self):
        self.start_pause_button.config(text=">>暂停游戏<<")
        self.update_id = self.root.after(100, self.update)  # 重新设置定时器

    # 添加新的方法来播放开始音效
    def play_start_sound(self):
        pygame.mixer.Sound(".//sounds//Ikun_Ji.wav").play()  # 播放Ikun_Ji.wav文件

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()