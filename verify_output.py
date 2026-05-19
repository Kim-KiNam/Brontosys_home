import colorsys
from PIL import Image

img = Image.open('logo_output/logo_orange_v3_icon_only.png').convert('RGBA')
pixels = img.load()
w, h = img.size

icon_w = int(w * 0.20)
y_start = h // 2

print("변환 후 아이콘 하단 픽셀:")
seen = set()
count = 0
for y in range(y_start, h):
    for x in range(icon_w):
        r, g, b, a = pixels[x, y]
        if a < 30: continue
        if r > 230 and g > 230 and b > 230: continue
        hue, lig, sat = colorsys.rgb_to_hls(r/255, g/255, b/255)
        key = (r//15*15, g//15*15, b//15*15)
        if key not in seen and sat > 0.05:
            seen.add(key)
            print(f"  RGB({r:3d},{g:3d},{b:3d}) → H={hue*360:.0f}° L={lig:.2f} S={sat:.2f}")
            count += 1
            if count >= 15: break
    if count >= 15: break
