import Ice, traceback
import cv2
import sys
import jderobot
import numpy
import Image

def data_to_image (data):
  img= Image.fromstring('RGB', (data.description.width,data.description.height), data.pixelData, 'raw', "BGR")
  pix = numpy.array(img)
  return pix

def transf_image (image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_trans = gray
    return img_trans

if __name__ == "__main__":

  status = 0
  ic = None
  try:
    ic = Ice.initialize()
    obj = ic.stringToProxy('cameraA:default -h localhost -p 9999')
    cv2.namedWindow("Image")
    cv2.moveWindow("Image", 50, 50)
    cv2.namedWindow("Transformate image", cv2.WINDOW_NORMAL)
    cv2.moveWindow("Transformate image", 1000, 50)




    while(1):
      cam = jderobot.CameraPrx.checkedCast(obj)
      data = cam.getImageData("RGB8")
      img = data_to_image (data)
      cv2.imshow('Image',img)
      cv2.imshow('Transformate image',transf_image(img))
      cv2.waitKey(30)


    cv2.destroyAllWindows()


  except:
    traceback.print_exc()
    status = 1


  if ic:
    try:
      ic.destroy()
    except:
      traceback.print_exc()
      status = 1

sys.exit(status)
