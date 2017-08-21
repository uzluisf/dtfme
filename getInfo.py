import json


def json_data(r):
    """Deserialize json and return a dictionary."""
    json_string = json.dumps(r.json())
    data = json.loads(json_string)
    lista = data["results"][0]

    return lista


def get_definition(lista):
    """Loop through a dictionary and return the first definition of a word."""
    for key, value in lista.items():
        if key == "lexicalEntries":
            for item in lista[key]:
                first = lista[key][0]
                for k, v in first.items():
                    if k == "entries":
                        second = first[k]
                        definition = second[0]["senses"][0]["definitions"][0]
    return definition

def comment_definition(comment, word, definition,filename):
    """Verify comment ids, handle exceptions and post word's definition."""
    header = "**{}**:".format(word.title())
    header = header.replace(" ", "")
    body = "\n\n>{}.\n".format(definition.capitalize())
    word_link = "\nMore about [{}](https://en.oxforddictionaries.com/definition/{}).".format(word, word)
    footer = "\n***\n[Info](https://www.reddit.com/r/roomofbugs)" 
    message = header + body + word_link + footer

    comment_obj_r = open(filename, 'r')

    log = ''

    if comment.id not in comment_obj_r.read().splitlines():
        log = "Word: " + word.lower() + ". Replying!"
        print(log)
        comment.reply(message)

        comment_obj_r.close()

        comment_obj_w = open(filename,'a+')
        comment_obj_w.write(comment.id + '\n')
        comment_obj_w.close()
    else:
        log = "Word: " + word.lower() + ". CID stored. No reply needed."
        print(log)




