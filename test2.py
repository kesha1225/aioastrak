import requests

host = "http://afternoon-dusk-97603.herokuapp.com/{}"


token_kesha = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlkIjoxMiwidXNlcm5hbWUiOiJrZXNoYTEyMjUiLCJwYXNzd29yZCI6InJvb3Ryb290In0sImlhdCI6MTU4MTg4NDEzNn0.CqZ-ZNl_gtYnrYHsYHx7-evRzumF2Tdx7QCXZBhpYIw"


a = requests.post(host.format("messages/send"), data={
    "token": token_kesha,
    "text": "привет",
    "to": 11,
})

print(a.json())
