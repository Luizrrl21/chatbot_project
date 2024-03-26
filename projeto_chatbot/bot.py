import json
from difflib import get_close_matches

# https://www.invertexto.com/workshopbibliotecas

def load_knowledge_base(file_path:str) -> dict:
    with open(file_path,'r') as file:
        data:dict = json.load(file)
    return data

def save_knowledge_base(file_path : str,data : dict):
    with open(file_path, 'w') as file:
        json.dump(data,file, indent=2)


def find_best_match(user_question : str, questions: list[str]) -> str | None:
    matches : list = get_close_matches(user_question,questions,n=1,cutoff=0.6)
    return matches[0] if matches else None


def get_answer_for_question(question : str, knowledge_base:dict) -> str | None:
    for q in knowledge_base["question"]:
        if q["question"] == question:
            return q["answer"]



def chat_bot():
    knowledge_base : dict = load_knowledge_base(file_path="knowledge.json")

    while True:
        print("Caso Deseje sair, digite QUIT")
        user_input:str = input("Voce: ")

        if user_input.lower() == "quit":
            break

        best_match = find_best_match(user_input,[q["question"] for q in knowledge_base["question"]])
    
        if best_match:
             answer:str = get_answer_for_question(best_match,knowledge_base)
             print(f"Bot : {answer}")
        else:
            print(f"Bot: Eu nao sei a resposta, voce poderia me ensinar? ")
            new_answer: str = input("Digite a resposta ou escreva \'pular\' para sair: ")

            if new_answer.lower() != "pular":
                knowledge_base["question"].append({"question" : user_input,
                                                   "answer" : new_answer})
                save_knowledge_base("knowledge.json", knowledge_base)
                print("Bot: Obrigado! Aprendi uma nova resposta!")