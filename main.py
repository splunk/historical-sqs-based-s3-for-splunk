from bin.historical import GUIArgs
from bin.historical import HandleArgs

def main():
    '''
    CLI GUI
    '''
    try:
        inst = GUIArgs()
    except ValueError as e:
        print(e)
        return
    inst.ingest()

    '''
    Normal CLI
    '''
    # try:
    #     inst = HandleArgs()
    # except SyntaxError as e:
    #     print(e)
    #     return
    # inst.ingest()

if __name__ == '__main__':
    main()