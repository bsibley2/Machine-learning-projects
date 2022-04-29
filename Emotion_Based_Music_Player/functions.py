import numpy as np
import pretty_midi
from collections import Counter


def generate_sequence(chord: str, data, emotion, length: int = 30) -> object:
    """Generate sequence of defined length."""
    # create list to store future chords
    chords = [chord]
    for n in range(length):
        emotionbi = emotion.copy()
        possibilities = []
        z = 0
        for i in data:
            y = predict_next_state(chord, i)
            if not y:
                x = emotionbi.pop(z)
                emotionbi = [float(value) / (1 - x) for value in emotionbi]
                continue
            else:
                possibilities.append(y)
                z = z + 1
        if not possibilities:
            next_chord = chord
        else:
            next_chord = np.random.choice(possibilities, p=emotionbi)
        chords.append(next_chord)
        # use last chord in sequence to predict next chord
        chord = chords[-1]
    return chords


def predict_next_state(chord: str, data: list):
    """Predict next chord based on current state."""
    # create list of bigrams which stats with current chord
    bigrams_with_current_chord = [bigram for bigram in data if bigram.split(' ')[0] == chord]
    # check if there are bigrams
    if not bigrams_with_current_chord:
        y = []
    else:
        # count appearance of each bigram
        count_appearance = dict(Counter(bigrams_with_current_chord))
        # convert apperance into probabilities
        for ngram in count_appearance.keys():
            count_appearance[ngram] = count_appearance[ngram] / len(bigrams_with_current_chord)
        # create list of possible options for the next chord
        options = [key.split(' ')[1] for key in count_appearance.keys()]
        # create  list of probability distribution
        probabilities = list(count_appearance.values())

        # return random prediction

        y = np.random.choice(options, p=probabilities)
    return y


def first_chord(emotions):
    firstchords = emotions.iloc[:, 0]
    firstcount = dict(Counter(firstchords))

    probabilities = list(firstcount.values())
    probabilities = [element / len(firstchords) for element in probabilities]
    options = [key.split(' ')[0] for key in firstcount.keys()]

    return np.random.choice(options, p=probabilities)


def create_midi(chords):
    midi_data = pretty_midi.PrettyMIDI()
    piano_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')
    piano = pretty_midi.Instrument(program=piano_program)
    length = 1
    for n, chord in enumerate(chords):
        for note_name in chord.components_with_pitch(root_pitch=4):
            note_number = pretty_midi.note_name_to_number(note_name)
            note = pretty_midi.Note(velocity=100, pitch=note_number, start=n * length, end=(n + 1) * length)
            piano.notes.append(note)
    midi_data.instruments.append(piano)
    return midi_data

    
