import random
import os

def load_list(name):
    result = []
    with open(name, 'r') as f:
        for line in f:
            result.append(line.strip())
    return result

dir = os.path.join(os.path.dirname(__file__), 'wordlists').replace('\\','/')
NOUNS = load_list(dir + '/nouns.txt')
ADJECTIVES = load_list(dir + '/adjectives.txt')

def get_name():
    adj1 = ADJECTIVES[random.randint(0, len(ADJECTIVES))]
    adj2 = ADJECTIVES[random.randint(0, len(ADJECTIVES))]
    noun = NOUNS[random.randint(0, len(NOUNS))]
    return adj1.capitalize() + adj2.capitalize() + noun.capitalize()


if __name__ == '__main__':
    for i in range(10):
        print get_name()
