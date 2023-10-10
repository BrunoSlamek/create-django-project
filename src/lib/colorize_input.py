from typing import Callable


colorize_input = lambda prompt, color_code: f"\033[{color_code}m{prompt}\033[0m"

input_color_green = lambda arg: input(colorize_input(arg, '32')).strip().lower() if isinstance(arg, str) else 'Str required'
