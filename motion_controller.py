import airsim
import math

def set_initial_position_and_orientation(client, x, y, z, roll_degrees, pitch_degrees, yaw_degrees):
    # Convert degrees to radians for roll, pitch, and yaw
    roll = math.radians(roll_degrees)
    pitch = math.radians(pitch_degrees)
    yaw = math.radians(yaw_degrees)

    # Create a pose with position and orientation
    pose = airsim.Pose(airsim.Vector3r(x, y, z), airsim.to_quaternion(pitch, roll, yaw))
    client.simSetVehiclePose(pose, True)
    print(f"Set initial position to: X={x}, Y={y}, Z={z}, Yaw={yaw_degrees} degrees")

# Function to connect to the AirSim drone client and move the drone
def main():
    # Connect to the AirSim drone client
    client = airsim.MultirotorClient()
    client.confirmConnection()
    client.enableApiControl(True)
    client.armDisarm(True)

    # Take off
    print("Taking off...")
    client.takeoffAsync().join()

    # Move forward
    print("Moving forward...")
    velocity = 4  # velocity in meters per second
    duration = 14  # duration in seconds
    client.moveByVelocityAsync(velocity, 0, 0, duration).join()
    print(f"Moving forward at {velocity} m/s for {duration} seconds.")

    # Wait for the duration of the movement to ensure it completes
    client.hoverAsync().join()  # Hover in place after moving
    print("Movement complete, hovering in place.")

        # Turn right by 90 degrees
    print("Turning right by 90 degrees...")
    yaw_rate = 90  # yaw rate in degrees per second
    turn_duration = 1  # duration in seconds to complete the turn
    client.rotateByYawRateAsync(yaw_rate, turn_duration).join()
    print("Turn completed.")

    # Move forward again in the new direction
    second_duration = 10  # second duration in seconds to move forward after turning
    print("Moving forward in new direction...")
    client.moveByVelocityAsync(0, velocity, 0, second_duration).join()
    print(f"Moving forward at {velocity} m/s for {second_duration} seconds in new direction.")

    # Hover in place after moving
    client.hoverAsync().join()
    print("Movement complete, hovering in place.")

    # Disarm and reset
    client.armDisarm(False)
    client.enableApiControl(False)
    print("Drone command execution complete.")

    # Disarm and reset
    client.armDisarm(False)
    client.enableApiControl(False)
    print("Drone command execution complete.")

# Run the main function
if __name__ == "__main__":
    main()
