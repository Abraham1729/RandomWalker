import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox

# Create the first figure for the line plot
fig1, ax1 = plt.subplots()
ax1.plot([1, 2, 3, 4, 5], [1, 2, 1, 4, 3])

# Create the second figure for the widget
fig2, ax2 = plt.subplots()
ax2.axis('off')  # Turn off axes for the widget figure

# Create a text box widget
textbox = TextBox(ax2, 'Enter Text:', initial="Hello, Matplotlib!")

def submit(text):
    print("Entered text:", text)

textbox.on_submit(submit)

plt.show()
