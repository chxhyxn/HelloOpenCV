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
fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
output = cv2.VideoWriter(f"{videoPath.split('.')[0]}_output.mp4", fourcc, videoFPS, videoSize)
if not captures.isOpened(): exit()

# Select ROI ( Region of Interest )
isReturn, firstFrame = captures.read()
cv2.namedWindow("Choose What you interest")
cv2.imshow("Choose What you interest", firstFrame)

rect = cv2.selectROI("Choose What you interest", firstFrame, fromCenter=False, showCrosshair=True)

cv2.destroyWindow("Choose What you interest")

# generate tracker
tracker = cv2.TrackerCSRT_create()
tracker.init(firstFrame, rect)

# overlay func
def overlay(frame, x, y, w, h, overlayImage):
    x,y,w,h = map(int,(x,y,w,h))
    overlayImageResized = cv2.resize(overlayImage, (2*w, 2*h))
    alpha = overlayImageResized[:,:,3] # RGBA
    maskImage = alpha/255
    for channel in range(3):
        frame[y-h:y+h, x-w:x+w, channel] = (overlayImageResized[:,:,channel]*maskImage) + (frame[y-h:y+h, x-w:x+w, channel]*(1-maskImage))


# get Image
circleImage = cv2.imread('circle1.png', cv2.IMREAD_UNCHANGED)

# video enhancing / tracker updating
while True:
    isReturn, frame = captures.read()
    if not isReturn:
        exit()

    isTracking, xywh = tracker.update(frame)
    x, y, w, h = map(int, xywh)

    # apply croma
    frame2 = copy.deepcopy(frame)
    img_hsv = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
    img_mask1 = cv2.inRange(img_hsv, (0,0,0), (35,255,255)) # 녹색 아닌 색영역1
    img_mask2 = cv2.inRange(img_hsv, (55,0,0), (255,255,255)) # 녹색 아닌 색영역2
    img_mask = img_mask1 + img_mask2

    # draw rectangle
    a = 20
    # cv2.rectangle(frame,(x-a,y-a), (x+w+a, y+h+a), (255,0,0), 2)

    # overlay Image
    overlay(frame, x+w/2, y+h, w+a, h, circleImage)

    # paste frame2 on frame1
    cv2.copyTo(frame2, img_mask, frame)

    output.write(frame[int((y+h/2)-videoHeight/2):int((y+h/2)+videoHeight/2),
                 int((x+w/2)-videoWidth):int((x+w/2)-videoWidth)])

    cv2.imshow("Now enhancing...", frame)

    if cv2.waitKey(1) == ord('q'):
        break
