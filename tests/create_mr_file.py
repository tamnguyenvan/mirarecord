import os
import struct

def create_mr_file(folder_path, output_file):
    images = sorted(os.listdir(folder_path))
    if not images:
        print("No images found in the folder.")
        return

    image_path = os.path.join(folder_path, images[0])
    width, height = get_image_size(image_path)
    num_frames = len(images)

    with open(output_file, 'wb') as file:
        # Write header
        file.write(struct.pack('<III', num_frames, width, height))

        # Write image data
        for image_name in images:
            image_path = os.path.join(folder_path, image_name)
            with open(image_path, 'rb') as img_file:
                img_data = img_file.read()
                file.write(struct.pack('<I', len(img_data)))  # Write frame size
                file.write(img_data)

def get_image_size(image_path):
    from PIL import Image
    with Image.open(image_path) as img:
        width, height = img.size
    return width, height

if __name__ == "__main__":
    folder_path = "/home/tamnv/Downloads/images"  # Thay đổi đường dẫn đến thư mục ảnh của bạn
    output_file = "output.mr"

    create_mr_file(folder_path, output_file)
    print("MR file created successfully.")
