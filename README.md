# zjzk_auto
## Description
老夫肝zjzk肝不动了于是一时起了兴致写了这个python脚本（bushi

当前支持自动walkshop检测，自动完成突发事件，自动检测满级人数并达到阈值后停止

分辨率仅支持了1080p

## Usage

打开adb调试

从源码运行：
1. 如果需要等级检测请在path.txt中加入你的tesseract目录并复制traindata到tessdata目录
2. 运行zjzk_auto.py，依次输入模式 大关号 小关号
3. 输入最大允许的满级人数（比如一带二可以输入2，当3人满级时自动停止防止浪费体力）

从release运行：
1. 运行zjzk_auto.exe，依次输入模式 大关号 小关号
2. 输入最大允许的满级人数（比如一带二可以输入2，当3人满级时自动停止防止浪费体力）
