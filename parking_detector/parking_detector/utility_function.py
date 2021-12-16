import base64
from PIL import Image
from io import BytesIO


def send_image_process(bytes_img):
    image_b64 = base64.b64encode(bytes_img) #we first create a string 
    image_ascii = image_b64.decode('ascii')#we decode it to ascii characters
    return image_ascii #we use the ascii image inside the json because it is serializable

def opencv_to_bytes(img):
    im_pil = Image.fromarray(img)
    img_byte_arr = BytesIO()
    im_pil.save(img_byte_arr, format='jpeg')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr
