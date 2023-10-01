
def colorize_input(prompt, color_code):
    return f"\033[{color_code}m{prompt}\033[0m"
