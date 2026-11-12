# Yuki Studio

- `dist/` 是年轻版作品集的静态源码，包含首页、简历、AI 走查助手案例及互动演示。
- `classic/` 是深色版完整源码及构建产物，包含年轻版作品列表引用的其他案例。
- `design/studio-hero-concept.png` 是最新手绘风格的首屏静态设计稿。

年轻版本地预览

```sh
python3 -m http.server 4173 --bind 127.0.0.1 --directory dist
```

深色版本地预览

```sh
python3 -m http.server 4174 --bind 127.0.0.1 --directory classic/dist
```

深色版构建说明见 [classic/README.md](classic/README.md)。`studio-preview` 用于保存与预览，两个已发布分支各自维护。
