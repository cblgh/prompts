import json
import sys
import urllib.request

# reference https://foosoft.net/projects/anki-connect/#note-actions

deckname = ""

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

def construct_params(lines): 
    cards = [] # list of (front, back) tuples
    front = ""
    back = [] # back is potentially many lines

    # process input into cards
    for line in lines:
        if line == "": # card separator
            # dump previous card
            cards.append((front, "\n".join(back)))
            # reset state
            front = "" 
            back = []
            continue
        if front == "":
            front = line
        else:
            back.append(line)
    # pop in the last card
    if front != "":
        cards.append((front, "\n".join(back)))

    # transform cards into request parameters for call
    params = dict()
    params["notes"] = []
    for card in cards:
        paramEntry = dict()
        paramEntry["deckName"] = deckname
        paramEntry["modelName"] = "Basic"
        paramEntry["fields"] = {"Front": card[0], "Back": card[1]}
        params["notes"].append(paramEntry)
    return params

def get_filename():
    if len(sys.argv) == 1:
        print("usage: prompts.py <prompts.txt>")
        sys.exit(0)
    filename = sys.argv[1]
    if not filename.endswith("txt"):
        print("prompts: file must end with txt")
        sys.exit(0)
    return filename

def read_lines(filename):
    # read input
    with open(filename) as f:
        lines = "".join(f.readlines()).split("\n")
        if len(lines) == 1:
            print("prompts: input file is empty")
            sys.exit(0)
        return lines

def erase_file(filename):
    with open (filename, "w") as f:
        f.write("")

def check_deckname():
    if deckname == "":
        print("prompts: set the deckname variable at the top of prompts.py")
        sys.exit(0)

check_deckname()
filename = get_filename()
lines = read_lines(filename)
print("reading {} lines".format(len(lines)))
result = invoke('addNotes', **construct_params(lines))
print('AnkiConnect says: {}'.format(result))
erase_file(filename)
