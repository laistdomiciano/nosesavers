import json
import random


def get_fun_facts(tree_type):
    """Return random fun facts about the 6 types of trees"""
    with open("fun_facts.json", "r") as file:
        fun_facts = json.load(file)
    if tree_type.lower() in fun_facts:
        fun_fact = random.choice(fun_facts[tree_type.lower()])
        return fun_fact

# chosen_tree = "Grass"
# fact = get_fun_facts(chosen_tree)
# print(fact)