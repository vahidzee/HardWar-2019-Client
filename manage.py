def load_settings(file_name='settings.py'):
    """
    executes given file and returns its lexical vocabulary
    as a python dictionary
    """
    namespace = dict()
    with open(file_name) as handle:
        exec(handle.read(), namespace)
    return namespace


# Loading Settings
settings = load_settings()

while True:
    # Getting input
    command = input('\033[32;0mCommand : \033[0m')

    if command == 'exit':
        exit()
