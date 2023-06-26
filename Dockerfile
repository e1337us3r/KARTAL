# Use the huggingface/transformers-pytorch-gpu base image
FROM huggingface/transformers-pytorch-gpu:latest

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire folder to the container
COPY . .
