#!/bin/python
import click, random, math, json
from textwrap import TextWrapper
from PIL import Image, ImageFont, ImageDraw

def hsv_to_rgb(h, s, v):
    h_i = int(h*6)
    f = h*6 - h_i
    p = v * (1 - s)
    q = v * (1 - f*s)
    t = v * (1 - (1 - f) * s)
    if h_i is 0:
        r = v
        g = t
        b = p
    elif h_i is 1:
        r = q
        g = v
        b = p
    elif h_i is 2:
        r = q
        g = v
        b = p
    elif h_i is 3:
        r = p
        g = v
        b = t
    elif h_i is 4:
        r = t
        g = p
        b = v
    elif h_i is 5:
        r = v
        g = p
        b = q
    return (int(r*256), int(g*256), int(b*256))

#def calc_fg_color(bg_color):
#    result = []
#    for c,idx in enumerate(bg_color):
#        c = c / 255.0
#        if c <= 0.03928:
#            result.append(c/12.92)
#        else:
#            result.append(((c+0.055)/1.055) ^ 2.4)
#
#    L = 0.2126 * result[0] + 0.7152 * result[1] + 0.0722 * result[2]
#
#    #if L > math.sqrt(1.05 * 0.05) - 0.05:
#    if L > math.sqrt(1.05 * 0.05):
#        return (0, 0, 0)
#    else:
#        return (255, 255, 255)
#

@click.command()
@click.option('--font', default=None, help='(Optional) Path to the font you wish to use, overrides --font-list')
@click.option('-f', '--font-list', default=None, help='(Optional) Path to a list of fonts. Fonts in a font list must be absolute paths to the font and there can only be one font per line.')
@click.option('--quote', default=None, help='(Optional) Quote to put in the image. Overrides --quote-list.')
@click.option('-q', '--quote-list', default=None, help='(Optional) Path to a list of quotes.')
@click.option('-o', '--output', default=None, help='(Required) Output image path')
@click.option('-h', '--height', default=None, help='(Required) Height of output image.')
@click.option('-w', '--width', default=None, help='(Required) Width of output image.')
@click.option('-s', '--font-size', default=12, help='(Optional) Size of font. Defaults to 12.')
@click.option('-v', '--verbose', default=False, is_flag=True, help='(Optional) Toggles Verbosity.')
@click.option('--font-test', default=False, is_flag=True, help='(Optional) Runs program in font test mode. The program with attempt to load all fonts in font list. Requires --font-list')
def main(font, font_list, quote, quote_list, output, height, width, font_size, verbose, font_test):
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

    if(verbose):
        print("Font List: {0}".format(font_list))

    if font_test:
        with open(font_list, "r") as f:
            font_list = json.load(f)
            for font in font_list:
                try:
                    ImageFont.truetype(font, font_size)
                except:
                    print("Bad font: \"{0}\"".format(font))
        print("Test Passed! Exiting...")
        exit()



    if not font:
        with open(font_list, "r") as f:
            font_list = json.load(f)
            if font_list[len(font_list)-1] == "":
                font_list.pop()
            font = random.choice(font_list)

    if(verbose):
        print("Font: {0}".format(font))

    font = ImageFont.truetype(font, font_size)

    bg_color = hsv_to_rgb(random.random(), 0.8, 0.3)
    #bg_color = (
    #        random.randint(0, 255),
    #        random.randint(0, 255),

    #        255) #random.randint(0, 255))

    #variance_value = random.randint(0, 255)
    #variance_factor = 5 #random.randint(0, 5)
    #variance_sign = random.choice([-1, 1])
    #variance = variance_value * variance_factor * variance_sign

    #bg_color = (
    #    bg_color[0] + variance if bg_color[0] + variance > 0 else bg_color[0],
    #    bg_color[1] + variance if bg_color[1] + variance > 0 else bg_color[1],
    #    bg_color[2] + variance if bg_color[2] + variance > 0 else bg_color[2]
    #)
    #bg_color = (
    #    bg_color[0] if bg_color[0] < 255 else bg_color[0] - 255,
    #    bg_color[1] if bg_color[1] < 255 else bg_color[1] - 255,
    #    bg_color[2] if bg_color[2] < 255 else bg_color[2] - 255
    #)


    fg_color = (255, 255, 255) #calc_fg_color(bg_color)

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

    line_height = []

    T = TextWrapper(replace_whitespace=False, drop_whitespace=False, width=(width/avg_w)-5)
    for line in T.wrap(quote):
        line_height.append(font.getsize(line)[1])

    line_height = max(line_height)

    lines = quote.split("\n")
    print("lines: %s" % lines)
    for line in lines:
        print("line: %s" % line)
        if line != "":
            for subline in T.wrap(line):
                print("subline: %s" % subline)
                draw.text((margin, offset), subline, fg_color, font=font)
                offset += line_height
        else:
            offset += math.ceil(line_height/2)



    img.save(output)




if __name__ == "__main__":
    main()
