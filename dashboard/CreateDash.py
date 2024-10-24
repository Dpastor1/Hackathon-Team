import pandas as pd
import matplotlib.pyplot as plt
import os
import time

def main():
    csv_file = init("devnet\sensor_data\sensor_data.csv")
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    statsImg(csv_file)
    path = "devnet/images/" + currImg()
    img = plt.imread(path)
    img2 = plt.imread("myimg.png")
    ti_m = os.path.getmtime(path)
    m_ti = time.ctime(ti_m)
    axs[0].imshow(img)
    axs[0].axis('off')
    axs[0].set_title('Current Image: ' + m_ti)
    axs[1].imshow(img2)
    axs[1].axis('off')
    axs[1].set_title(label="Current Data: " + csv_file.iloc[0, 0].strftime("%a %b %d %H:%M:%S %Y"))
    plt.tight_layout()
    plt.savefig("dashboard.png")

def init(filename):
    csv_file = pd.read_csv("devnet\sensor_data\sensor_data.csv")
    csv_file['date_time'] = pd.to_datetime(csv_file['date_time'])
    csv_file.sort_values(by=['date_time'], inplace=True, ascending=False)
    return csv_file
    
        
def table(csv_file, csv_shape):
    for i in range(csv_shape[0]):
        for j in range(csv_shape[1]):
            print(csv_file.iloc[i, j], end = " | ")
        print("")
        
def currInfo(myDB):
    myString = ""
    for i in range(1, myDB.shape[1]):
        myString = myString + "\n" + myDB.columns[i] + ": " + str(myDB.iloc[0, i]) + "\n"
    return myString

def statsImg(myDB):
    width_px = 1024
    height_px = 768
    dpi = 100
    width_in = width_px / dpi
    height_in = height_px / dpi
    fig = plt.figure(figsize=(width_in, height_in), dpi=dpi)
    plt.text(0.5, 0.5, currInfo(myDB), ha="center", va="center", fontsize = 50)
    plt.axis('off')
    plt.grid(False)
    plt.savefig("myimg.png")
    plt.close(fig)

def currImg():
    directory_path = "devnet\images"
    most_recent_file = None
    most_recent_time = 0
    for entry in os.scandir(directory_path):
        if entry.is_file():
        # get the modification time of the file using entry.stat().st_mtime_ns
            mod_time = entry.stat().st_mtime_ns
            if mod_time > most_recent_time:
            # update the most recent file and its modification time
                most_recent_file = entry.name
                most_recent_time = mod_time
    return most_recent_file

if __name__=="__main__":
    main()