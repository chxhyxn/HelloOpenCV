# import package
try:
    from cv2 import cv2
except ImportError:
    pass
import copy

# get video
videoPath = "video/Sonny.mp4"
captures = cv2.VideoCapture(videoPath)

# get video properties
videoFPS = captures.get(cv2.CAP_PROP_FPS)
videoWidth = int(captures.get(cv2.CAP_PROP_FRAME_WIDTH))
videoHeight = int(captures.get(cv2.CAP_PROP_FRAME_HEIGHT))
videoSize = (videoWidth, videoHeight)

# encoding, write output video
# fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
# output = cv2.VideoWriter(f"{videoPath.split('.')[0]}_output.mp4", fourcc, videoFPS, videoSize)
if not captures.isOpened(): exit()

fps = 10

while True:
    isReturn, frame = captures.read()
    if not isReturn:
        exit()

    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    img_mask1 = cv2.inRange(img_hsv, (0,0,0), (35,255,255)) # 녹색 아닌 색영역1
    img_mask2 = cv2.inRange(img_hsv, (55,0,0), (255,255,255)) # 녹색 아닌 색영역2
    img_mask = img_mask1 + img_mask2

    img_result = cv2.bitwise_and(frame, frame, mask=img_mask)

    cv2.imshow("Croma", img_result)

    if cv2.waitKey(fps) == ord('q'):
        break