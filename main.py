import cv2
import sys, os

class faceExtractor:
    def __init__(self):
        self.images = os.listdir("faces")
        self.video_source = 'camera'
        self.capacities = []
        self.histograms = []
        self.faceX = 1
        self.faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.initilize()
    def initilize(self):
        if len(sys.argv) >= 1:
            if sys.argv[1] == '-h' or sys.argv[1] == '--help':
                print('Usage> python3 main.py VIDEO_PATH_TO_NAME(optional- default is your camera0 for live streaming)')
                return False
            self.video_source = sys.argv[1]
        self.handler()
            
    def existsFace(self, histogram):
        self.images = os.listdir("faces")
        self.capacities = []
        self.histograms = []
        for img in self.images:
            try:
                image = cv2.imread("faces/" + img)
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                self.histograms.append(cv2.calcHist([gray_image], [0],
                                        None, [256], [0, 256]))
                self.capacities.append(0)
            except:
                None
        row = 0
        for histogramX in self.histograms:
            i = 0
            try:
                while i<len(histogram) and i<len(histogramX):
                    self.capacities[row]+=(histogram[i]-histogramX[i])**2
                    i+= 1
                self.capacities[row] = self.capacities[row]**(1 / 2)
            except:
                None
            row += 1
        mostSimilarIndex = 0
        mostSimilar = 999999999999
        i = 0
        for c in self.capacities:
            if c < mostSimilar:
                mostSimilar = c
                mostSimilarIndex = i
            i += 1
        if mostSimilarIndex == 0:
            return False
        return True
    def handler(self):
        try:
            if self.video_source != 'camera0' or self.video_source != 'camera1':
                video_capture = cv2.VideoCapture(self.video_source)
                while(video_capture.isOpened()):
                    # Capture frame-by-frame
                    ret, frame = video_capture.read()

                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    faces = self.faceCascade.detectMultiScale(
                        gray,
                        scaleFactor=1.2,
                        minNeighbors=5,
                        minSize=(30, 30),
                        flags=cv2.CASCADE_SCALE_IMAGE
                    )

                    # Draw a rectangle around the faces
                    for (x, y, w, h) in faces:
                        face = gray[y:y+h, x:x+w]
                        histogram = cv2.calcHist([face], [0],
                                        None, [256], [0, 256])
                        if not self.existsFace(histogram):
                            cv2.imwrite("faces/{}.png".format(self.faceX), frame[y:y+h, x:x+w])
                            self.faceX += 1
                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                    # Display the resulting frame
                    cv2.imshow('Video', frame)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

            else:
                if self.video_source == 'camera0':
                    video_capture = cv2.VideoCapture(0)
                else:
                    video_capture = cv2.VideoCapture(1)
                while True:
                    # Capture frame-by-frame
                    ret, frame = video_capture.read()

                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    faces = self.faceCascade.detectMultiScale(
                        gray,
                        scaleFactor=1.2,
                        minNeighbors=5,
                        minSize=(30, 30),
                        flags=cv2.CASCADE_SCALE_IMAGE
                    )

                    # Draw a rectangle around the faces
                    for (x, y, w, h) in faces:
                        face = gray[y:y+h, x:x+w]
                        histogram = cv2.calcHist([face], [0],
                                        None, [256], [0, 256])
                        if not self.existsFace(histogram):
                            cv2.imwrite("faces/{}.png".format(self.faceX), frame[y:y+h, x:x+w])
                            self.faceX += 1
                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                    # Display the resulting frame
                    cv2.imshow('Video', frame)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

            # When everything is done, release the capture
            video_capture.release()
            cv2.destroyAllWindows()
        except:
            sys.exit(0)
            return False
# Starting
ob = faceExtractor()