import cv2
import numpy as np
import argparse
import time
import datetime
import threading


parser = argparse.ArgumentParser()
parser.add_argument('--play_video', help="Tue/False", default=False)
parser.add_argument('--image', help="Tue/False", default=False)
parser.add_argument('--video_path', help="Path of video file", default="videos/fire1.mp4")
parser.add_argument('--image_path', help="Path of image to detect objects", default="Images/bicycle.jpg")
parser.add_argument('--verbose', help="To print statements", default=True)
parser.add_argument('--use_gpu', help='Use GPU (OpenCV must be compiled for GPU).', default=False,)
parser.add_argument('--weights', help='Path to model weights', default='yolov3.weights')
parser.add_argument('--config', help='Path to configuration file', default='yolov3.cfg')

args = parser.parse_args()


# Load yolo
def load_yolo():
    #net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    net = cv2.dnn.readNetFromDarknet(args.config, args.weights)
    if args.use_gpu:
        print('Using GPU')
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    classes = []
    with open("obj.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    layers_names = net.getLayerNames()
    output_layers = [layers_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    return net, classes, colors, output_layers


def detect_objects(img, net, outputLayers):
    blob = cv2.dnn.blobFromImage(img, scalefactor=0.00392, size=(320, 320), mean=(0, 0, 0), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward(outputLayers)
    return blob, outputs


def get_box_dimensions(outputs, height, width):
    boxes = []
    confs = []
    class_ids = []
    for output in outputs:
        for detect in output:
            scores = detect[5:]
            class_id = np.argmax(scores)
            conf = scores[class_id]
            if conf > 0.9:
                center_x = int(detect[0] * width)
                center_y = int(detect[1] * height)
                w = int(detect[2] * width)
                h = int(detect[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confs.append(float(conf))
                class_ids.append(class_id)
    return boxes, confs, class_ids


imageNumber = 0
frameFlag = 120
objectRange = 0


def draw_labels(boxes, confs, colors, class_ids, classes, img, fps):
    global imageNumber
    global lastSavedImage
    global frameFlag
    #print(imageNumber)
    imageNumber += 1
    indexes = cv2.dnn.NMSBoxes(boxes, confs, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_PLAIN
    if len(boxes) == 0:
        frameFlag += 1
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[0]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 4)
            cv2.putText(img, label, (x, y - 5), font, 4, color, 4)
            if label in ["Rifle", "Gun", "Fire"]:
                segundos = imageNumber / fps
                tiempo = str(datetime.timedelta(seconds=round(segundos))).replace(":", "-")
                print(tiempo)
                if (frameFlag >= 120):
                    cv2.imwrite('D:\\Carpeta\\' + tiempo + '.jpg', img)
                    frameFlag = 0
                else:
                    frameFlag = 0
        else:
            frameFlag += 1
    img = cv2.resize(img, (800, 600))
    cv2.imshow("Image", img)

def start_video(video_path):
    model, classes, colors, output_layers = load_yolo()
    cap = cv2.VideoCapture(video_path)
    FPS = int(cap.get(cv2.CAP_PROP_FPS))
    lista = []
    contador = 0
    while True:
        G, frame = cap.read()
        if not G:
            break
        lista.append(frame)
        print(contador)
        contador +=1

        height, width, channels = frame.shape
        blob, outputs = detect_objects(frame, model, output_layers)
        boxes, confs, class_ids = get_box_dimensions(outputs, height, width)
        draw_labels(boxes, confs, colors, class_ids, classes, frame, FPS)

        key = cv2.waitKey(1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()



    #t1 = threading.Thread(target=image_detect, args=(lista[:25],))
    #t2 = threading.Thread(target=image_detect, args=(lista[26:50],))

    #t1.start()
    #t2.start()

    #t1.join()
    #t2.join()


    #image_detect(lista[:200])



if __name__ == '__main__':
    video_play = args.play_video
    image = args.image
    if video_play:
        video_path = args.video_path
        if args.verbose:
            print('Opening ' + video_path + " .... ")
        start_video(video_path)
    cv2.destroyAllWindows()
