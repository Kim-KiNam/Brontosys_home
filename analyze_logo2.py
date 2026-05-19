import base64, re, io, colorsys
from PIL import Image

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'class="logo-icon"[^>]*src="data:image/png;base64,([^"]+)"', content)
img_bytes = base64.b64decode(match.group(1))
img = Image.open(io.BytesIO(img_bytes)).convert('RGBA')
pixels = img.load()
w, h = img.size

# 아이콘 영역 왼쪽 20%, 하단 절반
icon_w = int(w * 0.20)
y_start = h // 2

print(f"아이콘 하단 영역 분석 (x:0~{icon_w}, y:{y_start}~{h})")
seen = set()
count = 0
for y in range(y_start, h):
    for x in range(icon_w):
        r, g, b, a = pixels[x, y]
        if a < 30: continue
        if r > 230 and g > 230 and b > 230: continue  # 흰색 제외
        hue, lig, sat = colorsys.rgb_to_hls(r/255, g/255, b/255)
        key = (r//10*10, g//10*10, b//10*10)
        if key not in seen and sat > 0.05:
            seen.add(key)
            print(f"  RGB({r:3d},{g:3d},{b:3d}) → H={hue*360:.0f}° L={lig:.2f} S={sat:.2f}")
            count += 1
            if count >= 25: break
    if count >= 25: break
