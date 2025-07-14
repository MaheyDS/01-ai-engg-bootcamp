run-streamlit:
	streamlit run src/chatbot_ui/streamlit_app.py

build-docker-streamlit:
	docker build -t streamlit-app:latest .

run-docker-streamlit:
	docker run -v "$(PWD)/.env:/app/.env" -p 8501:8501 streamlit-app:latest

clean-notebooks-outputs:
	jupyter nbconvert --clear-output --inplace notebooks/*.ipynb

run-docker-compose:
	docker compose up --build

run-evals:
	uv sync
	PYTHONPATH=src uv run --env-file .env python -m evals.eval_retriever