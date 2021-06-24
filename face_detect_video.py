import cv2

# Load the cascade
face_cascade = cv2.CascadeClassifier('HS.xml')

# To capture video from webcam.
cap = cv2.VideoCapture(0)

# KNOWN WIDTH OF BOX = ~16in


def distance_from_camera(known_width, focal_length, per_width):
    return (float(known_width) * float(focal_length)) / float(per_width)


KNOWN_WIDTH = 16.0
KNOWN_DISTANCE = 25.0
F = (350 * 29) / 16


def get_distance_from_faces(frame, faces):
    for (x, y, w, h) in faces:
        for (x2, y2, w2, h2) in faces:
            cv2.line(frame, (x, y), (x2, y2), (100, 100, 0), 2)
    return 0


while True:
    # Read the frame
    _, img = cap.read()
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    get_distance_from_faces(img, faces)
    # Draw the rectangle around each face
    x_value = 0
    y_value = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    for (x, y, w, h) in faces:
        focal_length = float(w) * float(KNOWN_DISTANCE) / float(KNOWN_WIDTH)
        cv2.rectangle(img, (x, y), (x+w, y+h), (100, 100, 0), 2)
        # est_dist = distance_from_camera(KNOWN_WIDTH, focal_length, float(w))
        est_dist = round((16 * F) / w, 2)
        #print("EST - " + str(est_dist))
        print("WIDTH ", w)
        cv2.putText(img,
                    str(est_dist),
                    (x, y),
                    font, 1,
                    (0, 255, 255),
                    2,
                    cv2.LINE_4)

    # Display
    cv2.imshow('img', img)
    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
# Release the VideoCapture object
cap.release()
