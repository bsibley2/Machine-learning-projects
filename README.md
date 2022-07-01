# Machine-learning-projects
    Here you can find a few of projects I've completed.
    
    In the master branch there is small robotics project in which I attempt to use reinforcement learning to teach a virtual robotic arm to reach a certain fixed point on the screen (which is updated after each episode). This project consists of four main files and uses the libraries Open cv, AI gym, and Stable Baselines 3. The file robot pose.py controls the three servos of the virtual arm. The file mask_and_centroid_functions.py defines two functions, one of which creates a mask to locate the gripper of the virtual arm (represented on the screen by a blue disk), and the other of which uses this mask to find the coordinates for the centre of this disk. The main gym environment is contained in the class written in the file robot_arm_gym_environment.py. Using a webcam pointed at the screen displaying the virtual arm, this class uses Open cv together with the aforementioned functions to find the centre of the gripper (represented by a small black square placed on the gripper), creates the target (represented by a small red dot) and calculates a reward function based on the distance from the target. The soft actor-critic agent (represented by the virtual arm) is created in the file SAC_agent.py. The file VirtualRobotArm.py (written by Denis Steckelmacher), creates a pygame window displaying the virual arm. 
    
    There are three projects in the main branch. The first project is an end-to-end machine learning project,
    and the second is a spam filter analysis. The data sets are taken from the UCI machine learning repository.
    
    
    
    In the folder Emotion_Based_Music_Player you will also find a project I have made in collaboration with Arne Pais, Fabien Van de Velde, and Tom Oostvogels.
    This is an AI interface intended to capture the emotions of a user and play music according to his or her emotion. When run, a web based user interface appears 
    and allows the user to either input a photo or to make a live video recording. In the former case the program will analyse the emotions in the photo and then the
    user will have the option of playing a preselected piece of music based on his or her dominant emotion, or have an AI generated tune played based on all the emotions
    displayed, where the emotions are weighted according to the degree to which they appear. Emotions are detecting using the DeepFace library available in Python. The
    web interface has been made using streamlit, and is partly based on that of the project https://github.com/Mohammad-juned-khan/Face-detection-analysis-application.
    The CSV files contain chord sequences used to by the program in the file generator.py to generate a song based on the emotional input. The idea here is also partly 
    based on the article https://towardsdatascience.com/markov-chain-for-music-generation-932ea8a88305.
    
    
