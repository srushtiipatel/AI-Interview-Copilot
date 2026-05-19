from google import genai

client = genai.Client(api_key="AIzaSyD6TEeolvX2zWv54gzvhQGsjX81wrxB4Ng")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Say hello"
)

print(response.text)