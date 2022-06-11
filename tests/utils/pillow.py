
def load_with_PIL(path: str, get_data: bool = False):
    from PIL import Image
    img = Image.open(path)
    if get_data:
        return img.getdata()
    else:
        return img

def check_PIL_images_equality(*imgs) -> bool:
    from PIL import ImageChops
    if len(imgs) < 2:
        assert False# [TODO]: use `raise customError`
    img_base = imgs[0]
    for img_target in imgs[1:]:
        diff = ImageChops.difference(img_base, img_target).getbbox()
        if diff:
            return False
        else:
            return True
