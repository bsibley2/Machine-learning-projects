# import the necessary libraries
import numpy as np
import streamlit as st
import cv2
import os
import av
from deepface import DeepFace as dfc
from PIL import Image
from image_functions import face_detect, analyse_image, detect_web 
import generator
from generator import generator, generateaudio
from functions import create_midi
import sounddevice as sd



# Here we define the main function of the application. It creates a menu with three options. The "home" option just gives some basic information about the project. The second option prompts the user to upload a photo. This is photo is analysed using the Deep Face library. The user can then use this data to generate a song. The third option is video. Here the user's emotion is directly analysed (again using Deep Face) and his dominant emotion is extracted. The option is then given to play a piece of classical music according to the emotion expressed.#

def main():
    
     # html content
    st.markdown("""
    <h1>Emotion-Based Music Player</h1>
    """, unsafe_allow_html=True)
    # css styling
    st.markdown(""" 
    <style>
    .css-fk4es0 {background-image: linear-gradient(90deg, rgb(118, 50, 63), rgb(238, 210, 185))}
    .css-1xfuh55 {fill: #76323f;}
    .css-1jkb0cp {background: none;}
    h1 {font-family: cambria; text-align: center; color: #76323f; border-style: outset; background-color: #ebd2b9; border-width: 5px}
    section.main.css-1v3fvcr.egzxvld3 {background-color: #fef8ef; padding: 16px;}
    section.main.css-1v3fvcr.egzxvld3 > div {border-style: solid; border-color: #76323f; margin: 55px 0 0 0; background-color: #d7cec7;}
    #root > div:nth-child(1) > div > div > div > div {background-color: #fef8ef;}
    .css-12oz5g7 {padding: 16px;}
    div.css-1adrfps.e1fqkh3o2 {background-color: #ebd2b9;}
    .st-d9, .st-d8, .st-d7, .st-d6 {border-color: #76323f;}
    .st-bn {border-color: #76323f;}
    #root > div:nth-child(1) > div > div > div > div > section.main.css-1v3fvcr.egzxvld3 > footer {display: None;}
    </style> 
    """, unsafe_allow_html=True)

    # We store the options in a list which is used to create a sidebar from which the user can select his preferred activity.
    options = ["Home", "Upload Photo", "Make Video"]
    choice = st.sidebar.selectbox("Select Activity", options)
    
    # If the user chooses "Home, some basic information about the project is displayed". 
    if choice == "Home":
        # html content
        st.markdown("""
        <div id='intro'>
        <p id='intro_text'>Emotion-based music generation and selection.<br>Facial recognition is done with the DeepFace library, while this web app is developed using Streamlit.</p>
        </div>
        <h2>About the app</h2>
        <p>The application plays music based on the emotional input from the user. Input can take two different forms:</p>
        <ol>
        <li>Pre-selected image data.</li>
        <li>Live Video data.</li>
        </ol>
        <p>In the first case, the image will be analysed and a song will be generated according to the dominant emotion found. In the second case, a piece of classical music that matches the detected emotion will be played.</p>
        <p>You can select one of the options in the sidebar on the right.</p>
        <footer>Emotion Based Music Player by Arne Panis, Benjamin Sibley, Fabian Van de Velde, Tom Oostvogels</footer>
        """, unsafe_allow_html=True)
        # css styling
        st.markdown(""" 
        <style>
        #intro {background-color: None; padding: 12px 3px 0px;} 
        #intro_text {font-size: 1.1rem; font-weight: 900; color: white; text-align: center; margin-bottom: 0;} 
        h2 {padding-top: 0;}
        h2, p {color: #565656}
        ol {list-style-position: inside; font-style: italic; color: #565656}
        footer {color: #565656; font-size: 0.7rem; text-align: right; color: white; font-style: italic;}
        </style> 
        """, unsafe_allow_html=True)

            
    elif choice == "Upload Photo":
        # If the user chooses "Upload Photo", a prompt for him to upload his image appears
        # html content
        st.markdown("""
        <h2>Generate a new song using image data.</h2>
        <p>The uploaded image will be analysed for its dominant emotion and a song will be generated accordingly!</p>
        """, unsafe_allow_html=True)
        # css styling
        st.markdown(""" 
        <style>
        h2, p {color: #565656;}
        </style> 
        """, unsafe_allow_html=True)
        image_file = st.file_uploader("Upload image you want to analyze", type=['jpg', 'png', 'jpeg'])
        
        if image_file is not None:
            # Here we read the image using the PIL library.
            image_loaded = Image.open(image_file)
            #detect faces in image
            result_img, result_face = face_detect(image_loaded)
            st.image(result_img, use_column_width=True)
            st.success("found {} face\n".format(len(result_face)))
            

            # html content
            st.markdown("""
            <h4>Play a premade or randomly composed song</h4>
            <p>Press the first button to play a premade piece of music matching your mood or press the second one to play a randomly composed song matching it!</p>
            """, unsafe_allow_html=True)
            # css styling
            st.markdown(""" 
            <style>
            h4, p {color: #565656;}
            </style> 
            """, unsafe_allow_html=True)
            if st.button("Analyse image and play a piece of music",key=2):  
                # convert image to array
                new_image = np.array(image_loaded.convert('RGB'))
                img = cv2.cvtColor(new_image, 1)
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                #analyse features of face
                result = analyse_image(img)
                # st.write(result)
                # html content
                st.markdown("""
                <h2>Your emotion and song</h2>
                """, unsafe_allow_html=True)
                # css styling
                st.markdown(""" 
                <style>
                h2 {color: #565656; padding: 0;}
                </style> 
                """, unsafe_allow_html=True)
                st.write("Your emotion is ", result["dominant_emotion"], ".")
                st.write("Here is your piece of music.")
                audio_file = open(f'{result["dominant_emotion"]}.mp3', 'rb')
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='mp3')


 
            elif st.button("Analyse image and generate a song"):
                # convert image to array
                new_image = np.array(image_loaded.convert('RGB'))
                img = cv2.cvtColor(new_image, 1)
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                #analyse features of face
                result = analyse_image(img)
                # st.write(result)
                st.write("Your main emotion is ", result["dominant_emotion"], ".")
                st.write("Your song will be generated using the dictionary ", result["emotion"], ".")
                predictions = result["emotion"]
                # Emotions add up to 100 instead of 1
                for key in predictions:
                    predictions[key] = predictions[key] / 100
                # Doesn't add up to 1 (rounding)
                total = predictions['angry'] + predictions['disgust'] + predictions['fear'] + predictions['happy'] + predictions['sad'] + predictions['surprise'] + predictions['neutral']
                # This should be added to an emotion to make it 1
                rest = 1-total
                # Replace value of dominant emotion
                dominant = result["dominant_emotion"]
                predictions[dominant] = predictions[dominant] + rest
                # for testing: D={'angry': .1,'disgust': .1,'fear': 0.05,'happy': 0.5,'sad': .18,'surprise': 0.05,'neutral': .02}
                output_generator = generator(predictions)
                audio = generateaudio(output_generator)
                sd.play(audio, 100000, blocking=False)
                print(audio)
                if st.button("Stop music"):
                    sd.stop()

    elif choice == "Make Video":
        # html content
        st.markdown("""
        <h2>Play music based on video data</h2>
        <p>The app will analyse your face and extract an emotion 5 times, afterwards a piece of music will be played based on the last determined emotion!</p>
        """, unsafe_allow_html=True)
        # css styling
        st.markdown(""" 
        <style>
        h2, p {color: #565656;}
        </style> 
        """, unsafe_allow_html=True)
        run = st.checkbox('Analyse my emotions')
        emotion=[]
        FRAME_WINDOW = st.image([])
        camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        def generate_emotions():
            while run:
                    # Reading image from video stream
                    _, img = camera.read()
                    # Call method we defined above
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    img, a = detect_web(img)
                    # st.image(img, use_column_width=True)
                    FRAME_WINDOW.image(img)
                    live_result = analyse_image(img)
                    st.write(live_result["dominant_emotion"])
                    emotion.append(live_result["dominant_emotion"])
                    if len(emotion) >= 5:
                        break
            return emotion
        
        

        if st.button("Play a piece of music"):
                generate_emotions()
                audio_file = open(f'{emotion[-1]}.mp3', 'rb')
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='mp3')
               
    else:
        pass

if __name__ == '__main__':
    main()