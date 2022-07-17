import os

def program_open(name):
    app = None
    appsim = None
    get_user = os.path.expanduser('~')
    user = get_user + "\AppData\Roaming\Microsoft\Windows\Start Menu\Programs"


    for file in os.listdir(user):
        if name == file.lower():

            if (file.endswith('.lnk') or file.endswith('.url')):
                app = f'{user}\{file}'
                break

        elif name in file.lower():
            if (file.endswith('.lnk') or file.endswith('.url')):
                appsim = f'{user}\{file}'
                break

        else:
            for root, dirs, files in os.walk(user):
                for file in files:
                    file = file.split('.', 1)[0]
                    if name == file.lower():
                        app = os.path.join(root, file)
                        break
                    elif name in file.lower():
                        appsim = os.path.join(root, file)
                        break

    if app == None:
        for file in os.listdir("C:\ProgramData\Microsoft\Windows\Start Menu\Programs"):
            if name == file.lower():

                if file.endswith('.lnk') or file.endswith('.url'):
                    app = f"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\{file}"
                    break

            elif name in file.lower():

                if file.endswith('.lnk') or file.endswith('.url'):
                    appsim = f"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\{file}"
                    break

            else:
                for root, dirs, files in os.walk('C:\ProgramData\Microsoft\Windows\Start Menu\Programs'):
                    for file in files:
                        file = file.split('.', 1)[0]
                        if name == file.lower():
                            app = os.path.join(root, file)
                        elif name in file.lower():
                            appsim = os.path.join(root, file)

    if app is None:
        return appsim
    else:
        return app

