import cv2
import numpy as np
import argparse
import datetime
import threading
import os


parser = argparse.ArgumentParser()
parser.add_argument('--play_video', help="Tue/False", default=False)
parser.add_argument('--image', help="Tue/False", default=False)
parser.add_argument('--image_path', help="Path of image to detect objects", default="Images/bicycle.jpg")
parser.add_argument('--verbose', help="To print statements", default=True)
parser.add_argument('--weights', help='Path to model weights', default='yolov3.weights')
parser.add_argument('--config', help='Path to configuration file', default='yolov3.cfg')

args = parser.parse_args()


# Load yolo
def load_yolo():
    #net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    net = cv2.dnn.readNetFromDarknet(args.config, args.weights)

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
objectRange = 0

def draw_labels(boxes, confs, colors, class_ids, classes, img, fps, frame_flag):
    global imageNumber
    global lastSavedImage
    imageNumber += 1
    indexes = cv2.dnn.NMSBoxes(boxes, confs, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_PLAIN
    if len(boxes) == 0:
        frame_flag += 1
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
                if (frame_flag >= 120):
                    cv2.imwrite('.\Results\\' + tiempo + '.jpg', img)
                    frame_flag = 0
                else:
                    frame_flag = 0
        else:
            frame_flag += 1
    img = cv2.resize(img, (800, 600))
    cv2.imshow("Image", img)
    return frame_flag

def start_video(video_path):
    print(video_path)
    model, classes, colors, output_layers = load_yolo()
    cap = cv2.VideoCapture(video_path)
    FPS = int(cap.get(cv2.CAP_PROP_FPS))
    contador = 0
    frameFlag = 120
    while True:
        G, frame = cap.read()
        if not G:
            break
        contador += 1
        height, width, channels = frame.shape
        blob, outputs = detect_objects(frame, model, output_layers)
        boxes, confs, class_ids = get_box_dimensions(outputs, height, width)
        frameFlag = draw_labels(boxes, confs, colors, class_ids, classes, frame, FPS, frameFlag)
        key = cv2.waitKey(1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()

if __name__ == '__main__':
    video_play = args.play_video
    videos_path = "./videos"
    thread_list = []
    if video_play:
        #We use the function listdir from os to get a list of all files in a folder
        #in this case the folder used is videos_path, where all videos should be
        files = os.listdir(videos_path)
        start_time = datetime.datetime.now()
        for f in files:
            #We proceed to fetch the files (videos) to create their specific thread,
            #then we run it and save it in thread_list
            video_path = videos_path+'/'+f
            video_thread = threading.Thread(target=start_video, args=(video_path,))
            video_thread.start()
            thread_list.append(video_thread)

        #After all the threads are finished, we join them in the main thread
        for video_thread in thread_list:
            video_thread.join()
            print("hola")
        end_time = datetime.datetime.now()
        print('Duration: {}'.format(end_time - start_time))

    cv2.destroyAllWindows()
