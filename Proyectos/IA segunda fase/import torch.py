import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Nom du modèle
model_name = "mistralai/Mistral-7B-Instruct-v0.1"

# Charger le tokenizer (convertit le texte en nombres)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Charger le modèle
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"  # utilise automatiquement ton GPU RTX 3070
)

def chat(prompt):
    # Convertir le texte en tokens
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

    # Génération
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=200,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )

    # Convertir les tokens en texte
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

while True:
    user_input = input("Toi : ")

    if user_input.lower() == "quit":
        break

    prompt = f"[INST] {user_input} [/INST]"
    answer = chat(prompt)

    print("IA :", answer)
    print("-" * 50)
