import sys, wave, numpy as np
from PIL import Image, ImageDraw, ImageFilter

def wavify(wav_file, out="out.png", w=1000, h=400,
               bg=(10,10,30), colors=((0,200,255),(255,0,150))):
    with wave.open(wav_file) as wf:
        ch, frames = wf.getnchannels(), wf.getnframes()
        data = np.frombuffer(wf.readframes(frames), dtype=np.int16)
    if ch > 1:
        data = data[::ch]
    data = data / np.max(np.abs(data))
    data = data[::max(1, len(data)//w)]

    grad = Image.new("RGB", (1,h))
    draw = ImageDraw.Draw(grad)
    for i in range(h):
        t = i / h
        draw.point((0,i), tuple(int(a*(1-t)+b*t) for a,b in zip(colors[0], colors[1])))
    grad = grad.resize((w,h))

    mid, amp = h//2, (h//2)*0.85
    pts = [(x, int(mid - s*amp)) for x,s in enumerate(data[:w])] + [(w,mid),(0,mid)]
    mask = Image.new("L",(w,h))
    ImageDraw.Draw(mask).polygon(pts, fill=255)

    img = Image.composite(grad, Image.new("RGB",(w,h), bg), mask)
    img = Image.blend(img.filter(ImageFilter.GaussianBlur(15)), img, 0.7)
    img.save(out)

if __name__ == "__main__":
    wavify(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "out.png")
