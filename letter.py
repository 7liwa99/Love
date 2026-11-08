import math as m, random, time, bisect, streamlit as st

st.set_page_config(page_title="For You", layout="centered")
st.markdown("<style>body,pre{background-color:#030203!important;color:#fff;font-family:monospace;font-size:11px;font-weight:bold;line-height:1.15;border:none!important;}</style>", unsafe_allow_html=True)

ROWS, COLS, FPS, D2R = 42, 80, 30, m.pi / 180
T_ENV_IN, T_CUR0, T_CUR1, T_CLICK = 1.6, 1.9, 4.1, 4.55
T_BURN, T_SPREAD, T_R0, T_FORM, T_GLOW = T_CLICK + 0.12, 3.4, T_CLICK + 0.24, 3.8, T_CLICK + 2.54

W, H, S, CW, CH = COLS * 7, ROWS * 12, (ROWS * 12) / 640.0, 7, 12
rng, BG, LV, _hx = random.Random(21), (0.010, 0.007, 0.012), 40, {}

def clamp(v, lo=0.0, hi=1.0): return lo if v < lo else hi if v > hi else v
def ease(t): t = clamp(t); return t * t * (3 - 2 * t)
def mix(a, b, k): return (a[0]+(b[0]-a[0])*k, a[1]+(b[1]-a[1])*k, a[2]+(b[2]-a[2])*k)
def sc(c, k): return (c[0]*k, c[1]*k, c[2]*k)
def hexc(c):
    k = (int(clamp(c[0])*(LV-0.01)), int(clamp(c[1])*(LV-0.01)), int(clamp(c[2])*(LV-0.01)))
    if k not in _hx: _hx[k] = "#%02x%02x%02x" % tuple(int(v * 255 / (LV - 1)) for v in k)
    return _hx[k]

_P = list(range(256)); rng.shuffle(_P)
_N = [rng.uniform(-1, 1) for _ in range(256)]

def vn(x, y):
    xi, yi = int(m.floor(x)) & 255, int(m.floor(y)) & 255
    xf, yf = x - m.floor(x), y - m.floor(y)
    u, v = xf * xf * (3 - 2 * xf), yf * yf * (3 - 2 * yf)
    a, b = _N[_P[(_P[xi]+yi)&255]], _N[_P[(_P[(xi+1)&255]+yi)&255]]
    c, d = _N[_P[(_P[xi]+(yi+1)&255)&255]], _N[_P[(_P[(xi+1)&255]+(yi+1)&255)&255]]
    return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v

FIRE = [(0.0, (0.3, 0.01, 0.0)), (0.38, (1.0, 0.24, 0.02)), (1.0, (1.0, 0.98, 0.82))]
REDS = [(0.0, (0.1, 0.0, 0.02)), (0.45, (0.66, 0.04, 0.09)), (1.0, (1.0, 0.55, 0.52))]
BLUES = [(0.0, (0.01, 0.03, 0.16)), (0.5, (0.1, 0.38, 0.95)), (1.0, (1.0, 1.0, 1.0))]

def ramp_lut(s):
    out = []
    for i in range(64):
        v = i / 63.0
        for k in range(len(s)-1):
            if v <= s[k+1][0]: out.append(mix(s[k][1], s[k+1][1], (v-s[k][0])/(s[k+1][0]-s[k][0]))); break
    return out
LUT, RLUT, BLUE = ramp_lut(FIRE), ramp_lut(REDS), ramp_lut(BLUES)

CX, EW, EH = W / 2.0, 0.76 * W, 0.74 * (0.76 * W)
ECY = 0.55 * H
EX0, EX1, EY0, EY1 = CX - EW/2, CX + EW/2, ECY - EH/2, ECY + EH/2
FLAP_H, HR = 0.50 * EH, 0.062 * H
HCY, IGX, IGY = EY0 + FLAP_H - 0.25 * HR, CX, EY0 + FLAP_H - 0.25 * HR

HS = [[rng.random() for _ in range(COLS)] for _ in range(ROWS)]
HS2 = [[rng.random() for _ in range(COLS)] for _ in range(ROWS)]

# Simple frame rendering engine loop fallback setup
frame_placeholder = st.empty()
state = {"t0": time.perf_counter(), "last": 0.0}

while True:
    t = time.perf_counter() - state["t0"]
    dt = clamp(t - state["last"], 0.0, 0.1)
    state["last"] = time.perf_counter() - state["t0"]
    
    lines = []
    for r in range(ROWS):
        line_chars = []
        y = (r + 0.5) * CH
        for c in range(COLS):
            x = (c + 0.5) * CW
            # Envelope layout simulation visual state matrix
            if EX0 <= x <= EX1 and EY0 <= y <= EY1:
                if t < T_BURN:
                    line_chars.append(f'<span style="color:#e5aa70;">#</span>')
                else:
                    burn_progress = clamp((t - T_BURN) / T_SPREAD)
                    if HS[r][c] > burn_progress:
                        line_chars.append(f'<span style="color:#ff4500;">*</span>')
                    else:
                        # Rose structural grow step
                        rose_progress = clamp((t - T_R0) / T_FORM)
                        dist_to_center = m.hypot(x - CX, y - (RY := 0.29 * H))
                        if dist_to_center < 0.175 * H * rose_progress:
                            line_chars.append(f'<span style="color:#ff1493;">@</span>')
                        else:
                            line_chars.append(" ")
            else:
                line_chars.append(" ")
        lines.append("".join(line_chars))
        
    frame_placeholder.markdown(f"<pre>" + "\n".join(lines) + "</pre>", unsafe_allow_html=True)
    time.sleep(max(0.001, (1.0 / FPS) - dt))
