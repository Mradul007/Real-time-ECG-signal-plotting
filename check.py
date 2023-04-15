import matplotlib.pyplot as plt
import matplotlib.animation as animation
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import csv
#Hardware SPI configuration:
SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

x_len = 200
# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = list(range(0, 200))
ys = [0] * x_len
ax.set_ylim(100,1300)
# Create a blank line. We will update the line in animate
line, = ax.plot(xs, ys)
#Ecg_data_label
with open('ECG_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Sample", "Data"])
# Add labels
plt.title('Ecg')
# This function is called periodically from FuncAnimation
def animate(i, ys):

    value = mcp.read_adc(0)

    # Add y to list
    ys.append(value)

    # Limit y list to set number of items
    ys = ys[-x_len:]
    
    #append_data_in_csv
    with open('ECG_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([i,ys[x_len-1]])

    # Update line with new Y values
    line.set_ydata(ys)

    return line,

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig,
        animate,
        fargs=(ys,),
        interval=5,
        blit=True)
plt.show()