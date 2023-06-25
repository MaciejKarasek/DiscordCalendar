def handle_response(message) -> str:
    p_message = message.lower()
    # TODO more commands and functionality
    # Test command
    if p_message == 'test run':
        return 0xffc200, 'Test', 'test run 1 2 3...'

    # Command that returns usable commands and information about them
    if p_message == 'help':
        return 0x87ceeb, 'Help:', '`-test run` - runs a test of a bot\n\
                                    Use double prefix for answer \
                                    in private chat `--`\n\
                                    `example: --help` - Sends you private \
                                                message with bot instructions'
    # When there is no command like provided
    else:
        return 0xFF0000, 'Error', 'wrong command, use -help for help'
