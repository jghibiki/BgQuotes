#!/bin/python
import click, random, math, json
from termcolor import colored, cprint

colors = [
    "grey",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white"
]

highlights = [
    None,
    "on_grey",
    "on_red",
    "on_green",
    "on_yellow",
    "on_blue",
    "on_magenta",
    "on_cyan",
    "on_white"
]


color_combos = [
    #("grey",    "on_white"),
    #("grey",    "on_blue"),
    #("grey",    "on_red"),
    #("grey",    "on_cyan"),
    #("grey",    "on_green"),
    #("grey",    "on_magenta"),
    ("blue",    None),
    ("red",     None),
    ("green",   None),
    ("yellow",  None),
    ("magenta", None),
    ("white",   None)
]

attrs = [
    None,
    "bold",
    "dark",
    "underline",
    "blink"
]



@click.command()
@click.option('--quote', default=None, help='(Optional) Quote to put in the image. Overrides --quote-list.')
@click.option('-q', '--quote-list', default=None, help='(Optional) Path to a list of quotes.')
@click.option('-o', '--output', default=None, help='(Required) Output image path')
@click.option('-v', '--verbose', default=False, is_flag=True, help='(Optional) Toggles Verbosity.')
@click.option('-t', '--color-test', default=False, is_flag=True, help='(Optional) Toggles color test mode.')
def main(quote, quote_list, output, verbose, color_test):
    if( not quote and not quote_list ):
        click.echo("Either --quote or -q / --quote_list must be provided.")
        return

    if not quote:
        with open(quote_list, "r") as f:
            quote_list = json.load(f)
            if quote_list[len(quote_list)-1] == "":
                quote_list.pop()
            quote = random.choice(quote_list)

    if not color_test:
        combo = random.choice(color_combos)
        attr = random.choice(attrs)

        if attr:
            cprint(quote, combo[0], combo[1], attrs=[attr])
        else:
            cprint(quote, combo[0], combo[1])
    else:
        for combo in color_combos:
            cprint(quote, combo[0], combo[1])

if __name__ == "__main__":
    main()
