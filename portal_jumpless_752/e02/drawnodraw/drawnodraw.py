import math
import cv2
import matplotlib.pyplot as plt


camera_position = [53.906250, 6182.281250, -959.968750]
fov = 90.0
point = [6724.04541, 573.957642, 575.96875]
screen_width = 1280
screen_height = 720


def calculate_camera_angles(screen_x, screen_y):
    aspect_ratio = screen_width / screen_height
    ratio = 4 / 3
    fov_x = 2 * math.degrees(math.atan(math.tan(math.radians(fov) / 2) * aspect_ratio / ratio))
    # fov_y = 2 * math.degrees(math.atan(math.tan(math.radians(fov) / 2) / ratio))
    fov_y = fov_x / aspect_ratio

    dir_x = point[0] - camera_position[0]
    dir_y = point[1] - camera_position[1]
    dir_z = point[2] - camera_position[2]

    yaw = math.degrees(math.atan2(dir_y, dir_x))
    pitch = math.degrees(math.atan2(-dir_z, math.sqrt(dir_x * dir_x + dir_y * dir_y)))

    screen_center_x = screen_width / 2
    screen_center_y = screen_height / 2

    offset_x = (screen_x - screen_center_x) / screen_width * fov_x
    offset_y = (screen_y - screen_center_y) / screen_height * fov_y

    yaw += offset_x
    pitch -= offset_y

    return pitch, yaw


def create_script(image_path, out_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    resized_image = cv2.resize(image, (200, 200))
    edges = cv2.Canny(resized_image, threshold1=100, threshold2=200)

    with open(out_path, "w") as f:
        # f.write("----------|------|------|-|-|1|gameui_activate\n")
        # f.write("----------|------|------|-|-|30|\n")
        # f.write("----------|------|------|-|-|1|gameui_hide\n")

        height, width = edges.shape
        offset_x = (screen_width - width) // 2
        offset_y = (screen_height - height) // 2

        for y in range(height):
            if y % 3 == 0:
                continue
            for x in range(width):
                pixel_value = edges[y, x]
                if pixel_value > 0:
                    pitch, yaw = calculate_camera_angles(x + offset_x, y + offset_y)
                    f.write(f"----------|------|------|-|-|1|tas_aim {pitch} {yaw} 1;\n")


if __name__ == "__main__":
    create_script("tako.jpg", "out.srctas")
