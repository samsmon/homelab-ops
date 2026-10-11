#!/usr/bin/env python3
import os

BASE_DIR = "/mnt/hdd-backup/music/Lossless"

print("=== CHECKING ALL ARTISTS IN Anime/ (excluding verified franchises) ===")
known_anime = [
    "100 Kanojo", "Bad Girl", "Bakupuri Channel", "BanG Dream!", "Bocchi the Rock!",
    "D4DJ", "DATE WARS", "Denonbu", "Fate", "Girls Band Cry", "Girls und Panzer",
    "Gochuumon Wa Usagi Desu Ka", "Gotoubun no Hanayome", "Healer Girl", "Hitoribocchi",
    "HoneyWorks", "Iroawase", "Just Because!", "Love Live!", "Love4", "Lucky Star",
    "Lycoris Recoil", "MILGRAM", "Macross Delta", "Maebashi Witches", "Makeine", "Maou 2099",
    "Megami no Cafe Terrace", "Mitsuboshi Colors", "Monogatari", "NEW GAME!", "Narenare",
    "ORESUKI", "Oshi no Ko", "PINKISH!!!!", "Pole Princess!!", "Princess Session Orchestra",
    "Revue Starlight", "SAO", "SYNDUALITY", "Shinmai Ossan Boukensha", "Slow Loop",
    "Sound! Euphonium", "Spice and Wolf", "Swing, Sing", "THE IDOLM@STER", "Tamayura",
    "Ultraman Arc", "Uma Musume", "Uta no Princess-sama", "Utagoe wa Mille-Feuille",
    "Utahime Dream", "Vivy -Fluorite Eye's Song-", "World Dai Star",
    "Yoru no Kurage wa Oyogenai", "Yuru Camp", "iMarine Project", "2.5 Jigen no Ririsa",
    "Ayakashi Triangle", "Giji Harem", "Isekai Yururi Kikou", "Kono Sekai wa Fukanzensugiru",
    "Maou Gakuin no Futekigousha", "Mato Seihei no Slave", "Mayonaka Punch", "Nige Jouzu no Wakagimi",
    "NieR Automata", "Onimai", "Re Zero", "Senpai wa Otokonoko", "Tate no Yuusha no Nariagari",
    "Tensura", "Tsue to Tsurugi no Wistoria"
]

anime_dir = os.path.join(BASE_DIR, "Anime")
for item in sorted(os.listdir(anime_dir)):
    if not any(k.lower() in item.lower() for k in known_anime):
        print(f"  Uncategorized in Anime: {item}")
