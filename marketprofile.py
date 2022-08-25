from matplotlib.widgets import Slider, Button
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys

trade_pair = "xmrusdt"
file = input("Choose file from 'extracting.py': (-1, 0, 1):  ")
config_name = f"config/{trade_pair}/{trade_pair}_config_{file}.json"
filename = f"extracted_trades/{trade_pair}/extracted_trades_{trade_pair}_{file}.csv"
# step 10min * 60s * 1000ms
step = 10 * 60 * 1000


# Import Data
def read_data(file_name):
    df = pd.read_csv(file_name, usecols=['Time', 'Price', 'Amount Bought', 'Sum of Delta', 'Amount Sold'])
    global x, y1, y2, y3, y4
    x = df['Time']
    y1 = df['Price']
    y2 = df['Sum of Delta']
    y3 = df['Amount Bought']
    y4 = df['Amount Sold']


def drawing_plots(refresh: bool = False):
    global ax1, ax2, ax3, ax4
    # loading data from file to global variables:
    read_data(filename)
    # Plot Line 1 (Left Y Axis)
    if not refresh:
        fig, ax1 = plt.subplots(figsize=(16, 8), dpi=90)
        plt.subplots_adjust(left=0.05, bottom=0.16)

    ax1.plot(x, y1, 'k-')
    ax1.grid('minor')

    # Plot Line 2 (Right Y Axis)
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.plot(x, y2, 'b-')

    # Plot Line 3 (Right Y Axis)
    ax3 = ax1.twinx()
    ax3.plot(x, y3, 'g-', alpha=0.3)
    ax3.spines.right.set_position(("axes", 1.045))

    # Plot Line 4 (Right Y Axis)
    ax4 = ax1.twinx()
    ax4.plot(x, y4, 'r-', alpha=0.3)
    ax4.spines.right.set_position(("axes", 1.09))


def autoscale_y(ax, margin=0.05):
    def get_bottom_top(line):
        xd = line.get_xdata()
        yd = line.get_ydata()
        lo, hi = ax1.get_xlim()
        y_displayed = yd[((xd > lo) & (xd < hi))]
        h = np.max(y_displayed) - np.min(y_displayed)
        bot = np.min(y_displayed) - margin * h
        top = np.max(y_displayed) + margin * h
        return bot, top

    lines = ax.get_lines()
    bot, top = np.inf, -np.inf

    for line in lines:
        new_bot, new_top = get_bottom_top(line)
        if new_bot < bot:
            bot = new_bot
        if new_top > top:
            top = new_top

    ax.set_ylim(bot, top)


def resetSliders(event):
    slider1.valmax = (max(x) + step)
    slider2.reset()
    slider1.reset()


def setvalue_butt24(val):
    slider2.set_val(slider1.val - 24 * 60 * 60 * 1000)


def setvalue_butt12(val):
    slider2.set_val(slider1.val - 12 * 60 * 60 * 1000)


def setvalue_butt4(val):
    slider2.set_val(slider1.val - 4 * 60 * 60 * 1000)


def setvalue_butt1(val):
    slider2.set_val(slider1.val - 1 * 60 * 60 * 1000)


def hour_left(val):
    slider2.set_val(slider2.val - 1 * 60 * 60 * 1000)
    slider1.set_val(slider1.val - 1 * 60 * 60 * 1000)


def hour_right(val):
    slider1.set_val(slider1.val + 1 * 60 * 60 * 1000)
    slider2.set_val(slider2.val + 1 * 60 * 60 * 1000)


def move_left_L(hour):
    slider2.set_val(slider2.val - 60 * 60 * 1000)


def move_right_L(hour):
    slider2.set_val(slider2.val + 60 * 60 * 1000)


def move_left_R(hour):
    slider1.set_val(slider1.val - 60 * 60 * 1000)


def move_right_R(hour):
    slider1.set_val(slider1.val + 60 * 60 * 1000)


def move_left_L4(val):
    slider2.set_val(slider2.val - 4 * 60 * 60 * 1000)


def move_right_L4(val):
    slider2.set_val(slider2.val + 4 * 60 * 60 * 1000)


def move_left_R4(val):
    slider1.set_val(slider1.val - 4 * 60 * 60 * 1000)


def move_right_R4(val):
    slider1.set_val(slider1.val + 4 * 60 * 60 * 1000)


def refresh_all(event):
    ax1.cla()
    ax2.cla()
    ax3.cla()
    ax4.cla()

    drawing_plots(refresh=True)

    slider1.valmax = max(x) + step
    slider1.set_val(max(x) + step)


def valupdate1(val):
    xval = slider1.val
    ax1.set_xlim(left=slider2.val, right=xval)
    autoscale_y(ax1)
    autoscale_y(ax2)
    autoscale_y(ax3)
    plt.draw()


def valupdate2(val):
    xval = slider2.val
    ax2.set_xlim(left=xval, right=slider1.val)
    autoscale_y(ax1)
    autoscale_y(ax2)
    autoscale_y(ax3)
    plt.draw()


def exit_program(event):
    sys.exit("Program Closed")


# First plot:
drawing_plots()

# Making Slider 1 for MinX Value:
axSlider1 = plt.axes([0.1, 0.08, 0.8, 0.02])
slider1 = Slider(axSlider1, "Max Time Range", valmin=min(x), valmax=max(x), valinit=max(x), valstep=step, color='red')

axSlider2 = plt.axes([0.1, 0.05, 0.8, 0.02])
slider2 = Slider(axSlider2, "Min Time Range", valmin=min(x), valmax=max(x), valstep=step, slidermax=slider1, color='green')

# Buttons:
axButton24h = plt.axes([0.1, 0.91, 0.02, 0.03])
btn24h = Button(axButton24h, '24H')

axButton12h = plt.axes([0.125, 0.91, 0.02, 0.03])
btn12h = Button(axButton12h, '12H')

axButton4h = plt.axes([0.15, 0.91, 0.02, 0.03])
btn4h = Button(axButton4h, '4H')

axButton1h = plt.axes([0.175, 0.91, 0.02, 0.03])
btn1h = Button(axButton1h, '1H')

axButtonReset = plt.axes([0.2, 0.91, 0.03, 0.03])
btnReset = Button(axButtonReset, 'Reset')

axButtonRefresh = plt.axes([0.28, 0.91, 0.06, 0.06])
btnRefresh = Button(axButtonRefresh, 'Refresh\nChart')

axButton_moveleft = plt.axes([0.4, 0.91, 0.03, 0.03])
btn_ML = Button(axButton_moveleft, '<<')

axButton_moveright = plt.axes([0.435, 0.91, 0.03, 0.03])
btn_MR = Button(axButton_moveright, '>>')

axButton_minusleft_1 = plt.axes([0.47, 0.91, 0.03, 0.03])
btn_minusL_1 = Button(axButton_minusleft_1, '<-1HL')

axButton_minusleft_4 = plt.axes([0.47, 0.94, 0.03, 0.03])
btn_minusL_4 = Button(axButton_minusleft_4, '<-4HL')

axButton_plusleft_1 = plt.axes([0.505, 0.91, 0.03, 0.03])
btn_plusL_1 = Button(axButton_plusleft_1, '1HL+>')

axButton_plusleft_4 = plt.axes([0.505, 0.94, 0.03, 0.03])
btn_plusL_4 = Button(axButton_plusleft_4, '4HL+>')

axButton_minusright_1 = plt.axes([0.54, 0.91, 0.03, 0.03])
btn_minusR_1 = Button(axButton_minusright_1, '<-1HR')

axButton_minusright_4 = plt.axes([0.54, 0.94, 0.03, 0.03])
btn_minusR_4 = Button(axButton_minusright_4, '<-4HR')

axButton_plusright_1 = plt.axes([0.575, 0.91, 0.03, 0.03])
btn_plusR_1 = Button(axButton_plusright_1, '1HR+>')

axButton_plusright_4 = plt.axes([0.575, 0.94, 0.03, 0.03])
btn_plusR_4 = Button(axButton_plusright_4, '4HR+>')

axButton_exit = plt.axes([0.85, 0.91, 0.04, 0.03])
btn_exit = Button(axButton_exit, 'EXIT')

# Sliders change:
slider1.on_changed(valupdate1)
slider2.on_changed(valupdate2)

# Buttons calls:
btnRefresh.on_clicked(refresh_all)
btnReset.on_clicked(resetSliders)

btn24h.on_clicked(setvalue_butt24)
btn12h.on_clicked(setvalue_butt12)
btn4h.on_clicked(setvalue_butt4)
btn1h.on_clicked(setvalue_butt1)

btn_ML.on_clicked(hour_left)
btn_MR.on_clicked(hour_right)

btn_minusL_1.on_clicked(move_left_L)
btn_plusL_1.on_clicked(move_right_L)
btn_minusR_1.on_clicked(move_left_R)
btn_plusR_1.on_clicked(move_right_R)

btn_minusL_4.on_clicked(move_left_L4)
btn_plusL_4.on_clicked(move_right_L4)
btn_minusR_4.on_clicked(move_left_R4)
btn_plusR_4.on_clicked(move_right_R4)

btn_exit.on_clicked(exit_program)

plt.show()

print("------------")
