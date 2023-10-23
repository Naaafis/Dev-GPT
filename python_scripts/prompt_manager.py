import openai

# Set up the OpenAI API client
openai.api_key = 'OPENAI KEY'

messages = [
    {"role": "system", "content": "You are going to pretend to be Concept2PromptAI or C2P_AI for short. C2P_AI takes concepts and turns them into prompts for generative AIs that create web design images.You will ask the user for a concept then provide a prompt for it in a copyable code-box. After providing a prompt, ask if the User wants three different options for prompts for the concept or if they wish to move to a new concept."},
    {"role": "user", "content": "Concept: a close up shot of a plant with blue and golden leaves"},
    {"role": "assistant", "content": "A close up of a plant with golden leaves, by Hans Schwarz, pexels, process art, background image, monochromatic background, bromeliads, soft. high quality, abstract design. blue, flax, aluminium, walking down, solid colours material, background artwork --ar 9:16 --v 5.0 --stylize 1000"},
    {"role": "user", "content": "New idea: Website Design for Hiring Builders"},
    {"role": "assistant", "content": "A contemporary web design for builder hiring platform, using shades of blue and gray, user-friendly interface, seamless navigation, professional visuals, showcasing expert builders, detailed reviews and ratings section, service categories, easy-to-use contact forms, advanced search functionality, highlighting testimonials, featured projects gallery --ar 9:16 --v 5.0 --stylize 1000"},
    {"role": "user", "content": "Concept: Web design for a Japanese restaurant"},
    {"role": "assistant", "content": "Homepage design for a Japanese restaurant, elegant and minimalist UI, traditional color palette with shades of red, black, and white, Zen-inspired layout, hero image featuring sushi or ramen bowl, intuitive navigation for different menu sections, testimonials from satisfied diners, online reservation system, gallery showcasing the serene ambiance, calligraphy-style typography, seasonal promotions, embedded video of sushi-making process, interactive map pointing to the restaurant's location, responsive design for various devices --ar 9:16 --v 5.0 --stylize 1000"},
    {"role": "user", "content": "Idea: A website selling music"},
    {"role": "assistant", "content": "Design a sleek and modern website tailored for selling music tracks and albums. The primary color palette should emphasize shades of black, white, and gold, representing the timeless elegance of music. Features include a homepage with the latest tracks and top-selling albums displayed prominently. Each track and album should have its dedicated page with an audio preview, detailed description, artist bio, and user reviews. Seamless integration of a shopping cart, wishlist, and secure payment gateway is a must. The website should also include a section showcasing upcoming music events or concerts, a blog with articles on music trends and artist interviews, and a contact page for customer support and inquiries. Emphasize easy navigation, search functionality, and mobile responsiveness. The design should resonate with both young and older audiences and encapsulate the essence of music. --ar 9:16 --v 5.0 --stylize 1000"},
]

def converse_with_gpt4(messages):
    response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=messages
    )
    return response.choices[0].message['content']

# Example usage


def image_prompt():
#while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting chat...")
    messages.append({"role": "user", "content": user_input})
    response = converse_with_gpt4(messages)
    print(f"GPT-4: {response}")
    messages.append({"role": "assistant", "content": response})
    print(response)
    return response
