FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "main.py"]

# Build the image using command: docker build . -t pokeapi-game
# Run the image in interactive mode using command: docker run -it pokeapi-game