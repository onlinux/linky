#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
ok = [
    "Ok patron!",
    "Ok, c'est fait!",
    "Voilà, c'est fait",
    "ordre exécuté",
    "c'est bon Chef!",
    "Voilà",
]
responses = [
    "Je vais très bien, merci",
    "ça va bien  merci!",
    "Je m'ennuie un peu, merci quand même",
    "Je suis un peu fatigué",
    "je m'emmerde un peu, et vous",
    "Pas super, j'ai mal dormi",
    "J'ai besoin d'une petite sieste, merci",
    "La grande forme, merci",
    "C'est pas la grande forme, bof!",
    "ça boum du tonnerre",
    "je vais étudier un peu",
    "j'aimerais être un peu tranquille, svp",
    "j'ai besoin d'un peu de sommeil, stp",
    "ça ira mieux demain",
    "j'ai la flemme aujourd'hui",
    "Pas envie de travailler aujourd'hui"
]
volets = {
    "droit":  {"ids": [78], "scene": [1]},
    "gauche": {"ids": [79], "scene": [2]},
    "salon": {"ids": [78, 79], "scene": [1, 2]},
    "cuisine": {"ids": [80], "scene": [6]},
    "chambre de Caro": {"ids": [50], "scene": [9]},
    "chambre de Gaby": {"ids": [48], "scene": [8]},
    "salle de bain": {"ids": [49], "scene": [10]},
    "chambre parentale": {"ids": [47], "scene": [7]},
    "bas": {"ids": [78, 79, 80], "scene": [1, 2, 6]},
    "haut": {"ids": [50, 48, 49, 47], "scene": [7, 8, 9, 10]},
}
lights = {
    "cuisine": {"ids": [32]},
    "salon": {"ids": [89]},
    "la lumière en sel": {"ids": [16]},
    "salle à manger": {"ids": [68]},
    "buanderie": {"ids": [253]},
    "extérieure": {"ids": [21]},
    "vmc":  {"ids": [72]},
    "bas":  {"ids": [68, 16, 89]},
    "les lumières":  {"ids": [21, 32, 16, 68, 89, 253]},
}
switches = {
    "lave-vaisselle": {"ids": [283]},
    "tv-chambre": {"ids": [279]},
    "tv-cuisine": {"ids": [289]},
}
