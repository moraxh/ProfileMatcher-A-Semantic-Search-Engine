# Base image for the project
FROM node:18

# Set the working directory
WORKDIR /app

# Copyt files
COPY package*.json ./
RUN npm install
COPY . .

# Install nodemon
RUN npm instal --save-dev nodemon

# Insall pip
RUN apt-get update && apt-get install -y python3 python3-venv python3-pip

# Create Virtual Environment
RUN python3 -m venv /venv

# Install python dependencies in virtual environment
RUN /venv/bin/pip3 install --no-cache-dir -r python/requirements.txt

# Expose port
EXPOSE 5000 5001

# Startup command
CMD ["sh", "-c", "npm run dev & /venv/bin/python3 /app/python/main.py"]