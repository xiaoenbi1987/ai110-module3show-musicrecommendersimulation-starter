# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

**Follow** is a small music recommender: it represents each song as a handful of attributes (genre, mood, energy, tempo, valence, danceability, acousticness) and represents a listener's taste as a short profile (favorite genre, favorite mood, a target energy level, and whether they like acoustic songs). It scores every song in a 10-track catalog against that profile with a weighted scorecard — genre and mood matches count for the most, energy closeness and an acoustic bonus fill in the rest — then returns a ranked shortlist, each pick paired with a plain-language explanation of why it was chosen. It's a classroom demo, not a production recommender: the catalog is tiny and the scoring rule is intentionally simple, so the point of the project is seeing, end to end, how a handful of data points and weights turn into a ranked prediction — and where that approach breaks down (see Limitations and Risks, and the model card).

---

## How The System Works

**Song features.** Each `Song` stores 9 attributes: id, title, artist, **genre** (e.g. pop/lofi/rock), **mood** (e.g. happy/chill/intense), **energy** (0–1, how intense the track feels), tempo (bpm), valence (emotional positivity), danceability, and **acousticness** (0–1, how close it is to unprocessed/acoustic sound). Only 4 of these — genre, mood, energy, acousticness — actually feed into the score right now. Tempo, valence, and danceability are stored but currently unused (see Limitations).

**User profile.** A `UserProfile` stores 4 preferences: favorite genre, favorite mood, a target energy value (a specific number 0–1, not a vague "high/low"), and whether the user likes acoustic songs (True/False).

**Scoring rule.** Think of it like a matchmaking scorecard — a few weighted categories added together:

- Genre matches favorite → **+2.0** (highest weight — wrong genre basically means unlistenable)
- Mood matches favorite → **+1.5**
- Energy closeness to target → up to **+1.0**, scaled down the further the song's energy is from what the user wants
- Acousticness bonus → up to **+1.0**, but only applied if the user says they like acoustic songs; otherwise this term is skipped entirely (no bonus, no penalty)

All four terms are added into one total score, and every recommendation comes with a plain-language explanation of which of these terms fired.

**Choosing recommendations.** Every song in the catalog gets scored this way, then the list is sorted highest-to-lowest and the top `k` (default 5) are returned.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Real output from `python -m src.main`, with the starter profile `genre=pop, mood=happy, energy=0.8`:

```
Top recommendations:

Sunrise City - Score: 4.48
Because: genre matches your favorite (pop); mood matches your favorite (happy); energy 0.82 is close to your target 0.80

Gym Hero - Score: 2.87
Because: genre matches your favorite (pop); energy 0.93 is close to your target 0.80

Rooftop Lights - Score: 2.46
Because: mood matches your favorite (happy); energy 0.76 is close to your target 0.80

Night Drive Loop - Score: 0.95
Because: energy 0.75 is close to your target 0.80

Storm Runner - Score: 0.89
Because: energy 0.91 is close to your target 0.80
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

I tried three different user profiles against the same 10-song catalog to see how the scoring rule behaves:

- **Lofi/chill fan who likes acoustic** (`genre=lofi, mood=chill, energy=0.35, likes_acoustic=True`): the top two results (*Library Rain*, *Midnight Coding*) were genuinely lofi + chill + high acoustic score. This is the case where the system works best, because genre, mood, energy, and acoustic preference all reinforce each other.

- **Rock/intense high-energy fan** (`genre=rock, mood=intense, energy=0.9`): *Storm Runner* won by a wide margin (4.49 vs. 2.47 for second place) — but only because it is the **only rock song in the whole catalog**. A confident-looking top score can just mean "the only option," not "a great option."

- **A genre that doesn't exist in the catalog at all** (`genre=hiphop, mood=energetic, energy=0.6`): with no genre or mood match possible, every song's score collapsed to just the energy-closeness term, and the top 5 scores all landed within 0.78–0.85 of each other. The system still confidently returned a ranked top 5 — it has no way to say "none of these are actually a good match for you." This behavior is now locked in by an automated test (`test_recommend_degrades_gracefully_when_no_genre_or_mood_match`) so it doesn't silently change later.

---

## Limitations and Risks

- **Tiny catalog (only 10 songs).** If a user's real taste (e.g. "heavy metal + sad") isn't represented in the catalog at all, the system can't satisfy them — and an unsatisfied user is likely to just go try a different recommendation app instead of sticking around.

- **Some song data is stored but never used in scoring** (tempo, valence, danceability). This specifically hurts users who care about danceability/rhythm — someone who mainly picks music by "can I dance to this" gets recommendations based only on genre/mood/energy/acousticness, so the result can match on paper (right genre, right mood) while still missing what they actually wanted.

- **The system never admits "I don't have a good match for you."** When nothing in the catalog fits the user's taste (see the hiphop experiment above), it still confidently outputs a ranked top 5 instead of saying so. This can make the user feel like the system "doesn't understand them," which — same as the catalog-size problem — creates a real risk of the user giving up and switching to a competing product instead of trusting the recommendations.

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

Building this made it concrete how a recommender turns raw data into a prediction: it's really just a weighted scorecard. Every song attribute (genre, mood, energy, acousticness) gets compared to what the user said they want, each match is worth a fixed number of points, and the points get added up into one number you can sort by. There's no "understanding" happening — the system doesn't know what a lofi song *is*, it just knows whether a text label matches another text label, and whether two numbers are close together.

The clearest example of where bias creeps in wasn't in the scoring math at all — it was in the data. Two artists (Neon Echo, LoRoom) happen to have 2 songs each in the 10-song catalog while everyone else has 1, so those two artists are simply twice as likely to show up in anyone's top 5, regardless of how "fair" the scoring rule is. That's the same shape of problem real-world recommenders run into: an algorithm can be completely unbiased on paper and still produce skewed results if the underlying catalog/dataset isn't balanced.



