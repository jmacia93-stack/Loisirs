"""Génère toutes les voix et assemble la page « La route des sons »."""
import json, os, re, subprocess, base64, sys, hashlib
sys.path.insert(0, os.path.dirname(__file__))
from content import build_data, PHRASES, CONTINUANTS
from phon import synth

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = '/tmp/lecture_clips'
PIPER = '/tmp/piper/piper'
MODEL = '/tmp/v_voice-fr-siwis-medium/fr-siwis-medium.onnx'
os.makedirs(CACHE, exist_ok=True)

data = build_data()
jobs = []  # (id, kind, payload, length_scale)
for g in data['G']:
    p = g['ph']
    if g['v']:
        jobs.append(('snd:' + g['g'], 'ph', p + 'ː', 2.2))
    elif p in CONTINUANTS:
        jobs.append(('snd:' + g['g'], 'ph', p + 'ːː', 2.8))
    else:
        jobs.append(('snd:' + g['g'], 'ph', p + 'ə', 1.2))
    jobs.append(('ex:' + g['g'], 'txt', g['ex'], 1.08))
for s in data['SYL']:
    if s.get('solo'):
        jobs.append(('syl:' + s['s'], 'ph', s['ph'] + 'ː', 1.5))
        continue
    jobs.append(('syl:' + s['s'], 'ph', s['ph'], 1.25))
    c, v = s['g'][0], s['g'][-1]
    G = {x['g']: x for x in data['G']}
    cp, vp = G[c]['ph'], G[v]['ph']
    if cp in CONTINUANTS:
        jobs.append(('blend:' + s['s'], 'ph', cp + 'ːː' + vp + 'ːː', 2.0))
    else:
        jobs.append(('blend:' + s['s'], 'ph', cp + vp + 'ːː', 1.8))
for w in data['W']:
    jobs.append(('w:' + w['w'], 'txt', w['w'], 1.1))
for k, t in PHRASES.items():
    jobs.append(('p:' + k, 'txt', t, 1.08))


def key(j):
    return hashlib.md5(json.dumps(j[1:], ensure_ascii=False).encode()).hexdigest()


# texte -> piper (en un seul appel)
todo = [j for j in jobs if j[1] == 'txt' and not os.path.exists(f'{CACHE}/{key(j)}.mp3')]
by_ls = {}
for j in todo:
    by_ls.setdefault(j[3], []).append(j)
for ls, js in by_ls.items():
    inp = '\n'.join(json.dumps({'text': j[2], 'output_file': f'{CACHE}/{key(j)}.wav'}, ensure_ascii=False) for j in js)
    subprocess.run([PIPER, '-q', '-m', MODEL, '--json-input', '--length_scale', str(ls)], input=inp.encode(), check=True, stderr=subprocess.DEVNULL)
# phonèmes -> onnx direct
for j in jobs:
    if j[1] == 'ph' and not os.path.exists(f'{CACHE}/{key(j)}.mp3'):
        synth(j[2], f'{CACHE}/{key(j)}.wav', ls=j[3])

FILTER = ('silenceremove=start_periods=1:start_threshold=-45dB,areverse,'
          'silenceremove=start_periods=1:start_threshold=-45dB,areverse,apad=pad_dur=0.1,loudnorm=I=-16:TP=-1.5')
clips = {}
for j in jobs:
    k = key(j)
    mp = f'{CACHE}/{k}.mp3'
    if not os.path.exists(mp):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{CACHE}/{k}.wav', '-af', FILTER, '-ar', '22050', '-ac', '1', '-b:a', '40k', mp], check=True)
    clips[j[0]] = 'data:audio/mpeg;base64,' + base64.b64encode(open(mp, 'rb').read()).decode()

tpl = open(os.path.join(ROOT, 'template.html'), encoding='utf8').read()
html = tpl.replace('__DATA__', json.dumps(data, ensure_ascii=False)).replace('__CLIPS__', json.dumps(clips, ensure_ascii=False))
out = os.path.join(ROOT, 'index.html')
open(out, 'w', encoding='utf8').write(html)
print(len(clips), 'clips,', os.path.getsize(out) // 1024, 'KB ->', out)
