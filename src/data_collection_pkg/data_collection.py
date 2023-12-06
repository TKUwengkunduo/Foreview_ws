import os
import time
import cv2
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class DataCollector(Node):
    def __init__(self):
        super().__init__('data_collector')
        self.subscription = self.create_subscription(
            Int32,
            'topic_name',
            self.listener_callback,
            10)
        self.subscription
        self.latest_data = -1

    def listener_callback(self, msg):
        self.latest_data = msg.data

def create_directory():
    folder_name = time.strftime("%Y%m%d_%H%M")
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

def find_camera():
    index = 0
    while True:
        cap = cv2.VideoCapture(index)
        if cap is None or not cap.isOpened():
            print(f"No camera found at index {index}")
            index += 1
        else:
            print(f"Camera found at index {index}")
            return cap

def capture_photo_and_data():
    rclpy.init(args=None)
    data_collector = DataCollector()
    cap = find_camera()
    folder_name = create_directory()

    try:
        while True:
            ret, frame = cap.read()
            if ret:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"{folder_name}/{timestamp}.png"
                cv2.imwrite(filename, frame)
                print(f"Captured {filename}")

                data_to_save = data_collector.latest_data if data_collector.latest_data is not None else -1
                with open(f"{folder_name}/data.txt", "a") as file:
                    file.write(f"{filename}: {data_to_save}\n")

            time.sleep(1)
            rclpy.spin_once(data_collector, timeout_sec=0)
    except KeyboardInterrupt:
        print("Program interrupted, releasing resources...")
    finally:
        cap.release()
        rclpy.shutdown()
        print("Resources released and ROS node shut down.")

if __name__ == "__main__":
    capture_photo_and_data()
