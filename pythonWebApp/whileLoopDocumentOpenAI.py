import openai
import pytesseract
import os
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import fitz

openai.api_key = "your-api-key"

# from pytesseract import image_to_string

# ---------------------------------------------------------------------------------------------------

def document_to_string(document_path, list_dict_final_images=None):
    # Check the file extension to determine the type of document
    _, file_extension = os.path.splitext(document_path)

    if file_extension.lower() in ['.png', '.jpeg', '.jpg']:
        # Load the image for PNG, JPEG, JPG files
        image = Image.open(document_path)
        # Perform OCR on the image to extract text
        list_final_images = pytesseract.image_to_string(image)
        return list_final_images

    all_images = [list(data.values())[0] for data in list_dict_final_images]

    for index, image_bytes in enumerate(all_images):
        image = Image.open(BytesIO(image_bytes))
        figure = plt.figure(figsize=(image.width / 100, image.height / 100))

        plt.title(f"--- Page Number {index + 1} ---")
        plt.imshow(image)
        plt.axis("off")
        plt.show()


# -------------------------------------------------------------------------------

# Below is the PDF to Image
def pdf_to_image(file_path, scale=300 / 72):
    text = ""
    pdf_document = fitz.open(file_path)

    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()

    pdf_document.close()
    return text


# -------------------------------------------------------------------------------


def convert_any_to_string(filepath):
    my_path = filepath
    if my_path.endswith(".pdf"):
        return pdf_to_image(my_path)

    elif my_path.endswith(".png"):
        return document_to_string(my_path)

    elif my_path.endswith(".jpeg"):
        return document_to_string(my_path)

    elif my_path.endswith(".jpg"):
        return document_to_string(my_path)

    else:
        return "The extension is not valid!"


# ------------------------------------------------------------------------------------------------------

def main():
    filepath = "mjn_final.pdf"
    new_path = filepath.lower()

    try:
        text1 = convert_any_to_string(new_path)
       # print("Document content as string: \n ", text)

        while True:
            question = input("Enter the question (or 'q' to exit): ")
            if question.lower() == 'q':
                break
            prompt = f"Given the following document {text1}\n\nAnswer the questions:{question}"

            response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",
                prompt=prompt,
                max_tokens=100,
                n=1,
                stop=None,
                temperature=0.7
            )
            answer = response.choices[0].text.strip()
            print(answer)

    except Exception as e:
        print("Error: ", e)


if __name__ == "__main__":
    main()
