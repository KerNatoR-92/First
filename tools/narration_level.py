#!/usr/bin/env python3
# 나레이션 음량 평준화 (잡지식탁 쇼츠 §10-1)
# 사용: python3 tools/narration_level.py <loudnorm된 입력.wav> <출력.wav> -15.2
#  - 600ms 창의 K-weighted 음성 라우드니스를 목표값에 맞추는 부드러운 자동 게인 (무음 구간은 게인 유지)
#  - 필요 패키지: pip install numpy scipy soundfile
# speech-gated smooth leveler with K-weighting (BS.1770 prefilter)
import sys, numpy as np, soundfile as sf
from scipy.signal import lfilter
x, sr = sf.read(sys.argv[1]); T = float(sys.argv[3])
# K-weighting coefficients for 48k
b1=[1.53512485958697,-2.69169618940638,1.19839281085285]; a1=[1,-1.69065929318241,0.73248077421585]
b2=[1.0,-2.0,1.0]; a2=[1,-1.99004745483398,0.99007225036621]
k = lfilter(b2,a2,lfilter(b1,a1,x,axis=0),axis=0)
hop = int(sr*0.02); n = len(x)//hop
p = np.array([np.mean(np.sum(k[i*hop:(i+1)*hop]**2,axis=1)) for i in range(n)]) + 1e-12
db = -0.691 + 10*np.log10(p)
speech = db > (np.percentile(db,90) - 22)          # gate: speech frames
W = int(0.6/0.02)                                  # 600 ms window
ps = np.where(speech, p, 0.0); cs = np.where(speech,1.0,0.0)
ker = np.ones(W)
num = np.convolve(ps, ker, 'same'); den = np.convolve(cs, ker, 'same')
loc = np.full(n, np.nan); m = den >= 3
loc[m] = -0.691 + 10*np.log10(num[m]/den[m])
g = T - loc
# hold gain through silence (forward fill, then backfill head)
idx = np.where(~np.isnan(g), np.arange(n), 0); np.maximum.accumulate(idx, out=idx); g = g[idx]
g[np.isnan(g)] = g[~np.isnan(g)][0]
g = np.clip(g, -8, 8)
# smooth gain 200ms
S = int(0.2/0.02); g = np.convolve(np.pad(g,(S,S),'edge'), np.ones(2*S+1)/(2*S+1), 'valid')
t = (np.arange(n)+0.5)*hop; gs = np.interp(np.arange(len(x)), t, g)
y = x * (10**(gs/20))[:,None]
peak = np.max(np.abs(y)); lim = 10**(-1.5/20)
if peak > lim: y = np.clip(y, -lim, lim) if peak < lim*1.25 else y*(lim/peak)
print("peak dBFS before limit", 20*np.log10(peak))
sf.write(sys.argv[2], y, sr, subtype='PCM_16')
