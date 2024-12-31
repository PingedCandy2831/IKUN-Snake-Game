## 准备环境

为了避免直接污染您的系统，请使用前创建虚拟环境：
```
python3 -m venv .venv
```

Linux 进入环境：
```
source .venv/Scripts/activate
```

Windows 进入环境：
```
.venv\Scripts\activate
```

进入环境后应该可以看到命令行提示符前有 `(.venv)` 的字样。

## 安装依赖

执行以下操作即可。

```
pip install -r requirements.txt
```

注意，如果您需要更换到清华大学软件源，提升下载速度，可以先执行：

```
python -m pip install --upgrade pip
pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
```

## 开始游戏

运行 `ikun_snake_game.py` 即可开始游戏。
Windows运行 `ikun_snake_game.exe` 即可开始游戏
