import google.generativeai as genai

genai.configure(api_key="AIzaSyCkzZgM6ejc3y0WuUrCWO05MD599q4a4ZA")
model = genai.GenerativeModel("gemini-2.0-flash-thinking-exp-1219")
response = model.generate_content("Explain how the world will work when AGI is achieved")
print(response.text)