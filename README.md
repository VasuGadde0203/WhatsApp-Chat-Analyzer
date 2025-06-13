# WhatsApp Chat Analyzer
- This is a Streamlit web app that allows users to upload their WhatsApp chat export and gain rich insights using data analysis, visualizations, sentiment analysis, topic modeling, and more. It supports user-wise as well as overall group analysis.

## Features
- 📈 **Chat Statistics**
  - Total messages, words, media shared, and links shared.

- 🗓 **Timelines**
  - Visualizes chat activity over time (daily/monthly).

- 🔥 **Activity Maps**
  - Busiest day of the week

- **Most active months**
  - Heatmap of message distribution by time of day

- 👥 **Most Active Users**
  - Displays top contributors in a group chat.

- ☁️ **WordCloud**
  - A visual representation of most frequent words (excluding stop words).

- 🗣️ **Common Words**
  - Bar chart of top 20 most used words.

- 😃 **Emoji Analysis**
  - Shows emoji usage statistics and pie chart.

- 🧠 **Sentiment Analysis**
  - Calculates and visualizes daily sentiment trends using TextBlob.

- ⏱ **Average Response Time**
  - Analyzes how long it takes users to respond.

- 🕰️ **Messages by Hour**
  - Time-of-day activity breakdown.

- 📚 **Topic Modeling**
  - Discover hidden themes in chats using LDA (Latent Dirichlet Allocation).

## How to Use
- **Clone this repository:**
  - git clone [https://github.com/your-username/whatsapp-chat-analyzer.git](https://github.com/VasuGadde0203/WhatsApp-Chat-Analyzer.git)
  - cd whatsapp-chat-analyzer

- **Install dependencies:**
  - pip install -r requirements.txt

- **Run the Streamlit app:**
  - streamlit run app.py

- Upload your WhatsApp chat text file (exported from WhatsApp) in the sidebar.

## How to Export WhatsApp Chat
- Open WhatsApp and go to the group or personal chat.
- Tap on the three dots (⋮) → More → Export Chat.
- Choose Without Media.
- Save the .txt file and upload it to this app.

## Technologies Used
- Python
- Pandas, Numpy for data manipulation
- Matplotlib, Seaborn, Plotly for visualizations
- TextBlob for sentiment analysis
- Sklearn (LDA) for topic modeling
- Streamlit for web interface

## File Structure
.
├── app.py               # Main Streamlit app
├── helper.py            # Utility functions for analysis
├── preprocessor.py      # Parses and cleans raw WhatsApp data
├── stop_hinglish.txt    # Hinglish stop words for NLP cleaning
└── requirements.txt     # Python dependencies

## Notes
- Currently supports WhatsApp exported chats in English or Hinglish.
- Chat must be in default WhatsApp format (DD/MM/YYYY, HH:MM AM/PM - User: Message).
- Best used for group chats or active one-on-one conversations.

## Some Screenshots 
![image](https://github.com/user-attachments/assets/bb184d49-4d8d-491c-9183-6e5400e5cdfe)
![image](https://github.com/user-attachments/assets/828dcec1-8db6-4f15-ba58-915c53a626e0)
![image](https://github.com/user-attachments/assets/915fc321-3fd0-496f-a430-1e972e8aab57)

## Contributing
- Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change or improve.

