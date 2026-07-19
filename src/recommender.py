import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.5
ENERGY_WEIGHT = 1.0
ACOUSTIC_WEIGHT = 1.0


def _score(
    genre: str,
    mood: str,
    energy: float,
    acousticness: float,
    favorite_genre: str,
    favorite_mood: str,
    target_energy: float,
    likes_acoustic: bool,
) -> Tuple[float, List[str]]:
    """
    Single scoring rule shared by both the dict-based (score_song) and
    dataclass-based (Recommender) recommendation paths.
    """
    total = 0.0
    reasons: List[str] = []

    if genre == favorite_genre:
        total += GENRE_WEIGHT
        reasons.append(f"genre matches your favorite ({genre})")

    if mood == favorite_mood:
        total += MOOD_WEIGHT
        reasons.append(f"mood matches your favorite ({mood})")

    energy_closeness = max(0.0, 1 - abs(energy - target_energy))
    total += energy_closeness * ENERGY_WEIGHT
    reasons.append(f"energy {energy:.2f} is close to your target {target_energy:.2f}")

    if likes_acoustic:
        total += acousticness * ACOUSTIC_WEIGHT
        reasons.append(f"you like acoustic songs and this one scores {acousticness:.2f}")

    return total, reasons


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = [
            (song, _score(
                song.genre, song.mood, song.energy, song.acousticness,
                user.favorite_genre, user.favorite_mood, user.target_energy, user.likes_acoustic,
            )[0])
            for song in self.songs
        ]
        scored.sort(key=lambda pair: pair[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, reasons = _score(
            song.genre, song.mood, song.energy, song.acousticness,
            user.favorite_genre, user.favorite_mood, user.target_energy, user.likes_acoustic,
        )
        if not reasons:
            return "No strong matches with your taste profile."
        return "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    numeric_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            for field in numeric_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    return _score(
        song["genre"], song["mood"], song["energy"], song["acousticness"],
        user_prefs.get("genre"), user_prefs.get("mood"), user_prefs.get("energy", 0.5),
        user_prefs.get("likes_acoustic", False),
    )

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    scored.sort(key=lambda triple: triple[1], reverse=True)
    return [
        (song, score, "; ".join(reasons) if reasons else "No strong matches with your taste profile.")
        for song, score, reasons in scored[:k]
    ]
