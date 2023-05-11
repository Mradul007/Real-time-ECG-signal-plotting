import matplotlib.pyplot as plt
import matplotlib.animation as animation
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
from scipy import signal,stats
import multiprocessing
import pandas as pd
import datetime
#Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
dfecg = pd.DataFrame(columns=['Time', 'Sample'])
x_len = 150
# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = list(range(0, x_len))
ys = [0] * x_len
ax.set_ylim(-5,5)
ecg = []
timeecg = []
dfecg = pd.DataFrame(columns=['Time', 'Sample'])
# Create a blank line. We will update the line in animate
line, = ax.plot(xs, ys)
#Ecg_data_label
#with open('ECG_data.csv', 'w', newline='') as file:
    #writer = csv.writer(file)
    #writer.writerow(["Sample", "Data"])
# Add labels
plt.title('Ecg')
ax.set_xlabel('Samples')
ax.set_ylabel('Amplitude(mV)')
#filter
def moving_average(values, window):
    """
    Applies a moving average filter of a given window size to a list of values.

    Args:
        values (list): The input list of values.
        window (int): The size of the moving window.

    Returns:
        A list containing the filtered values.
    """
    # Check if the window size is valid
    if window < 1:
        raise ValueError("Window size must be at least 1.")

    # Initialize the output list
    filtered = []

    # Apply the moving average filter
    for i in range(len(values)):
        if i < window-1:
            # If there are not enough values for the window, use the available values
            window_vals = values[0:i+1]
        else:
            # Use the last 'window' values
            window_vals = values[i-window+1:i+1]

        # Calculate the average of the window
        avg = sum(window_vals) / len(window_vals)

        # Append the filtered value to the output list
        filtered.append(avg)

    return filtered
#sos = signal.butter(2,0.5,btype='highpass',output='sos',fs=200)
# This function is called periodically from FuncAnimation
def animate(i, ys):

    value = mcp.read_adc(0)

    # Add y to list
    ys.append(value)

    # Limit y list to set number of items
    ys = ys[-x_len:]
    y_ = stats.zscore(ys)
    #y1 = signal.sosfilt(sos,ys)
    #y1 = y1[-x_len:]
    y = moving_average(y_,2)
    y = y[-x_len:]
    #append_data_in_csv
    #with open('ECG_data.csv', 'a', newline='') as file:
        #writer = csv.writer(file)
        #writer.writerow([i,ys[x_len-1]])

    # Update line with new Y values
    #line.set_ydata(ys)
    ecg.append(y[x_len-1])
    timeecg.append(datetime.datetime.now())

    line.set_ydata(y)

    return line,

# Set up plot to call animate() function periodically
def loop1():
    ani = animation.FuncAnimation(fig,
        animate,
        fargs=(ys,),
        interval=3,
        blit=True)
    plt.show()
    dfecg['Time'] = timeecg
    dfecg['Sample'] = ecg
    dfecg.to_csv('ECG.csv')


if __name__ == '__main__':
    p1 = multiprocessing.Process(target=loop1)
    p1.start()
    p1.join()
