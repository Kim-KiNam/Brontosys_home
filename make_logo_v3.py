import base64, re, io, colorsys
from PIL import Image

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'class="logo-icon"[^>]*src="data:image/png;base64,([^"]+)"', content)
img_bytes = base64.b64decode(match.group(1))

TARGET_HUE = 29 / 360  # #e77000 (H≈29°)
TARGET_SAT = 1.0       # #e77000 채도 100%

# ── v3: 아이콘(밝은 파란) → #e77000 오렌지, 텍스트(어두운 네이비) 유지 ──
img = Image.open(io.BytesIO(img_bytes)).convert('RGBA')
pixels = img.load()
w, h = img.size

for y in range(h):
    for x in range(w):
        r, g, b, a = pixels[x, y]
        if a < 30:
            continue
        hue, lig, sat = colorsys.rgb_to_hls(r/255, g/255, b/255)
        # lig > 0.35: 밝은 파란 아이콘만 변환 (어두운 네이비 텍스트 완전 제외)
        # sat > 0.25: 충분히 채도 있는 파란 픽셀만
        # 아이콘: H≈199°(0.553), S=1.00, L≈0.43 / 텍스트: H≈240°, S≈0.50, L≈0.10
        # sat > 0.60 → 아이콘(S=1.00) 포함, 텍스트(S≈0.50) 제외
        # 아이콘 최대 H≈233°(0.647), 텍스트 최소 H≈238°(0.661) → 0.655 경계로 분리
        if 0.50 <= hue <= 0.655 and sat > 0.40:
            # 어두운 아이콘 픽셀 최소 밝기 보정 (너무 어두우면 오렌지가 안 보임)
            lig_out = max(lig, 0.22)
            nr, ng, nb = colorsys.hls_to_rgb(TARGET_HUE, lig_out, TARGET_SAT)
            pixels[x, y] = (int(nr*255), int(ng*255), int(nb*255), a)

img.save('logo_output/logo_orange_v3_icon_only.png')
print('v3 저장 완료')
