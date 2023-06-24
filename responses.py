def handle_response(message) -> str:
    p_message = message.lower()
    # TODO more commands and functionality
    # Test command
    if p_message == 'test run':
        return 'test run 1 2 3...'

    # Command that returns usable commands and information about them
    if p_message == 'help':
        return '-test run - runs a test of a bot'
    # When there is no command like provided
    else:
        return 'wrong command, use -help for help'
