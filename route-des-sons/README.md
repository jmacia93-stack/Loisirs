# La route des sons

Appli pour apprendre à lire en français (méthode syllabique), thème voitures et trains, pour enfant de 3 ans.

- 6 étapes de sons (a i o m l → … → c g z), l'étape suivante s'ouvre après 15 réussites
- 5 jeux : Les sons · Le train des sons (fusion) · Les syllabes · Lis le mot · Construis le mot
- Espace parents : appui long (1 s) sur ⚙️ pour choisir l'étape ou remettre à zéro
- Voix intégrées, fonctionne hors ligne

## Modifier le contenu
`web/tools/content.py` (sons, mots, phrases) puis `python3 web/tools/build.py` (nécessite piper + voix fr-siwis-medium) → copie `web/index.html` vers `app/src/main/assets/index.html`.
