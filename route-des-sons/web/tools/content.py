# Contenu pédagogique de « La route des sons » (méthode syllabique, français)
# g = graphème affiché, ph = phonème (IPA, voix piper), ex = exemple, lvl = palier

GRAPHEMES = [
    # palier 1 : voyelles simples + consonnes qui se prolongent (faciles à « chanter »)
    dict(g='a', ph='a', v=True,  lvl=1, ex='comme ananas', e='🍍'),
    dict(g='i', ph='i', v=True,  lvl=1, ex='comme igloo', e='🧊'),
    dict(g='o', ph='o', v=True,  lvl=1, ex='comme moto', e='🏍️'),
    dict(g='m', name='èm', ph='m', v=False, lvl=1, ex='comme moto', e='🏍️'),
    dict(g='l', name='èl', ph='l', v=False, lvl=1, ex='comme lune', e='🌙'),
    # palier 2
    dict(g='u', ph='y', v=True,  lvl=2, ex='comme tortue', e='🐢'),
    dict(g='é', ph='e', v=True,  lvl=2, ex='comme vélo', e='🚲'),
    dict(g='r', name='èr', ph='ʁ', v=False, lvl=2, ex='comme radio', e='📻'),
    dict(g='s', name='ès', ph='s', v=False, lvl=2, ex='comme soleil', e='☀️'),
    # palier 3
    dict(g='f', name='èf', ph='f', v=False, lvl=3, ex='comme fusée', e='🚀'),
    dict(g='ch', name='ché', ph='ʃ', v=False, lvl=3, ex='comme chat', e='🐱'),
    dict(g='n', name='èn', ph='n', v=False, lvl=3, ex='comme nuage', e='☁️'),
    dict(g='v', name='vé', ph='v', v=False, lvl=3, ex='comme voiture', e='🚗'),
    # palier 4 : premières consonnes « qui claquent »
    dict(g='p', name='pé', ph='p', v=False, lvl=4, ex='comme pomme', e='🍎'),
    dict(g='t', name='té', ph='t', v=False, lvl=4, ex='comme tracteur', e='🚜'),
    dict(g='e', ph='ə', v=True,  lvl=4, ex='comme cheval', e='🐴'),
    # palier 5
    dict(g='b', name='bé', ph='b', v=False, lvl=5, ex='comme bus', e='🚌'),
    dict(g='d', name='dé', ph='d', v=False, lvl=5, ex='comme dé', e='🎲'),
    dict(g='j', name='ji', ph='ʒ', v=False, lvl=5, ex='comme judo', e='🥋'),
    # palier 6
    dict(g='c', name='cé', ph='k', v=False, lvl=6, ex='comme camion', e='🚚'),
    dict(g='g', name='gé', ph='ɡ', v=False, lvl=6, ex='comme gorille', e='🦍'),
    dict(g='z', name='zèd', ph='z', v=False, lvl=6, ex='comme zèbre', e='🦓'),
]
CONTINUANTS = set('mlsʁfʃnvʒz')

WORDS = [
    ('lama', ['la', 'ma'], '🦙'), ('vélo', ['vé', 'lo'], '🚲'), ('sofa', ['so', 'fa'], '🛋️'),
    ('moto', ['mo', 'to'], '🏍️'), ('tomate', ['to', 'ma', 'te'], '🍅'), ('tulipe', ['tu', 'li', 'pe'], '🌷'),
    ('piano', ['pi', 'a', 'no'], '🎹'), ('lune', ['lu', 'ne'], '🌙'), ('vache', ['va', 'che'], '🐄'),
    ('pirate', ['pi', 'ra', 'te'], '🏴‍☠️'), ('salade', ['sa', 'la', 'de'], '🥗'), ('bébé', ['bé', 'bé'], '👶'),
    ('radio', ['ra', 'di', 'o'], '📻'), ('dé', ['dé'], '🎲'), ('robe', ['ro', 'be'], '👗'),
    ('judo', ['ju', 'do'], '🥋'), ('banane', ['ba', 'na', 'ne'], '🍌'), ('café', ['ca', 'fé'], '☕'),
    ('coco', ['co', 'co'], '🥥'),
]

PHRASES = {
    'welcome': "Bonjour ! On va apprendre à lire. Choisis un jeu.",
    'q_sound': "Quelle lettre fait le son",
    'yes': "Oui !",
    'again': "Essaie encore !",
    'tap_loco': "Touche la locomotive.",
    'tap_wagon': "Touche le wagon.",
    'link': "Accroche le wagon !",
    'q_syl': "Trouve",
    'read_word': "Lis le mot, puis touche la bonne image.",
    'build': "Construis le mot",
    'newsounds': "Bravo ! Tu as gagné de nouveaux sons ! Touche-les pour les écouter.",
    'first': "Voici tes premiers sons. Touche-les pour les écouter.",
    'locked': "Encore un peu de sons à apprendre, et ce jeu va s'ouvrir !",
    'p0': "Bravo !", 'p1': "Super !", 'p2': "Génial !", 'p3': "Bien joué !", 'p4': "Youpi !", 'p5': "Tu lis comme un grand !",
}


def gparse(s):
    out, i = [], 0
    while i < len(s):
        if s[i:i+2] == 'ch':
            out.append('ch'); i += 2
        else:
            out.append(s[i]); i += 1
    return out


def build_data():
    G = {g['g']: g for g in GRAPHEMES}
    vowels = [g for g in GRAPHEMES if g['v']]
    cons = [g for g in GRAPHEMES if not g['v']]
    syls = {}
    for c in cons:
        for v in vowels:
            if c['g'] in ('c', 'g') and v['g'] in ('e', 'i', 'é'):
                continue
            s = c['g'] + v['g']
            syls[s] = dict(s=s, g=[c['g'], v['g']], ph=c['ph'] + v['ph'], lvl=max(c['lvl'], v['lvl']))
    for v in vowels:
        syls[v['g']] = dict(s=v['g'], g=[v['g']], ph=v['ph'], lvl=v['lvl'], solo=True)
    words = []
    for w, ss, e in WORDS:
        for s in ss:
            if s not in syls:
                gs = gparse(s)
                syls[s] = dict(s=s, g=gs, ph=''.join(G[x]['ph'] for x in gs), lvl=max(G[x]['lvl'] for x in gs), extra=True)
        lvl = max(syls[s]['lvl'] for s in ss)
        words.append(dict(w=w, s=ss, e=e, lvl=lvl))
    words.sort(key=lambda x: x['lvl'])
    for g in GRAPHEMES:
        g['cont'] = g['ph'] in CONTINUANTS
    return dict(G=GRAPHEMES, SYL=list(syls.values()), W=words, P=PHRASES)
