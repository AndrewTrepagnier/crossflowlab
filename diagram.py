import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Create figure and axis
fig, ax = plt.subplots(figsize=(7, 6))

# Read and display the PNG directly
img = mpimg.imread("diagram_png_folder/crossflowlab.drawio.png")
ax.imshow(img, aspect='auto', zorder=0) # zorder=0 puts the image in the back

# Add a label with specific position and styling
# x and y are in data coordinates (0 to 1 for normalized coordinates)
ax.text(x=122, y=57, # Position (center of the plot)
s="Coolant", # The text to display
fontsize=12, # Size of the text
color='red', # Text color
ha='center', # Horizontal alignment ('left', 'center', 'right')
va='center', # Vertical alignment ('top', 'center', 'bottom')
zorder=2, # Higher zorder puts it on top of the image
bbox=dict( # Optional: add a box around the text
facecolor='white',
alpha=0.7,
edgecolor='red',
boxstyle='round,pad=0.5'
))

ax.text(x=495, y=172, # Position (center of the plot)
s="Air", # The text to display
fontsize=12, # Size of the text
color='blue', # Text color
ha='center', # Horizontal alignment ('left', 'center', 'right')
va='center', # Vertical alignment ('top', 'center', 'bottom')
zorder=2, # Higher zorder puts it on top of the image
bbox=dict( # Optional: add a box around the text
facecolor='white',
alpha=0.7,
edgecolor='blue',
boxstyle='round,pad=0.5'
))

# Rotated "Fin Length" labels
ax.text(x=429, y=13,
s="Fin Length",
fontsize=10,
color='red',
ha='left',
va='top',
rotation=0, # Rotate 45 degrees
zorder=2)

ax.text(x=375, y=104,
s="Fin Width",
fontsize=10,
color='red',
ha='left',
va='top',
rotation=28, # Rotate -45 degrees
zorder=2)

ax.axis('off') # Hide axes
plt.tight_layout()
plt.show()