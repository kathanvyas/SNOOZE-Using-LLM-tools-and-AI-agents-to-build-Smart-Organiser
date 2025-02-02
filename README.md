# SNOOZE: Smart Notification and Optimised Organiser with Zero Effort

## Overview
SNOOZE is an AI-powered personal assistant designed to facilitate various tasks such as document querying, scheduling meetings, and sending emails. It leverages advanced language models and a retrieval-augmented generation (RAG) approach to provide intelligent responses based on user input and uploaded documents.

*Click to access the presentation that explains SNOOZE*

[![Access Presentation](https://img.youtube.com/vi/Kf9k9Xnn4jw/0.jpg)]([https://youtu.be/Kf9k9Xnn4jw](https://docs.google.com/presentation/d/1ZfYWNVLsh5n6_DQvPbV08IzMxdM3Hlc3/edit?usp=sharing&ouid=113974454502710491743&rtpof=true&sd=true))


## Snapshots
Here are some demo videos of the SNOOZE application:
[![Watch the video](https://img.youtube.com/vi/pJIweJ_txu4/0.jpg)](https://www.youtube.com/watch?v=pJIweJ_txu4)

*Click to watch the video of the email-sending feature*

[![Watch the video](https://img.youtube.com/vi/Kf9k9Xnn4jw/0.jpg)](https://youtu.be/Kf9k9Xnn4jw)



*Snapshot of the document query feature*

## Features
- **Chat Interface**: Users can interact with the AI assistant through a user-friendly chat interface.
- **Document Uploading**: Users can upload multiple PDF documents for the assistant to query and extract information from.
- **Intent Detection**: The system can detect user intents such as scheduling meetings, sending emails, or performing internet searches.
- **Email and Calendar Integration**: The assistant can send emails and schedule meetings, create calendar events using integrated tools. It can also update or delete the existing meetings/calendar events.
- **Dynamic Responses**: The assistant generates responses based on the context of the conversation and the uploaded documents.

## Architecture
The QuickMind application is divided into two main components: the Streamlit frontend and the backend API.

### Streamlit Frontend
The frontend is built using Streamlit, a powerful framework for creating web applications in Python. Key functionalities include:
- **User Interface**: The UI allows users to upload documents, select model types, and interact with the assistant.
- **Session State Management**: The application maintains the state of user interactions, including messages and uploaded documents.
- **Chat Functionality**: Users can send messages to the assistant, which processes the input and returns responses based on the context.

### Backend API
The backend is built using FastAPI, providing a robust API for handling requests from the frontend. Key functionalities include:
- **File Uploading**: The API allows users to upload PDF files, which are stored for later querying.
- **Chat Processing**: The backend processes chat messages, invoking the appropriate models and tools based on user intents.
- **Integration with Langchain**: The backend utilizes Langchain for document loading, text splitting, and embedding, enabling efficient retrieval of information from uploaded documents.

**Note**: For the local model to work, ensure that Ollama is running in the background with the Llama 3.2 model pulled.
### API Endpoints
The following API endpoint is used in the application:

- **`/chat/stream`**: This endpoint handles chat interactions between the user and the assistant.

### Langgraph Work Flow
![Snapshot 3](backend/graph.jpeg) \
*Graph Workflow*


## Tech Stack
The QuickMind application utilizes the following libraries and technologies:
- **Streamlit**: For building the frontend web application.
- **FastAPI**: For creating the backend API.
- **Langchain**: For language model integration and document processing.
- **LangGraph**: For managing graph workflows and enhancing data processing capabilities.
- **Poetry**: For dependency management and packaging in Python.

## Installation
To set up the QuickMind application, follow these steps:

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd quickmind
   ```

2. Set up the backend:
   - Navigate to the `backend` directory. Run the setup script to configure the environment and connect to Google Calendar and Gmail. 
     ```bash
        cd backend
        source setup.sh
     ```
   - setup.sh does the following
     - create a virtual python environment (Note: use python3.11 or above since all the libraries downloaded are using this version)
     - install composio to connect to google calendar and gmail
     - install libraries using poetry
     - Add google calendar and gmail tool (This asks for google auth)
   - ## Environment Setup
   - copy the .env.example to .env and assign all the api keys
     ```
     cp .env.example > .env
     ```
     This will copy all the environment variables to .env from which the API keys will be exported by the backend server
   - Make sure you run the following to load the env file by poetry
     ```
     poetry self add poetry-dotenv-plugin
     ```
   - Set all the below environment variables given below for the backend to work
      ```
        # ------------------LangSmith tracing------------------
        LANGCHAIN_API_KEY=your-langchain-api-key
        LANGCHAIN_CALLBACKS_BACKGROUND=true
        LANGCHAIN_TRACING_V2=false
        LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
        LANGCHAIN_PROJECT="your-project-name"
        # -------------------Tools & Model API KEYS----------------------------------
        OPENAI_API_KEY=your-openai-api-key
        GOOGLE_CSE_ID=your-custom-search-engine-id
        GOOGLE_API_KEY=your-google-search-api-key
        COMPOSIO_API_KEY=your-composio-key
      ```
    To generate API Keys:
    - visit: https://app.composio.dev/ and login to get your API key
    - visit: https://console.cloud.google.com/apis/dashboard and login to get your API key for google search
    - visit: https://programmablesearchengine.google.com/controlpanel/all to get your CSE ID
    - visit: https://platform.openai.com/ and login to get your openai API key
    - visit: https://smith.langchain.com/ and login to get your lanchain API key. (visit settings to find the api key generator)

3. Set up the frontend:
   - Navigate to the `streamlit` directory and install dependencies:
     ```bash
     cd streamlit
     pip install -r requirements.txt
     ```
  - ## Environment Setup
       ```
        cp .env.example > .env
       ```
       - Assign the open ai api key in the .env file as shown below
       ```
        OPENAI_API_KEY=Your-OpenAI-API-Key
       ```


4. Run the backend server:
   ```bash
   cd backend
   poetry run start
   ```

5. Run the Streamlit application:
   ```bash
   cd streamlit
   streamlit run chat_bot.py
   ```

## Usage
- **Uploading Documents**: Use the sidebar to upload PDF documents that the assistant can query.
- **Interacting with the Assistant**: Type your questions or commands in the chat input area and receive responses based on the context and uploaded documents.
- **Model Selection**: Choose between different AI models (e.g., OpenAI, Llama) to customize the assistant's behavior.


## Errors and Debugging
If you come accross this error while downloading packages for streamlit app the solution is given below
```
TypeError: Descriptors cannot be created directly. If this call came from a _pb2.py file, your generated code is out of date and must be regenerated with protoc >= 3.19.0. If you cannot immediately regenerate your protos, some other possible workarounds are: 1. Downgrade the protobuf package to 3.20.x or lower. 2. Set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python (but this will use pure-Python parsing and will be much slower). More information: https://developers.google.com/protocol-buffers/docs/news/2022-05-06#python-updates
```
Solution:
```
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
```
## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments
- [Streamlit](https://streamlit.io/) for the web application framework.
- [FastAPI](https://fastapi.tiangolo.com/) for the backend API.
- [Langchain](https://langchain.com/) for the language model integration and document processing.
- [LangGraph](https://www.langchain.com/langgraph) for building agents that reliably handle complex tasks.

