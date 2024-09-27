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

# Expose port
EXPOSE 5000

# Startup command
CMD ["npm", "run", "dev"]