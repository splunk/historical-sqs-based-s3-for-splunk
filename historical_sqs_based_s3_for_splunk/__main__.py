from historical_sqs_based_s3_for_splunk.cli import Cli, CliGUI

def main():
    '''
    CLI GUI
    '''
    try:
        CliGUI().queue()
    except Exception as e:
        print(e)
        return
    # inst.queue()

    '''
    Normal CLI
    '''
    # try:
    #     inst = Cli()
    # except SyntaxError as e:
    #     print(e)
    #     return
    # inst.queue()

if __name__ == '__main__':
    main()