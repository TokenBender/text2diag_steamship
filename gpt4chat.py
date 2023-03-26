from steamship import Steamship

# Create a Steamship client
# NOTE: When developing a package, just use `self.client`
client = Steamship(workspace="gpt-4_chat_v1")

# Create an instance of this generator
generator = client.use_plugin('gpt-4')

while True:
    # Generate text
    print("\n\nAssistant Ready>>")
    task = generator.generate(text=input("User:"))

    # Wait for completion of the task.
    task.wait()

    # Print the output
    print("Assistant:",task.output.blocks[0].text)