import airsim
import os
import time
import numpy as np
import cv2
# Connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)

# Take off
# print("Taking off...")
# client.armDisarm(True)
# client.takeoffAsync().join()

# # Move forward at 1 meter/second for 10 seconds
# print("Moving forward...")
# velocity = 3  # velocity in meters per second
# duration = 1  # duration in seconds
# client.moveByVelocityAsync(velocity, 0, 0, duration).join()
current_dir = os.getcwd()

# Ensure the output directory exists
output_dir = os.path.join(current_dir, 'output_images')
output_dir = "D:\\final_project\\py_scripts\\output_data"
os.makedirs(output_dir, exist_ok=True)

# Capture images from stereo cameras

print("Capturing images...")
def captureImages(i):
# for i in range(10):  # Increase the number of captures to 10
    left_image = client.simGetImage("StereoLeft", airsim.ImageType.Scene)
    right_image = client.simGetImage("StereoRight", airsim.ImageType.Scene)
    
    response = client.simGetImages([airsim.ImageRequest("1", airsim.ImageType.DepthPerspective, True)])[0]

    if left_image:
        left_image_path = output_dir+f"\\left_{i}.png"
        # print(left_image_path)
        with open(left_image_path, 'wb') as f:
            f.write(left_image)
    if right_image:
        right_image_path = output_dir+f"\\right_{i}.png"
        with open(right_image_path, 'wb') as f:
            f.write(right_image)
    if response:

            filename = output_dir + f"\\depth_{i}"
            if response.pixels_as_float:
                print("Type %d, size %d" % (response.image_type, len(response.image_data_float)))                
                airsim.write_pfm(os.path.normpath(filename + '.pfm'), airsim.get_pfm_array(response))
                depth_pfm = airsim.read_pfm(filename+".pfm")
                depth_array = np.array(depth_pfm[0], dtype=np.float32)
                os.remove(filename+".pfm")
                cv2.imwrite(filename+".png", depth_array)
                # airsim.write_file(os.path.normpath(filename + '.png'), df)
            elif response.compress: #png format
                print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
                airsim.write_file(os.path.normpath(filename + '.png'), response.image_data_uint8)
            else: #uncompressed array
                print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
                img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8) # get numpy array
                img_rgb = img1d.reshape(response.height, response.width, 3) # reshape array to 4 channel image array H X W X 3
                cv2.imwrite(os.path.normpath(filename + '.png'), img_rgb) #
    #             right_image_path = output_dir+ f"\\depth_{i}.png"
    # with open(right_image_path, 'wb') as f:
    #         f.write(depth)
    
    print(f"Saved left_{i}.png and right_{i}.png and depth_{i}.png")
    
    
    # time.sleep(1)  # Interval between captures

start_time = time.time()  # Record the start time
end_time = start_time + 28  # Set the end time for 10 seconds later
i=0
while time.time() < end_time:
    # print(f"Running... {time.strftime('%H:%M:%S')}")
    
    captureImages(i)
    i+=1
    time.sleep(1)
# Disarm and reset
client.armDisarm(False)
client.reset()

client.enableApiControl(False)
print("Image capture complete.")