# Web-Based Voice Assistant

This project is a web-based voice assistant created using Python's Flask framework. It integrates several advanced technologies to provide a seamless user experience. The assistant can recognize speech, generate responses using AI, process images, and convert text to speech.

## Features

- **Speech Recognition (Speech to Text):** Converts spoken language into text.
- **Google GenAI (Generative AI):** Generates human-like responses based on user input.
- **OpenCV (Open Source Computer Vision):** Processes and analyzes visual data.
- **Blip Image Captioning Model:** Generates captions for images.
- **Natural Language Processing (NLP):** Understands and processes human language.
- **ElevenLabs (Text to Speech):** Converts text responses into spoken language.
- **Flask:** The web framework used to develop and deploy the application.

## Installation

To run this project locally, follow these steps:

1. **Clone the repository:** 
   ```bash
   git clone https://github.com/hsynalv/Felix_SesliAsistan.git
   cd web-based-voice-assistant
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
  ```bash
     GOOGLE_GENAI_API_KEY=your_google_genai_api_key
     ELEVENLABS_API_KEY=your_elevenlabs_api_key
  ```
5. Run the Flask application:
  ```bash
     flask run
   ```
## Usage

1. Speech Recognition: Click the microphone button to start speaking. The assistant will transcribe your speech into text.
2. AI Response: The transcribed text is sent to Google GenAI, which generates a response.
3. Image Processing: Comment on the camera snapshot by giving the specified voice command.
4. Text to Speech: The AI-generated response is converted into speech using ElevenLabs.
   
## Screenshots

![a](https://github.com/hsynalv/Felix_SesliAsistan/assets/73330164/31116141-1a97-47b7-b388-8b26a5dbdefc)


## Technologies Used
- Speech Recognition: SpeechRecognition
- Google GenAI: Google GenAI API
- OpenCV: OpenCV!

- Blip Image Captioning Model: BLIP
- NLP: Natural Language Toolkit (NLTK)
- Text to Speech: ElevenLabs
- Flask: Flask

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any changes or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.




