import base64, re, io, colorsys
from PIL import Image
from collections import Counter

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'class="logo-icon"[^>]*src="data:image/png;base64,([^"]+)"', content)
img_bytes = base64.b64decode(match.group(1))
img = Image.open(io.BytesIO(img_bytes)).convert('RGBA')
pixels = img.load()
w, h = img.size

print(f"이미지 크기: {w} x {h}")

# 아이콘 영역 (왼쪽 ~18%), 텍스트 영역 (오른쪽)
icon_w = int(w * 0.18)

print("\n[아이콘 영역 파란 픽셀 샘플 - HLS]")
count = 0
for y in range(h):
    for x in range(icon_w):
        r, g, b, a = pixels[x, y]
        if a < 30 or (r > 240 and g > 240 and b > 240): continue
        hue, lig, sat = colorsys.rgb_to_hls(r/255, g/255, b/255)
        if 0.45 <= hue <= 0.80 and sat > 0.1:
            print(f"  RGB({r:3d},{g:3d},{b:3d}) → H={hue*360:.0f}° L={lig:.2f} S={sat:.2f}")
            count += 1
            if count >= 20: break
    if count >= 20: break

print("\n[텍스트 영역 어두운 픽셀 샘플 - HLS]")
text_x_start = int(w * 0.22)
count = 0
for y in range(h):
    for x in range(text_x_start, min(text_x_start + int(w*0.15), w)):
        r, g, b, a = pixels[x, y]
        if a < 30 or (r > 200 and g > 200 and b > 200): continue
        hue, lig, sat = colorsys.rgb_to_hls(r/255, g/255, b/255)
        if sat > 0.1:
            print(f"  RGB({r:3d},{g:3d},{b:3d}) → H={hue*360:.0f}° L={lig:.2f} S={sat:.2f}")
            count += 1
            if count >= 20: break
    if count >= 20: break
