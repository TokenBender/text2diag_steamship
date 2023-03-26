from steamship import Steamship
import re

# Create a Steamship client
# NOTE: When developing a package, just use `self.client`
client = Steamship(workspace="gpt-4_chat_v1")

# Create an instance of this generator
generator = client.use_plugin('gpt-4')

while True:
    # Ask for user input
    print("Assistant Ready>>")
    user_input = input("Enter input: ").strip()

    # Check for empty input
    if not user_input:
        print("Please provide some input.")
        continue

    # Create the prompt
    prompt = f"System: Using mermaid.js, create a diagram that shows the entities involved, the transactions between them, and the events that occur during the process of {user_input}. Please provide a high-level overview of the process and highlight any important decision points or outcomes. Reply only with mermaid.js code and no description or explanation. However, you can silently think step-by-step. Enclose your answer with __begin__ and __end__ tag. The diagram type should be automatically selected based on the task."

    # Generate text
    task = generator.generate(text=prompt)

    # Wait for completion of the task.
    task.wait()

    # Get the mermaid code from the response
    mermaid_code_match = re.search(r"```mermaid([\s\S]*)```", task.output.blocks[0].text)

    if mermaid_code_match:
        mermaid_code = mermaid_code_match.group(1).strip()

        # Create the HTML file with the mermaid code
        with open("diagram.html", "w") as f:
            f.write(f"""
            <html>
                <head>
                    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
                    <script>mermaid.initialize({{startOnLoad:true}});</script>
                </head>
                <body>
                    <div class="mermaid">
                        {mermaid_code}
                    </div>
                </body>
            </html>
            """)
        
        print("Diagram successfully generated.")
        
        # Save the response to a file
        with open("gpt4_response.txt", "w") as f:
            f.write(task.output.blocks[0].text)
    else:
        print("No diagram found in the response from GPT-4.")