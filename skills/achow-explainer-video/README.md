# achow-explainer-video · 知识讲解类视频

模拟数据重建页面 → 3D 倾斜一镜到底 → 逐项高亮讲解 + 卡通主讲人 + 配音字幕 + BGM 闪避音效，输出 1080×1920 竖版。

```bash
cd templates && npm install
python3 build.py ../examples/02-audience --keyframes-only
python3 build.py ../examples/02-audience
```
详见 [SKILL.md](SKILL.md)。BGM 与音效均为 numpy 实时合成，无版权问题。
