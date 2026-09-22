#!/usr/bin/env python3
"""从设计参考图里取色与量尺寸。输出纯文本，供 agent 直接读。

用法:
  sample_colors.py info    IMAGE
  sample_colors.py palette IMAGE [--crop x,y,w,h] [--top N] [--min-share P]
  sample_colors.py sample  IMAGE --points "x,y;x,y" [--avg N]
  sample_colors.py scan    IMAGE --line "x1,y1,x2,y2" [--tolerance N]

palette 报的每个颜色都取自像素本身；scan 的容差比的是相邻像素，默认 4。

坐标可写像素 ("120,340") 或百分比 ("30%,50%")。点数与线宽为 0 的输入会被拒绝。

颜色同时给出 hex 与 oklch。oklch 一列可以直接粘进 CSS（shadcn 的主题令牌就用这个格式），
所以取到色之后不需要再手工换算。

依赖: Pillow (python3 -m venv .venv && .venv/bin/pip install Pillow)
"""

import argparse
import math
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


def srgb_to_oklch(pixel):
    """sRGB 0-255 -> OKLCh。矩阵取自 Ottosson 的 oklab 参考实现。"""

    def to_linear(channel):
        c = channel / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (to_linear(v) for v in pixel)
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = (math.copysign(abs(v) ** (1 / 3), v) for v in (l, m, s))

    lightness = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    b2 = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_

    chroma = math.hypot(a, b2)
    hue = math.degrees(math.atan2(b2, a)) % 360
    return lightness, chroma, hue


def _num(value, places):
    text = f"{value:.{places}f}"
    return text.rstrip("0").rstrip(".") if "." in text else text


def oklch_of(pixel):
    """写成可直接粘进 CSS 的形式，例如 oklch(0.4885 0.2428 264.05)。

    无彩色（chroma 近 0）的色相没有意义，固定写 0，免得每取一次灰都报一个随机角度。
    """
    lightness, chroma, hue = srgb_to_oklch(pixel)
    if chroma < 5e-4:
        hue = 0.0
    return f"oklch({_num(lightness, 4)} {_num(chroma, 4)} {_num(hue, 2)})"


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


EXACT_COLOR_CAP = 1 << 16


def count_colors(img):
    """按出现次数统计颜色，返回 (列表, 是否精确)。

    颜色种类不多时（UI 稿、截图基本都是）逐色精确统计，报出的每个值图上都真实存在；
    种类过多（照片）才退回量化，这时只能给近似色，调用方要如实标注。
    """
    exact = img.getcolors(EXACT_COLOR_CAP)
    if exact is not None:
        return exact, True

    quantized = img.quantize(colors=256, method=Image.MEDIANCUT)
    palette = quantized.getpalette()
    counts = [
        (count, tuple(palette[index * 3 : index * 3 + 3]))
        for count, index in quantized.getcolors()
    ]
    return counts, False


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
        try:
            w, h = int(float(parts[2])), int(float(parts[3]))
        except ValueError:
            sys.exit("--crop 的宽高要写像素值，如 '100,80,320,200'")
        if w <= 0 or h <= 0:
            sys.exit("--crop 的宽高必须大于 0")
        img = img.crop((x, y, min(img.width, x + w), min(img.height, y + h)))

    total = img.width * img.height
    counts, exact = count_colors(img)
    counts.sort(key=lambda item: item[0], reverse=True)

    kind = "逐色精确统计" if exact else "近似色（颜色种类过多，已量化到 256 色）"
    print(f"区域      {img.width} x {img.height} px，共 {total} 像素")
    print(f"主色      {kind}，最多 {args.top} 行，低于 {args.min_share:g}% 的不列")
    print()
    print(f"{'#':>3}  {'hex':<9} {'oklch':<28} {'rgb':<16} {'占比':>7}   条带")
    print("-" * 85)

    shown = 0
    for count, rgb in counts:
        share = count / total * 100
        if share < args.min_share:
            continue
        shown += 1
        if shown > args.top:
            shown -= 1
            break
        bar = "█" * max(1, round(share / 2))
        print(
            f"{shown:>3}  {hex_of(rgb):<9} {oklch_of(rgb):<28} {str(rgb):<16} "
            f"{share:>6.1f}%   {bar}"
        )

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
    print(f"{'#':>3}  {'坐标':<16} {'hex':<9} {'oklch':<28} {'rgb':<16} {'xy':>10}")
    print("-" * 95)

    for index, raw in enumerate(points, start=1):
        x, y = parse_point(raw, img.size)
        rgb = average_box(img, x, y, (args.avg - 1) // 2)
        print(
            f"{index:>3}  {raw.strip():<16} {hex_of(rgb):<9} {oklch_of(rgb):<28} "
            f"{str(rgb):<16} {f'{x},{y}':>10}"
        )


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
            previous = samples[offset - 1][2]
            drift = max(abs(rgb[i] - previous[i]) for i in range(3))
            if drift <= args.tolerance:
                last = segments[-1]
                last["end"] = (x, y)
                last["length"] += 1
                continue
        segments.append({"start": (x, y), "end": (x, y), "rgb": rgb, "length": 1})

    print(f"扫描      ({x1},{y1}) -> ({x2},{y2})，{steps} 步，容差 {args.tolerance}/通道（比相邻像素）")
    print(f"总长      {steps} px")
    print()
    # oklch 排在最后：本命令的主产出是长度，超宽时被折到下一行的应该是颜色而不是尺寸
    print(f"{'#':>3}  {'hex':<9} {'rgb':<16} {'长度':>7}  {'起点':<12} {'终点':<12}  oklch")
    print("-" * 95)
    for index, seg in enumerate(segments, start=1):
        start = f"{seg['start'][0]},{seg['start'][1]}"
        end = f"{seg['end'][0]},{seg['end'][1]}"
        print(
            f"{index:>3}  {hex_of(seg['rgb']):<9} {str(seg['rgb']):<16} "
            f"{seg['length']:>5} px  {start:<12} {end:<12}  {oklch_of(seg['rgb'])}"
        )

    print()
    print("分段长度就是间距与尺寸。容差比的是相邻像素，平缓渐变会合成一段，那种位置用 sample 定点确认。")
    print("多扫几条线取一致值，落在抗锯齿上的那一段要忽略。")


def main():
    parser = argparse.ArgumentParser(
        description="从设计参考图取色与量尺寸。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_info = sub.add_parser("info", help="图片尺寸与格式")
    p_info.add_argument("image")
    p_info.set_defaults(func=cmd_info)

    p_pal = sub.add_parser("palette", help="主色统计（逐色精确，颜色过多时退回量化）")
    p_pal.add_argument("image")
    p_pal.add_argument("--crop", help="只统计该区域，'x,y,w,h'，坐标可写百分比")
    p_pal.add_argument("--top", type=int, default=16, help="最多列几行，默认 16")
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
    p_scan.add_argument("--tolerance", type=int, default=4, help="相邻像素的通道容差，默认 4")
    p_scan.set_defaults(func=cmd_scan)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
