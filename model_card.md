# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**Follow 1.0**

---

## 2. Intended Use  

Follow is a classroom demo, not a product built for real users. It takes a small, fixed catalog of songs and a stated taste profile (favorite genre, favorite mood, a target energy number, and an acoustic preference), and returns a ranked shortlist with a plain-language reason for each pick.

It assumes the user can hand it a precise, structured description of their taste — an exact favorite genre as a single word, an exact favorite mood as a single word, and a specific energy number between 0 and 1. Real listeners don't actually think in these terms; someone would more likely say "something to study to" than "genre=lofi, mood=chill, energy=0.35." That gap between how the model expects input and how people actually describe music is itself a limitation worth keeping in mind (see Section 6).

---

## 3. How the Model Works  

Think of it like a matchmaking scorecard: every song gets compared against the user's stated taste on four categories, and the points from each category are added into one total score.

- **Genre match** is worth the most (2.0 points) — if the genre is wrong, nothing else matters much.
- **Mood match** is worth 1.5 points.
- **Energy closeness** is worth up to 1.0 point, and it's not all-or-nothing — the closer the song's energy is to what the user asked for, the more of that point it earns.
- **Acoustic bonus** is worth up to 1.0 point, but only if the user actually said they like acoustic songs. If they didn't say that, this category is skipped — it neither helps nor hurts.

All songs in the catalog get scored this way, then they're sorted highest to lowest and the top few are returned, each with a short explanation of which categories it scored on.

The starter file had none of this implemented — every function was a placeholder that returned an empty result or a fixed dummy string. This scoring rule, and sharing one scoring function between the two interfaces the starter code exposed (a dictionary-based one and a class-based one), is what was actually built.

---

## 4. Data  

The catalog (`data/songs.csv`) has 10 songs, unchanged from the starter data.

- **Genres represented (7):** pop, lofi, rock, ambient, jazz, synthwave, indie pop — lofi has the most entries (3 songs), pop has 2, everything else has just 1.
- **Moods represented (6):** happy, chill, intense, relaxed, moody, focused — chill has the most entries (3 songs).
- **Artists:** 8 unique artists across 10 songs; 2 of them (Neon Echo, LoRoom) appear twice, everyone else appears once. This uneven coverage matters — see Section 6.
- **Missing from this dataset:** lyrics/language, cultural or regional style, release era, and popularity — the model has no way to know if a song is a deep cut or a hit, or what language it's sung in.

---

## 5. Strengths  

Follow feels most reliable for a listener with a relaxed, "artsy"/introspective taste — someone who wants something chill and low-key to unwind to. This matches what the lofi/chill experiment showed: a user asking for `genre=lofi, mood=chill, energy=0.35, likes_acoustic=True` got back songs that were genuinely lofi, genuinely chill, and genuinely high on acoustic sound (*Library Rain*, *Midnight Coding*) — all four scoring categories agreed with each other, so the result matched intuition well.

---

## 6. Limitations and Bias 

- **Tiny catalog.** With only 10 songs, a user whose real taste isn't represented at all (e.g. "heavy metal + sad") simply can't be satisfied — and in a real product, an unsatisfied user is likely to just go try a competing app instead of sticking around.
- **Unused features.** Tempo, valence, and danceability are stored per song but never factored into the score. This specifically shortchanges anyone who picks music by rhythm or danceability — they can get a recommendation that matches on genre and mood but still doesn't fit the way they actually chose it.
- **No "I don't have a good match" case.** When nothing in the catalog fits (see the hiphop experiment in the README), the system still confidently returns a ranked top 5 instead of admitting it. That can make a user feel like the system "doesn't get them" — the same trust/churn risk as the tiny-catalog problem.
- **Uneven catalog coverage as a concrete bias example.** Two artists (Neon Echo, LoRoom) have 2 songs each while everyone else has only 1. Even with completely fair, unbiased scoring math, those two artists simply have twice the chance of landing in someone's top 5 purely because they take up more of the catalog. This is a good illustration of a bias that comes from the *data*, not from the scoring logic itself — the algorithm can be "fair" and still produce an unfair outcome if what it's fed is unbalanced.

---

## 7. Evaluation  

Four user profiles were run through the recommender and the results were read by hand (no numeric metrics beyond the score itself):

1. `genre=pop, mood=happy, energy=0.8` (the starter profile in `main.py`) — top pick matched on genre, mood, and energy all at once.
2. `genre=lofi, mood=chill, energy=0.35, likes_acoustic=True` — top picks were genuinely lofi/chill/acoustic (see Strengths).
3. `genre=rock, mood=intense, energy=0.9` — the one rock song in the catalog won by a wide margin, which turned out to just mean "the only option," not "a great option."
4. `genre=hiphop, mood=energetic, energy=0.6` (a genre/mood combination that doesn't exist anywhere in the catalog) — scores collapsed to just the energy term and the system still returned a confident-looking top 5 (see Limitations).

Nothing about this was surprising — the results matched what you'd expect from reading the scoring rule (Section 3) directly. The value of running it wasn't discovering a surprise, it was confirming the scoring rule does what it's supposed to and turning case #4 into a permanent automated test (`test_recommend_degrades_gracefully_when_no_genre_or_mood_match`) so that behavior is tracked on purpose instead of by accident.

---

## 8. Future Work  

The main idea to pursue next: when there's no strong match for what the user asked for, don't force a confident-looking ranked list out of a weak signal (Section 6). Instead, fall back to recommending well-known/popular songs in the genre the user actually searched for — that turns an "I have to guess" situation into an honest "here's what's popular in what you asked for" answer, which should feel more trustworthy than a top 5 that's really just noise.

---

## 9. Personal Reflection  

Building Follow reinforced for me that a good product has to be centered on what the user actually wants deep down — not just whatever fixed labels they're able to hand you — and it has to account for how diverse and varied those real wants are, instead of assuming one narrow set of categories fits everyone. Working through this project also left me more excited, not less, about applying recommender-style thinking to other fields and scenarios beyond music.
