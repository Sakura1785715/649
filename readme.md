# RuoYi-Vue-Flask 启动操作手册

## 🍎 macOS / Linux 系统启动

### 🟢 步骤 1：启动后端
**请打开第 1 个终端窗口，依次执行以下命令：**

```bash
# 1. 进入项目根目录 (请根据你的实际位置调整)
cd ~/Desktop/RuoYi_vue_flask-main

# 2. 激活虚拟环境
source venv/bin/activate

# 3. 设置临时环境变量 (防止报错找不到模块)
export PYTHONPATH=$PYTHONPATH:$(pwd)

# 4. 启动服务
./venv/bin/python ruoyi_admin/app.py
```

### 🔵 步骤 2：启动前端
```bash
# 1. 进入前端目录
cd ~/Desktop/RuoYi_vue_flask-main/ruoyi-ui

# 2. 启动服务
npm run dev
```
## 🍏 Windows 系统启动
### 🟢 步骤 1：启动后端
**打开第 1 个终端窗口，依次执行以下命令：**
```bash
# 1. 进入项目根目录 (请根据你的实际位置调整)
cd RuoYi_vue_flask-main

# 2. 激活虚拟环境
# --- 如果是 CMD 请执行: ---
 venv\Scripts\activate
# --- 如果是 PowerShell 请执行: ---
.\venv\Scripts\Activate.ps1

# 3. 设置环境变量
# --- 如果是 CMD 请执行: ---
 set PYTHONPATH=%PYTHONPATH%;%cd%
# --- 如果是 PowerShell 请执行: ---
$env:PYTHONPATH += ";$PWD"

# 4. 启动服务
python ruoyi_admin\app.py
```
### 🔑 默认登录信息
- 用户名：admin
- 密码：admin123