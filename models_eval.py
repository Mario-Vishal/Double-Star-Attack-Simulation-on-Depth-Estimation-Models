import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def load_images_from_folder(folder, prefix):
    images = {}
    for filename in sorted(os.listdir(folder)):
        if filename.startswith(prefix) and filename.endswith(".png"):
            img_id = int(filename.split('_')[-1].split('.')[0])  # Extract ID from filename
            img = cv2.imread(os.path.join(folder, filename), cv2.IMREAD_UNCHANGED)
            if img is not None:
                images[img_id] = img
    return images

def calculate_mse(image_a, image_b):
    # Ensure both images are the same size by resizing both to a common size
    # Here, I'm choosing to resize to the size of the first image, or you could choose a fixed size
    height, width = image_a.shape[:2]
    image_b_resized = cv2.resize(image_b, (width, height), interpolation=cv2.INTER_LINEAR)

    # Calculate MSE
    return np.mean((image_a - image_b_resized) ** 2)

def plot_depth_profiles(ground_truth, predictions, img_id, graph_output_dir):
    plt.figure()
    # Assuming depth maps and ground truth are single-channel images, select a middle row
    mid_row = ground_truth.shape[0] // 2
    plt.plot(ground_truth[mid_row, :], label='Ground Truth')

    for model_name, pred_image in predictions.items():
        plt.plot(pred_image[mid_row, :], label=f'{model_name} Prediction')

    plt.title(f'Depth Profile Comparison for Image ID {img_id}')
    plt.xlabel('Pixel Position')
    plt.ylabel('Depth Value')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(graph_output_dir, f'depth_profile_comparison_{img_id}.png'))
    plt.close()

def calculate_average_depth(image):
    return np.mean(image)

def plot_error_map(ground_truth, prediction, img_id, output_dir):
    # Ensure both images are the same size by resizing prediction to ground_truth dimensions
    if ground_truth.shape != prediction.shape:
        prediction = cv2.resize(prediction, (ground_truth.shape[1], ground_truth.shape[0]), interpolation=cv2.INTER_LINEAR)

    # Calculate the absolute error
    error = np.abs(ground_truth.astype(np.float32) - prediction.astype(np.float32))

    # Create an error map using a colormap to visualize the depth errors
    plt.figure(figsize=(10, 5))
    plt.imshow(error, cmap='hot', interpolation='nearest')
    plt.colorbar(label='Error')
    plt.title(f'Error Map for Image ID {img_id}')
    plt.axis('off')  # Hide axes ticks

    # Save the error map
    error_map_filename = os.path.join(output_dir, f'error_map_{img_id}.png')
    plt.savefig(error_map_filename)
    plt.close()  # Close the plot to free up memory
    print(f"Saved error map as {error_map_filename}")



def main():
    # Directories
    base_dir = "D:\\final_project\\py_scripts"
    ground_truth_dir = os.path.join(base_dir, "output_data")
    model_dirs = {
        "dispnet": os.path.join(base_dir, "dispnet_output"),
        "monodepth": os.path.join(base_dir, "monodepth_output"),
        "psmnet": os.path.join(base_dir, "psmnet_output")
    }
    graph_output_dir = os.path.join(base_dir, "graph_outputs")
    os.makedirs(graph_output_dir, exist_ok=True)

    # Load ground truth images
    ground_truth_images = load_images_from_folder(ground_truth_dir, "depth")

    # Model performance storage
    model_performance = {model: [] for model in model_dirs}

    # Process each model
    for model_name, dir_path in model_dirs.items():
        model_images = load_images_from_folder(dir_path, model_name)
        for img_id in sorted(ground_truth_images.keys()):
            if img_id in model_images:
                mse = calculate_mse(ground_truth_images[img_id], model_images[img_id])
                model_performance[model_name].append((img_id, mse))
            if img_id==12:
                plot_error_map(ground_truth_images[img_id],model_images[img_id],12,graph_output_dir)

    # Plotting results
    plt.figure(figsize=(10, 5))
    for model_name, performance in model_performance.items():
        if performance:
            ids, errors = zip(*performance)
            plt.plot(ids, errors, label=f'{model_name} MSE')

    plt.xlabel('Image ID')
    plt.ylabel('Mean Squared Error')
    plt.title('Comparison of Depth Model Performance')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(graph_output_dir, 'model_comparison.png'))
    plt.show()

    model_averages = {model: [] for model in model_dirs}
    gt_averages = []

    for img_id in sorted(ground_truth_images.keys()):
        gt_avg = calculate_average_depth(ground_truth_images[img_id])
        gt_averages.append((img_id, gt_avg))

        for model_name, dir_path in model_dirs.items():
            model_images = load_images_from_folder(dir_path, model_name)
            if img_id in model_images:
                model_avg = calculate_average_depth(model_images[img_id])
                model_averages[model_name].append((img_id, model_avg))

    plt.figure(figsize=(10, 5))
    ids, averages = zip(*gt_averages)
    plt.plot(ids, averages, label='Ground Truth', marker='o')

    for model_name, averages in model_averages.items():
        if averages:
            ids, model_avgs = zip(*averages)
            plt.plot(ids, model_avgs, label=f'{model_name}', marker='x')

    plt.xlabel('Image ID')
    plt.ylabel('Average Depth Value')
    plt.title('Average Depth Comparison Across Models')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(graph_output_dir, 'average_depth_comparison.png'))
    plt.show()

    # Create table for images 7 to 14
    summary_data = {'ID': list(range(7, 15))}
    summary_data['Ground Truth'] = [gt_averages[id][1] for id in range(7, 15) if id in dict(gt_averages)]

    for model_name, avgs in model_averages.items():
        avgs_dict = dict(avgs)
        summary_data[model_name] = [avgs_dict.get(id, np.nan) for id in range(7, 15)]
    
    # Debugging line: Check if all lists in summary_data are of the same length
    for key, value in summary_data.items():
        print(f"Length of data for {key}: {len(value)}")

    summary_df = pd.DataFrame(summary_data)
    print(summary_df)
    summary_df.to_csv(os.path.join(graph_output_dir, 'depth_summary_7_to_14.csv'), index=False)

if __name__ == "__main__":
    main()
