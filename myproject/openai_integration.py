from openai import OpenAI
key = 'sk-proj-Rd2kVMui6J29EL1cVSxxT3BlbkFJE8g23TTYFdUP8qHMl1tO'

client = OpenAI(api_key=key)
def generate_text(text):
    response = client.completions.create(
    model="gpt-3.5-turbo-instruct",
    prompt=text,
    temperature=0.7,
    max_tokens=400
    )

    if response and response.choices:
      print(response.choices[0].text.strip())
      return response.choices[0].text.strip()
    else:
      print("Ошибка")
      return "Ошибка"
