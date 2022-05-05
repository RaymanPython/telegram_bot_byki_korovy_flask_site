def check_name(s):
    s = s.strip()
    print(''.join(s.split('@')))
    return ''.join(s.split('@'))


def get_name(update, type_person):
    if type(update) == str:
        return check_name(update)
    if type(update) == type_person:
        update = update.update
    name = update.message.chat.username
    if name == None:
        return update.message.chat.id
    else:
        return name
