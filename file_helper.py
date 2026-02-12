import os

def removeFile(path: str):
    try:
        if os.path.isfile(path):
            os.remove(path)
    except Exception as ex:
        print(f"Error when removing file: {ex}")
        pass


def clearDir(path: str):
    try:
        if not os.path.isdir(path):
            return
        for f in os.listdir(path):
            file_path = os.path.join(path, f)
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                except Exception as ex:
                    print(f"Error when removing file: {ex}")
                    pass
    except Exception as ex:
        print(f"Error when clearing directory: {ex}")
        pass