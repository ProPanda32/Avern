from pathlib import Path
from tempfile import TemporaryDirectory
import math
import sys
from PIL import Image, ImageDraw, ImageFilter
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_FILL
from pptx.enum.shapes import MSO_SHAPE_TYPE

source=Path(sys.argv[1])
target=Path(sys.argv[2])
deck=Presentation(source)
palettes=[
    ((7,23,22),(43,107,82),(166,243,207)),
    ((5,25,37),(24,86,116),(129,216,250)),
    ((25,21,19),(114,77,44),(232,193,138)),
    ((23,18,32),(89,58,112),(219,196,248)),
    ((9,30,31),(42,103,94),(145,231,216)),
    ((29,19,32),(117,53,94),(233,181,206)),
    ((28,18,33),(111,58,94),(233,181,206)),
    ((15,25,41),(48,79,129),(183,210,255)),
    ((28,25,19),(116,88,47),(242,210,148)),
]

def background(index):
    base,glow,accent=palettes[index%len(palettes)]
    w,h=400,225
    image=Image.new('RGB',(w,h))
    px=image.load()
    for y in range(h):
        for x in range(w):
            dx=(x-w*.82)/(w*.32)
            dy=(y-h*.26)/(h*.47)
            bloom=max(0,1-math.hypot(dx,dy))**1.5
            bottom=max(0,1-math.hypot((x-w*.13)/(w*.65),(y-h*1.15)/(h*.72)))*.13
            amount=min(.74,bloom*.7+bottom)
            px[x,y]=tuple(round(base[c]*(1-amount)+glow[c]*amount) for c in range(3))
    image=image.resize((1600,900),Image.Resampling.BICUBIC).convert('RGBA')
    overlay=Image.new('RGBA',image.size,(0,0,0,0))
    d=ImageDraw.Draw(overlay)
    d.polygon([(960,0),(1200,0),(430,900),(190,900)],fill=(*accent,12))
    d.polygon([(1250,0),(1430,0),(650,900),(460,900)],fill=(*accent,7))
    for y in range(56,900,78):
        d.line((0,y,1600,y),fill=(*accent,13),width=1)
    d.arc((730,145,1710,1125),0,360,fill=(*accent,72),width=2)
    d.arc((870,270,1700,1100),0,360,fill=(*accent,25),width=2)
    image=Image.alpha_composite(image,overlay).convert('RGB')
    return image

with TemporaryDirectory() as folder:
    for index,slide in enumerate(deck.slides):
        base,glow,accent=palettes[index%len(palettes)]
        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb=RGBColor(*base)
        bg=Path(folder)/f'background-{index+1}.png'
        background(index).save(bg)
        picture=slide.shapes.add_picture(str(bg),0,0,width=deck.slide_width,height=deck.slide_height)
        tree=slide.shapes._spTree
        tree.remove(picture._element)
        tree.insert(2,picture._element)
        for shape in list(slide.shapes):
            if shape is picture:
                continue
            # A full-slide pale rectangle would hide the designed background.
            if shape.shape_type==MSO_SHAPE_TYPE.AUTO_SHAPE and shape.left<=10000 and shape.top<=10000 and shape.width>=deck.slide_width-20000 and shape.height>=deck.slide_height-20000:
                if shape.fill.type==MSO_FILL.SOLID:
                    color=shape.fill.fore_color
                    try:
                        rgb=color.rgb
                        if min(rgb)>220:
                            shape.fill.background()
                    except (AttributeError,TypeError):
                        pass
            if not shape.has_text_frame:
                continue
            for paragraph in shape.text_frame.paragraphs:
                for run in paragraph.runs:
                    run.font.color.rgb=RGBColor(245,248,244)
    deck.save(target)
print(f'Styled {len(deck.slides)} slide backgrounds; original content retained')
