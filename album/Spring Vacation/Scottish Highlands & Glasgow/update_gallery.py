#!/usr/bin/env python3
from pathlib import Path
import re
import sys

# 识别为图片的后缀（不区分大小写）
IMG_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tif', '.tiff', '.svg'}

def pick_md_file():
    md_files = [p for p in Path.cwd().glob("*.md") if p.is_file()]
    if not md_files:
        sys.exit("未找到 .md 文件。")
    # 若有多个 .md，则选修改时间最新的那个
    md_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return md_files[0]

def collect_images():
    imgs = [
        p.name for p in Path.cwd().iterdir()
        if p.is_file() and p.suffix.lower() in IMG_EXTS
    ]
    # 需要按名称排序（不区分大小写）
    imgs.sort(key=lambda s: s.lower())
    return imgs

def main():
    md_path = pick_md_file()
    images = collect_images()
    if not images:
        sys.exit("当前路径没有发现图片。")

    content = md_path.read_text(encoding="utf-8")

    gallery_block = "{% gallery %}\n" + "\n".join(f"![]({name})" for name in images) + "\n{% endgallery %}"

    # 匹配并替换已有的 gallery 块；若不存在则在文末追加
    pattern = re.compile(r"\{%\s*gallery\s*%}.*?\{%\s*endgallery\s*%}", re.S)
    if pattern.search(content):
        new_content = pattern.sub(gallery_block, content, count=1)
    else:
        new_content = content.rstrip() + "\n\n" + gallery_block + "\n"

    md_path.write_text(new_content, encoding="utf-8")
    print(f"已写入 {len(images)} 张图片到: {md_path.name}")

if __name__ == "__main__":
    main()
