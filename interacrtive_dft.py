import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor, Button

# Constants
N = 16  # Number of points
# x = np.zeros(N)  # Initialize x[n] with zeros
x = np.array([ 5.     ,     3.74357912 , 2.5119328  , 1.   ,       0.    ,     -1.
, -2.   ,      -3.64629878 ,-3.88315384 ,-3.64629878 ,-2.      ,   -1.
,  0.  ,        1.     ,     2.5119328  , 3.74357912])
threshold = 5e-1

# DFT Calculation
def compute_dft(x):
    X = np.fft.fft(x)
    X_magnitude = X
    X_phase = np.angle(X)
    return X_magnitude, X_phase

# Update the DFT plot based on the new x[n]
def update_dft_plot():
    X_magnitude, X_phase = compute_dft(x)
    stem2_mag_lines.set_ydata(X_magnitude)
    stem2_phase_lines.set_ydata(X_phase)
    
    # Update grey points for X_magnitude
    for n in range(1, N-1):
        grey_magnitude_values[n-1] = (X_magnitude[0] + X_magnitude[(2*n)%N]) / 2
    grey_mag_line.set_ydata(grey_magnitude_values)

    ax2.relim()
    ax2.autoscale_view()
    plt.draw()

# Update the grey points (average of neighbors) for x[n]
def update_grey_points():
    for n in range(1, N-1):
        grey_values[n-1] = (x[n-1] + x[n+1]) / 2
    grey_line.set_ydata(grey_values)
    plt.draw()

# Handle clicks on the x[n] plot
def on_click(event):
    if event.inaxes == ax1:
        n = int(round(event.xdata))
        if 0 <= n <= N // 2:
            y_value = event.ydata
            if event.key != 'shift':  # Snap to nearest integer if Shift is not held
                if abs(y_value-round(y_value)) < threshold:
                    y_value = round(y_value)
            x[n] = y_value
            if n!=0:
                x[N-n] = y_value  # Mirror around N/2
            stem1_lines.set_ydata(x)
            update_grey_points()
            update_dft_plot()

# Handle dragging on the x[n] plot
def on_motion(event):
    if event.inaxes == ax1 and event.button == 1:
        n = int(round(event.xdata))
        if 0 <= n <= N // 2:
            y_value = event.ydata
            if event.key != 'shift':  # Snap to nearest integer if Shift is not held
                if abs(y_value-round(y_value)) < threshold:
                    y_value = round(y_value)
            x[n] = y_value
            if n != 0:
                x[N-n] = y_value  # Mirror around N/2
            stem1_lines.set_ydata(x)
            update_grey_points()
            update_dft_plot()

# Reset function
def reset(event):
    global x
    x = np.zeros(N)  # Reset x[n] to zeros
    stem1_lines.set_ydata(x)  # Update the x[n] plot
    update_grey_points()  # Update grey points
    update_dft_plot()  # Update DFT plot

# Print function
def print_values(event):
    X_magnitude, X_phase = compute_dft(x)
    print("x[n]:", repr(x))
    print("X[k] (DFT Magnitude):", repr(np.real(X_magnitude)))
    print("X[k] (DFT Phase):", X_phase)

# Initialize the plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Plot x[n]
n_vals = np.arange(N)
markers, stemlines, baseline = ax1.stem(n_vals, x)
stem1_lines = markers
ax1.set_xlim(-1, N)
ax1.set_ylim(-N, N)
ax1.set_yticks([])  # Remove y-axis numbers
ax1.set_yticks(np.arange(-N, N+1, 1))  # Increase the number of horizontal gridlines
ax1.grid(True)
ax1.set_title("x[n] vs n")
ax1.set_xlabel("n")
ax1.set_ylabel("x[n]")

# Plot the grey points (average of neighbors) for x[n]
grey_values = np.zeros(N-2)  # Grey points for n=1 to N-2
grey_line, = ax1.plot(n_vals[1:-1], grey_values, 'o', color='grey', alpha=0.5)

# Add a cursor for easier point selection
cursor = Cursor(ax1, useblit=True, color='red', linewidth=1)

# Plot DFT
X_magnitude, X_phase = compute_dft(x)
markers_mag, stemlines_mag, baseline_mag = ax2.stem(n_vals, X_magnitude, linefmt='b', markerfmt='bo', basefmt='r')
markers_phase, stemlines_phase, baseline_phase = ax2.stem(n_vals, X_phase, linefmt='g', markerfmt='go', basefmt='r')
stem2_mag_lines = markers_mag
stem2_phase_lines = markers_phase
ax2.set_xlim(0, N-1)
ax2.set_yticks([])  # Remove y-axis numbers
ax2.grid(True)
ax2.set_title("DFT Magnitude (blue) and Phase (green)")
ax2.set_xlabel("Frequency Index")
ax2.set_ylabel("Magnitude / Phase")

# Plot the grey points (average of neighbors) for X_magnitude
grey_magnitude_values = np.zeros(N-2)  # Grey points for magnitude n=1 to N-2
grey_mag_line, = ax2.plot(n_vals[1:-1], grey_magnitude_values, 'o', color='grey', alpha=0.5)

# Add a reset button
reset_ax = plt.axes([0.75, 0.01, 0.1, 0.05])  # Position for the reset button
reset_button = Button(reset_ax, 'Reset', color='lightgrey', hovercolor='lightblue')
reset_button.on_clicked(reset)

# Add a print button
print_ax = plt.axes([0.6, 0.01, 0.1, 0.05])  # Position for the print button
print_button = Button(print_ax, 'Print', color='lightgrey', hovercolor='lightblue')
print_button.on_clicked(print_values)

# Connect the event handlers
fig.canvas.mpl_connect('button_press_event', on_click)
fig.canvas.mpl_connect('motion_notify_event', on_motion)

plt.tight_layout()
plt.show()
