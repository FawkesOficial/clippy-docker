FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install .

RUN useradd -m clippy

USER clippy

CMD ["sh", "-c", "echo \"$CLIP_USERNAME\n$CLIP_PASSWORD\" | clippy --path /CLIP"]
