import easyocr
import cv2

def scan_book(image_path):
    image = cv2.imread(image_path)
    return image

def read_book(image):
    # Initialize the EasyOCR reader
    reader = easyocr.Reader(['en'])

    # Perform OCR on the image
    result = reader.readtext(image)
    # Extract the heading or title

    top_words = []
    top_sizes = []
    num_top_words = 4

    for detection in result:
        _, _, prob = detection
        bounding_box = detection[0]
        width = bounding_box[1][0] - bounding_box[0][0]
        height = bounding_box[2][1] - bounding_box[0][1]
        size = width * height

        # Check if the current word should be included in the top words list
        if len(top_words) < num_top_words:
            top_words.append(detection[1])
            top_sizes.append(size)
        else:
            min_size = min(top_sizes)
            if size > min_size:
                min_index = top_sizes.index(min_size)
                top_words[min_index] = detection[1]
                top_sizes[min_index] = size

    book_name = ""
    for word in top_words:
        book_name = book_name + " " + word
    return book_name

def search_book_amazon(book_title):
    # Format the book title for the search query
    search_query = book_title.replace(' ', '+')

    # Create the Amazon search URL
    amazon_url = f'https://www.amazon.com/s?k={search_query}'
    print("The amazon link for the book you scanned is : \n")

def video_frame():
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        book_name = read_book(frame)
        search_book_amazon(book_name)

    # Release the VideoCapture object and close any open windows
    cap.release()
    cv2.destroyAllWindows()

video_frame()