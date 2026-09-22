#!/usr/bin/env python3
"""从设计参考图里取色与量尺寸。输出纯文本，供 agent 直接读。

用法:
  sample_colors.py info    IMAGE
  sample_colors.py palette IMAGE [--crop x,y,w,h] [--top N] [--min-share P]
  sample_colors.py sample  IMAGE --points "x,y;x,y" [--avg N]
  sample_colors.py scan    IMAGE --line "x1,y1,x2,y2" [--tolerance N]

坐标可写像素 ("120,340") 或百分比 ("30%,50%")。点数与线宽为 0 的输入会被拒绝。

依赖: Pillow (python3 -m venv .venv && .venv/bin/pip install Pillow)
"""

import argparse
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit(
        "缺少 Pillow。安装方式:\n"
        "  python3 -m venv .venv && .venv/bin/pip install Pillow\n"
        "然后用 .venv/bin/python 运行本脚本。"
    )


def load(path, flatten_bg=(255, 255, 255)):
    """打开图片。带透明通道的压到不透明底色上，否则取出的 hex 没有意义。"""
    try:
        img = Image.open(path)
    except FileNotFoundError:
        sys.exit(f"找不到文件: {path}")
    except OSError as exc:
        sys.exit(f"打不开图片 {path}: {exc}")

    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
        canvas = Image.new("RGB", img.size, flatten_bg)
        canvas.paste(img, mask=img.split()[-1])
        return canvas
    return img.convert("RGB")


def parse_coord(text, size, axis_name):
    """'120' 或 '30%' -> 像素值。"""
    text = text.strip()
    if text.endswith("%"):
        try:
            percent = float(text[:-1])
        except ValueError:
            sys.exit(f"{axis_name} 坐标无法解析: {text}")
        if not 0 <= percent <= 100:
            print(f"警告: {axis_name} 坐标 {text} 超出 0-100%，已夹到边界", file=sys.stderr)
        return min(size - 1, max(0, round(percent / 100.0 * size)))
    try:
        value = float(text)
    except ValueError:
        sys.exit(f"{axis_name} 坐标无法解析: {text}")
    return min(size - 1, max(0, round(value)))


def parse_point(text, size):
    parts = text.split(",")
    if len(parts) != 2:
        sys.exit(f"点坐标应形如 'x,y'，收到: {text}")
    x = parse_coord(parts[0], size[0], "x")
    y = parse_coord(parts[1], size[1], "y")
    return x, y


def hex_of(pixel):
    return "#{:02x}{:02x}{:02x}".format(*pixel)


def average_box(img, x, y, radius):
    """取 (x, y) 周围 (2*radius+1)^2 的均值，用于压制 JPEG 噪点。

    跨在控件边缘上时均值会掺进背景色，那种位置要退回单像素取样。
    """
    if radius <= 0:
        return img.getpixel((x, y))
    left, top = max(0, x - radius), max(0, y - radius)
    right, bottom = min(img.width, x + radius + 1), min(img.height, y + radius + 1)
    box = img.crop((left, top, right, bottom))
    # 缩到 1x1 即区域均值，避免逐像素遍历（也避开了 getdata 的弃用路径）
    return box.resize((1, 1), Image.BOX).getpixel((0, 0))


def cmd_info(args):
    img = load(args.image)
    print(f"路径      {args.image}")
    print(f"尺寸      {img.width} x {img.height} px")
    print(f"比例      {img.width / img.height:.3f}")
    print()
    print("百分比坐标换算: x_px = 宽 * x%, y_px = 高 * y%")


def cmd_palette(args):
    img = load(args.image)

    if args.crop:
        parts = args.crop.split(",")
        if len(parts) != 4:
            sys.exit("--crop 应形如 'x,y,w,h'")
        x, y = parse_point(f"{parts[0]},{parts[1]}", img.size)
        w, h = int(float(parts[2])), int(float(parts[3]))
        if w <= 0 or h <= 0:
            sys.exit("--crop 的宽高必须大于 0")
        img = img.crop((x, y, min(img.width, x + w), min(img.height, y + h)))

    total = img.width * img.height
    quantized = img.quantize(colors=max(2, args.top), method=Image.MEDIANCUT)
    palette = quantized.getpalette()
    counts = sorted(quantized.getcolors(), key=lambda item: item[0], reverse=True)

    print(f"区域      {img.width} x {img.height} px，共 {total} 像素")
    print(f"主色      Top {args.top}，按占比降序，低于 {args.min_share:g}% 的不列")
    print()
    print(f"{'#':>3}  {'hex':<9} {'rgb':<16} {'占比':>7}   条带")
    print("-" * 56)

    shown = 0
    for count, index in counts:
        share = count / total * 100
        if share < args.min_share:
            continue
        rgb = tuple(palette[index * 3 : index * 3 + 3])
        shown += 1
        bar = "█" * max(1, round(share / 2))
        print(f"{shown:>3}  {hex_of(rgb):<9} {str(rgb):<16} {share:>6.1f}%   {bar}")

    if shown == 0:
        print("(没有颜色达到该占比，降低 --min-share 试试)")


def cmd_sample(args):
    img = load(args.image)
    points = [p for p in args.points.split(";") if p.strip()]
    if not points:
        sys.exit("--points 至少给一个点")

    avg_note = f"{args.avg}x{args.avg} 均值" if args.avg > 1 else "单像素"
    print(f"取色      {len(points)} 个点，{avg_note}（图 {img.width}x{img.height}）")
    print()
    print(f"{'#':>3}  {'坐标':<16} {'hex':<9} {'rgb':<16} {'xy':>10}")
    print("-" * 62)

    for index, raw in enumerate(points, start=1):
        x, y = parse_point(raw, img.size)
        rgb = average_box(img, x, y, (args.avg - 1) // 2)
        print(f"{index:>3}  {raw.strip():<16} {hex_of(rgb):<9} {str(rgb):<16} {f'{x},{y}':>10}")


def cmd_scan(args):
    img = load(args.image)

    if "," not in args.line or args.line.count(",") != 3:
        sys.exit("--line 应形如 'x1,y1,x2,y2'")
    parts = args.line.split(",")
    x1, y1 = parse_point(f"{parts[0]},{parts[1]}", img.size)
    x2, y2 = parse_point(f"{parts[2]},{parts[3]}", img.size)

    steps = max(abs(x2 - x1), abs(y2 - y1)) + 1
    if steps <= 1:
        sys.exit("--line 的起点与终点距离太近，量不出东西")

    samples = []
    for step in range(steps):
        ratio = step / (steps - 1)
        x = round(x1 + (x2 - x1) * ratio)
        y = round(y1 + (y2 - y1) * ratio)
        samples.append((x, y, img.getpixel((x, y))))

    segments = []
    for offset, (x, y, rgb) in enumerate(samples):
        if segments:
            last = segments[-1]
            drift = max(abs(rgb[i] - last["rgb"][i]) for i in range(3))
            if drift <= args.tolerance:
                last["length"] += 1
                continue
        segments.append({"start": (x, y), "offset": offset, "rgb": rgb, "length": 1})

    print(f"扫描      ({x1},{y1}) -> ({x2},{y2})，{steps} 步，容差 {args.tolerance}/通道")
    print(f"总长      {steps} px")
    print()
    print(f"{'#':>3}  {'hex':<9} {'rgb':<16} {'长度':>7}  {'起点':<12} {'沿线偏移':>10}")
    print("-" * 66)
    for index, seg in enumerate(segments, start=1):
        start = f"{seg['start'][0]},{seg['start'][1]}"
        print(
            f"{index:>3}  {hex_of(seg['rgb']):<9} {str(seg['rgb']):<16} "
            f"{seg['length']:>5} px  {start:<12} {seg['offset']:>7} px"
        )

    print()
    print("分段长度就是间距与尺寸。多扫几条线取一致值，落在抗锯齿上的那一段要忽略。")


def main():
    parser = argparse.ArgumentParser(
        description="从设计参考图取色与量尺寸。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_info = sub.add_parser("info", help="图片尺寸与格式")
    p_info.add_argument("image")
    p_info.set_defaults(func=cmd_info)

    p_pal = sub.add_parser("palette", help="主色聚类")
    p_pal.add_argument("image")
    p_pal.add_argument("--crop", help="只统计该区域，'x,y,w,h'，坐标可写百分比")
    p_pal.add_argument("--top", type=int, default=16, help="最多列出几种颜色，默认 16")
    p_pal.add_argument("--min-share", type=float, default=0.5, help="过滤阈值，百分比，默认 0.5")
    p_pal.set_defaults(func=cmd_palette)

    p_sam = sub.add_parser("sample", help="定点取色")
    p_sam.add_argument("image")
    p_sam.add_argument("--points", required=True, help="'x,y;x,y'，坐标可写百分比")
    p_sam.add_argument("--avg", type=int, default=1, help="取 NxN 均值，奇数，默认 1（JPEG 噪点大时用 3）")
    p_sam.set_defaults(func=cmd_sample)

    p_scan = sub.add_parser("scan", help="沿线条扫描，输出颜色分段与像素长度")
    p_scan.add_argument("image")
    p_scan.add_argument("--line", required=True, help="'x1,y1,x2,y2'，坐标可写百分比")
    p_scan.add_argument("--tolerance", type=int, default=8, help="同一段的通道容差，默认 8")
    p_scan.set_defaults(func=cmd_scan)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
