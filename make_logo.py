import base64, re, io, colorsys
from PIL import Image

# ── HTML에서 base64 로고 추출 ──
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'class="logo-icon"[^>]*src="data:image/png;base64,([^"]+)"', content)
if not match:
    print("로고 base64 못찾음"); exit()

img_bytes = base64.b64decode(match.group(1))

# 원본 저장
with open('logo_output/logo_original.png', 'wb') as f:
    f.write(img_bytes)
print("원본 저장 완료")

# ─────────────────────────────────────────
# 방법 1: CSS filter 시뮬레이션 HTML 생성
# ─────────────────────────────────────────
html_preview = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Logo Preview - Method 1 (CSS Filter)</title>
<style>
  body { background:#fff; display:flex; flex-direction:column; align-items:center; gap:40px; padding:60px; font-family:sans-serif; }
  h3 { color:#333; margin-bottom:0; }
  .label { font-size:13px; color:#888; margin-top:6px; }
  .original img { height:80px; }
  .method1 img {
    height:80px;
    filter: brightness(0) saturate(100%) invert(39%) sepia(97%) saturate(572%) hue-rotate(346deg) brightness(103%);
  }
</style>
</head>
<body>
  <div class="original">
    <h3>원본</h3>
    <img src="../logo_output/logo_original.png"/>
    <div class="label">현재 파란색 로고</div>
  </div>
  <div class="method1">
    <h3>방법 1 — CSS Filter (#e8500a)</h3>
    <img src="../logo_output/logo_original.png"/>
    <div class="label">전체 오렌지 단색 (CSS filter)</div>
  </div>
</body>
</html>"""

with open('logo_output/preview_method1.html', 'w', encoding='utf-8') as f:
    f.write(html_preview)
print("방법1 HTML 저장 완료")

# ─────────────────────────────────────────
# 방법 2: 픽셀 직접 교체 (파란색 → 오렌지)
# ─────────────────────────────────────────
img = Image.open(io.BytesIO(img_bytes)).convert('RGBA')
pixels = img.load()
w, h = img.size

# #e8500a 의 HSL hue = 약 0.055 (20도)
TARGET_HUE = 20 / 360

changed = 0
for y in range(h):
    for x in range(w):
        r, g, b, a = pixels[x, y]
        if a < 30:
            continue

        # RGB → HLS
        hue, lig, sat = colorsys.rgb_to_hls(r/255, g/255, b/255)

        # 파란 계열 hue: 0.50 ~ 0.75 (180°~270°), 채도 있을 것
        if 0.50 <= hue <= 0.76 and sat > 0.15:
            # lightness 그대로, saturation 약간 강화, hue → 오렌지
            new_sat = min(sat * 1.1, 1.0)
            nr, ng, nb = colorsys.hls_to_rgb(TARGET_HUE, lig, new_sat)
            pixels[x, y] = (int(nr*255), int(ng*255), int(nb*255), a)
            changed += 1

print(f"변경된 픽셀 수: {changed:,}")
img.save('logo_output/logo_orange_v2.png')
print("방법2 PNG 저장 완료")
print("\n완료! logo_output 폴더를 확인하세요.")
