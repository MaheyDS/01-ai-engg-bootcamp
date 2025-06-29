# AI Engineering Bootcamp - Multi-Provider Chatbot

A modern Streamlit-based chatbot application that supports multiple LLM providers including OpenAI, Groq, and Google Gemini. This project demonstrates how to build a unified interface for different AI models with configurable parameters.

## 🚀 Features

- **Multi-Provider Support**: Switch between OpenAI, Groq, and Google Gemini models
- **Real-time Chat Interface**: Built with Streamlit for an intuitive user experience
- **Configurable Parameters**: Adjust temperature and max tokens for response control
- **Docker Support**: Easy deployment with containerization
- **Environment-based Configuration**: Secure API key management

## 📋 Prerequisites

- Python 3.12 or higher
- Docker (optional, for containerized deployment)
- API keys for your chosen providers:
  - OpenAI API key
  - Groq API key  
  - Google Gemini API key

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd 01-ai-engg-bootcamp
```

### 2. Install Dependencies

The project uses `uv` for dependency management. Install dependencies with:

```bash
uv sync
```

**Alternative (if not using uv):**
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the project root with your API keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

## 🏃‍♂️ Running Locally

### Option 1: Using Make (Recommended)

```bash
make run-streamlit
```

### Option 2: Direct Streamlit Command

```bash
streamlit run src/chatbot-ui/streamlit_app.py
```

The application will be available at:
- **Local URL**: http://localhost:8501
- **Network URL**: http://your-ip:8501

## 🐳 Running with Docker

### 1. Build the Docker Image

```bash
make build-docker-streamlit
```

### 2. Run the Container

```bash
make run-docker-streamlit
```

**Note**: If port 8501 is already in use, you can modify the port mapping in the Makefile or run directly:

```bash
docker run -v "$(PWD)/.env:/app/.env" -p 8502:8501 streamlit-app:latest
```

Then access the app at http://localhost:8502

## 🎛️ Usage

1. **Select Provider**: Choose between OpenAI, Groq, or Google from the sidebar
2. **Choose Model**: Select your preferred model for the chosen provider
3. **Adjust Parameters**:
   - **Temperature**: Controls randomness (0.0 = deterministic, 1.0 = creative)
   - **Max Tokens**: Limits response length
4. **Start Chatting**: Type your message and press Enter

## 📁 Project Structure

```
01-ai-engg-bootcamp/
├── src/
│   └── chatbot-ui/
│       ├── core/
│       │   └── config.py          # Configuration management
│       └── streamlit_app.py       # Main Streamlit application
├── notebooks/                     # Jupyter notebooks for exploration
├── Dockerfile                     # Docker configuration
├── Makefile                      # Build and run commands
├── pyproject.toml                # Project dependencies
└── .env                          # Environment variables (create this)
```

## 🔧 Configuration

### Supported Models

- **OpenAI**: `gpt-4o-mini`, `gpt-4o`
- **Groq**: `llama-3.3-70b-versatile`
- **Google**: `gemini-2.0-flash`

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key | For OpenAI models |
| `GROQ_API_KEY` | Groq API key | For Groq models |
| `GOOGLE_API_KEY` | Google Gemini API key | For Google models |

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using port 8501
   lsof -i :8501
   # Kill the process or use a different port
   ```

2. **API Key Errors**
   - Ensure your `.env` file exists and contains valid API keys
   - Verify API keys have sufficient credits/permissions

3. **Docker Mount Issues**
   - Ensure the `.env` file exists in the project root
   - Check Docker Desktop file sharing settings on macOS

4. **Google API Errors**
   - Verify you're using the correct Google Generative AI library version
   - Check API quotas and billing status

### Performance Optimization

For better performance, install the Watchdog module:
```bash
pip install watchdog
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Streamlit for the amazing web framework
- OpenAI, Groq, and Google for their LLM APIs
- The AI engineering community for inspiration and support