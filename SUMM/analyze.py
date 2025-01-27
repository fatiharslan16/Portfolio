import openai
import os

# Set your OpenAI API key
openai.api_key = "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"
# Function to analyze reviews with ChatGPT
def analyze_reviews_with_chatgpt(file_path):
    # Read reviews from the file
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    with open(file_path, "r") as file:
        reviews = file.readlines()

    # Prepare the prompt
    prompt = f"Here are some customer reviews:\n\n{''.join(reviews)}\n\n"
    prompt += "Summarize these reviews and provide tailored recommendations for improvement."

    # Send the request to OpenAI's ChatGPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant that provides business recommendations based on customer reviews."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500  # Adjust token limit based on the response size
    )

    # Print the summary and recommendations
    print(response["choices"][0]["message"]["content"].strip())

# Run the analysis
if __name__ == "__main__":
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "customer_reviews.txt")
    analyze_reviews_with_chatgpt(desktop_path)
