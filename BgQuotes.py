#!/bin/python
import click, random, math, json
from textwrap import TextWrapper
from PIL import Image, ImageFont, ImageDraw


def calc_fg_color(bg_color):
    result = []
    for c,idx in enumerate(bg_color):
        c = c / 255.0
        if c <= 0.03928:
            result.append(c/12.92)
        else:
            result.append(((c+0.055)/1.055) ^ 2.4)

    L = 0.2126 * result[0] + 0.7152 * result[1] + 0.0722 * result[2]

    #if L > math.sqrt(1.05 * 0.05) - 0.05:
    if L > math.sqrt(1.05 * 0.05):
        return (0, 0, 0)
    else:
        return (255, 255, 255)


@click.command()
@click.option('--font', default=None, help='(Optional) Path to the font you wish to use, overrides --font-list')
@click.option('-f', '--font-list', default=None, help='(Optional) Path to a list of fonts. Fonts in a font list must be absolute paths to the font and there can only be one font per line.')
@click.option('--quote', default=None, help='(Optional) Quote to put in the image. Overrides --quote-list.')
@click.option('-q', '--quote-list', default=None, help='(Optional) Path to a list of quotes.')
@click.option('-o', '--output', default=None, help='(Required) Output image path')
@click.option('-h', '--height', default=None, help='(Required) Height of output image.')
@click.option('-w', '--width', default=None, help='(Required) Width of output image.')
@click.option('-s', '--font-size', default=12, help='(Optional) Size of font. Defaults to 12.')
def main(font, font_list, quote, quote_list, output, height, width, font_size):
    if( not font and not font_list ):
        click.echo("Either --font or -f / --font_list must be provided.")
        return

    if( not quote and not quote_list ):
        click.echo("Either --quote or -q / --quote_list must be provided.")
        return

    if( not output ):
        click.echo("Must provide -o / --output to specity an output file. Example: ./my_image.png")
        return

    if( not height ):
        click.echo("Must provide -h / --height to specify output image width.")
        return

    height = int(height)

    if( not width):
        click.echo("Must provide -w / --weight to specify output image width.")
        return

    width = int(width)

    if not quote:
        with open(quote_list, "r") as f:
            quote_list = json.load(f)
            if quote_list[len(quote_list)-1] == "":
                quote_list.pop()
            quote = random.choice(quote_list)

    if not font:
        with open(font_list, "r") as f:
            font_list = json.load(f)
            if font_list[len(font_list)-1] == "":
                font_list.pop()
            font = random.choice(font_list)


    print("Font: %s" % font)
    font = ImageFont.truetype(font, font_size)

    bg_color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255))

    fg_color = calc_fg_color(bg_color)

    x = math.ceil(
            random.randint(
                0,
                math.ceil(
                    (width - (width * .2))
                )
            ))
    y = math.ceil(
            random.randint(
                0,
                math.ceil(
                    (width - (width * .2))
                )
            ))

    sum_h = 0
    sum_w = 0
    for c in quote:
        size = font.getsize(c)
        sum_w += size[0]
        sum_h += size[1]

    avg_w = math.ceil(sum_w/len(quote))
    avg_h = math.ceil(sum_h/len(quote))

    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    offset = 50
    margin = 50
    T = TextWrapper(replace_whitespace=False, drop_whitespace=False, width=(width/avg_w)-5)
    for line in T.wrap(quote):
        draw.text((margin, offset), line, fg_color, font=font)
        offset += font.getsize(line)[1]


    img.save(output)




if __name__ == "__main__":
    main()
