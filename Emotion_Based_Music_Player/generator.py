import pandas as pd
import numpy as np
from pychord import Chord
import pretty_midi
import IPython
from IPython.display import Audio
from functions import first_chord, predict_next_state, generate_sequence,create_midi

def generator(predictions):
    # Create the Emotion array used in all the calculations

    Emotion = [predictions['angry'], predictions['disgust'], predictions['fear'],
               predictions['happy'], predictions['neutral'], predictions['sad'],
               predictions['surprise']]
    # Read the CSV files for each emotion

    emo1 = pd.read_csv('Angry.csv', sep=";")
    emo2 = pd.read_csv('Disgust.csv', sep=";")
    emo3 = pd.read_csv('Fear.csv', sep=";")
    emo4 = pd.read_csv('Happy.csv', sep=";")
    emo5 = pd.read_csv('Neutral.csv', sep=";")
    emo6 = pd.read_csv('Sad.csv', sep=";")
    emo7 = pd.read_csv('Surprise.csv', sep=";")

    # Select a first possible chord for each emotion based on their occurences for that emotion using the first_chord
    # function

    angry = first_chord(emo1)
    disgust = first_chord(emo2)
    fear = first_chord(emo3)
    happy = first_chord(emo4)
    neutral = first_chord(emo5)
    sad = first_chord(emo6)
    surprise = first_chord(emo7)

    # combine the options into one array
    firstoptions = [angry, disgust, fear, happy, neutral, sad, surprise]
    # Select the first chord based on the chances of each emotion happening
    firstchord = np.random.choice(firstoptions, p=Emotion)

    # Create the empty working arrays for all the bigrams
    angrybi = []
    disgustbi = []
    fearbi = []
    happybi = []
    neutralbi = []
    sadbi = []
    surprisebi = []

    z = 0
    for i in [emo1, emo2, emo3, emo4, emo5, emo6, emo7]:
        bigrams1 = []
        for j in range(len(i)):
            n = 2
            chords = i.iloc[j].values
            cleanedchords = [x for x in chords if str(x) != 'nan']
            ngrams = zip(*[cleanedchords[e:] for e in range(n)])

            bigrams = [" ".join(ngram) for ngram in ngrams]
            bigrams1.extend(bigrams)

        if z == 0:
            angrybi = bigrams1
        elif z == 1:
            disgustbi = bigrams1
        elif z == 2:
            fearbi = bigrams1
        elif z == 3:
            happybi = bigrams1
        elif z == 4:
            neutralbi = bigrams1
        elif z == 5:
            sadbi = bigrams1
        elif z == 6:
            surprisebi = bigrams1
        z = z + 1
    bigramscombined = [angrybi, disgustbi, fearbi, happybi, neutralbi, sadbi, surprisebi]
    chords = generate_sequence(firstchord, bigramscombined, Emotion)
    return chords


freq = 44100  # audio CD quality
bitsize = -16  # unsigned 16 bit
channels = 2  # 1 is mono, 2 is stereo
buffer = 1024  # number of samples


def generateaudio(chords):
    """
    Input is a list of chords, in string format.
    This function then generates audio, and it displays this audio as output.

    Parameters
    ----------
    chords : TYPE
        DESCRIPTION.

    Returns
    -------
    audio : TYPE
        DESCRIPTION.

    """
    chordsreal = [Chord(c) for c in chords]
    chords_midi = create_midi(chordsreal)
    audio_data = chords_midi.synthesize() # this format can be played using IPython.display.Audio
    audio = IPython.display.Audio(audio_data, rate=32000)
    return audio_data
