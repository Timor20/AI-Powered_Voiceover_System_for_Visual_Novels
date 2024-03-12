from PIL import Image
import PIL.ImageOps
import pyautogui
import keyboard
import pytesseract
import numpy as np
import cv2

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
# /region function parameters are : left, top, width, height

while True:
    try:
        if keyboard.is_pressed('e'):
            screenshot = pyautogui.screenshot(region=(356, 818, 1214, 174))
            screenshot.save(r'./screenshot.png')

            img = cv2.imread("screenshot.png")

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            cv2.imwrite('gray1.png', gray)

            ret, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

            cv2.imwrite('thresh2.png', thresh)
            threshText = pytesseract.image_to_string('thresh2.png')
            print('**** THRESH2.PNG  *****')
            print(threshText)

            ret, thresh2 = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

            cv2.imwrite('thresh.png', thresh2)
            threshText = pytesseract.image_to_string('thresh.png')
            print('**** THRESH.PNG  *****')
            print(threshText)

            img[thresh == 255] = 0

            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            erosion = cv2.erode(img, kernel, iterations = 1)

            #cv2.namedWindow('image', cv2.WINDOW_NORMAL)
            #cv2.imshow("image", erosion)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()

            cv2.imwrite('screenshot2.png', erosion)

            text = pytesseract.image_to_string('screenshot.png')
            text2 = pytesseract.image_to_string('screenshot2.png')
            print('**** SCREENSHOT.PNG  *****')
            print(text)
            print('**** SCREENSHOT2.PNG  *****')
            print(text2)

            in_path  = 'screenshot.png'
            out_path = 'screenshot3.png'


            Image = cv2.imread(in_path)
            Image2 = np.array(Image, copy=True)

            white_px = np.asarray([255, 255, 255])
            black_px = np.asarray([0  , 0  , 0  ])

            (row, col, _) = Image.shape

            for r in range(row):
                for c in range(col):
                    px = Image[r][c]
                    if all(px == white_px):
                        Image2[r][c] = black_px

            cv2.imwrite(out_path, Image2)

            # cv2.imwrite(out_path, Image2)
            # Image = cv2.imread(in_path)
            # Image = cv2.bitwise_not(Image)
            # b,g,r = cv2.split(Image)
            # z = np.zeros_like(g)
            # Image = cv2.merge((z,z,b))
            # cv2.imwrite(out_path, Image)

            text3 = pytesseract.image_to_string('screenshot3.png')
            print('**** SCREENSHOT3.PNG  *****')
            print(text3)
    except:
        break
