import cv2
import face_recognition
import pickle
import time

image_file = 'C:/Users/user/opencv_dnn_202005/image/marathon_01.jpg'
encoding_file = 'encodings.pickle'
unknown_name = 'Unknown'
# Either cnn  or hog. The CNN method is more accurate but slower. HOG is faster but less accurate.
model_method = 'cnn'


def detectAndDisplay(image):
    start_time = time.time()
    # bgr형태를 rgb형태로 바꿈
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # detect the (x, y)-coordinates of the bounding boxes corresponding
    # to each face in the input image, then compute the facial embeddings
    # for each face
    boxes = face_recognition.face_locations(rgb,
                                            model=model_method)
    # 이미지에서 얼굴의 위치(박스로 표현) 찾아냄
    encodings = face_recognition.face_encodings(rgb, boxes)
    # box값을 encoding

    # initialize the list of names for each face detected
    names = []

    # loop over the facial embeddings
    for encoding in encodings:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(data["encodings"],
                                                 encoding)
        # encoding했던 사진과 지금 가져온 이미지를 비교
        name = unknown_name

        # check to see if we have found a match
        if True in matches:
            # find the indexes of all matched faces then initialize a
            # dictionary to count the total number of times each face
            # was matched
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            # determine the recognized face with the largest number of
            # votes (note: in the event of an unlikely tie Python will
            # select first entry in the dictionary)
            name = max(counts, key=counts.get)
            # 가장 많이 나온 이름을 name에 넣어줌 (테디 찾으려고 그러는데 잘못인식해서 손흥민이 몇번 나오는 경우가 생길 수 있으니까)

        # update the list of names
        names.append(name)

    # loop over the recognized faces
    for ((top, right, bottom, left), name) in zip(boxes, names):
        # draw the predicted face name on the image
        y = top - 15 if top - 15 > 15 else top + 15
        color = (0, 255, 0)
        line = 2
        if (name == unknown_name):
            color = (0, 0, 255)
            line = 1
            name = ''

        cv2.rectangle(image, (left, top), (right, bottom), color, line)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.75, color, line)

    end_time = time.time()
    process_time = end_time - start_time
    print("=== A frame took {:.3f} seconds".format(process_time))
    # show the output image
    cv2.imshow("Recognition", image)


# load the known faces and embeddings
data = pickle.loads(open(encoding_file, "rb").read())

# load the input image
image = cv2.imread(image_file)
detectAndDisplay(image)

cv2.waitKey(0)
cv2.destroyAllWindows()
