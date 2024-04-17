import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from numpy.random import default_rng
import ipywidgets as widgets
from IPython.display import display, clear_output

def generate_polygon(ax, radius, num_sides, center, rotation=0):
    """Generate a regular polygon and add it to the plot."""
    theta = np.linspace(0, 2 * np.pi, num_sides, endpoint=False) + np.deg2rad(rotation)
    points = np.vstack((np.cos(theta), np.sin(theta))).T
    polygon = patches.Polygon(radius * points + center, closed=True, fill=True, edgecolor='none')
    return polygon

def random_color(scheme):
    """Generate a random color based on chosen color scheme."""
    if scheme == 'Bright':
        return np.random.rand(3)
    elif scheme == 'Pastel':
        return np.random.rand(3) * 0.5 + 0.5
    elif scheme == 'Dark':
        return np.random.rand(3) * 0.5

def create_art(num_polygons, num_sides_range, color_scheme, transparency, rotation, positioning, background_color, ax_limits=(-1, 1)):
    rng = default_rng()
    fig, ax = plt.subplots()

    # Set limits, aspect, and figure background color
    fig.patch.set_facecolor(background_color)
    ax.set_xlim(ax_limits)
    ax.set_ylim(ax_limits)
    ax.set_aspect('equal')
    ax.axis('off')  # Hide axes
    ax.set_facecolor(background_color)

    for i in range(num_polygons):
        num_sides = rng.integers(num_sides_range[0], num_sides_range[1] + 1)
        radius = rng.uniform(0.05, 0.3)
        if positioning == 'Random':
            center = rng.uniform(*ax_limits, size=2)
        else:  # Grid positioning
            rows = int(np.sqrt(num_polygons))
            cols = (num_polygons + rows - 1) // rows
            row = i // cols
            col = i % cols
            center = ((2 * col / cols - 1) * ax_limits[1], (2 * row / rows - 1) * ax_limits[1])

        color = random_color(color_scheme)
        polygon = generate_polygon(ax, radius, num_sides, center, rotation * i)
        polygon.set_facecolor(color)
        polygon.set_alpha(transparency)
        ax.add_patch(polygon)

    plt.show()

# Interactive widgets
style = {'description_width': 'initial'}
num_polygons_slider = widgets.IntSlider(value=50, min=10, max=200, step=1, description='Number of Polygons:', style=style)
num_sides_range_slider = widgets.IntRangeSlider(value=[3, 8], min=3, max=12, step=1, description='Sides Range:', style=style)
color_scheme_dropdown = widgets.Dropdown(options=['Bright', 'Pastel', 'Dark'], value='Bright', description='Color Scheme:', style=style)
transparency_slider = widgets.FloatSlider(value=0.5, min=0.1, max=1.0, step=0.1, description='Transparency:', style=style)
rotation_slider = widgets.FloatSlider(value=0, min=0, max=360, step=10, description='Rotation Angle:', style=style)
positioning_toggle = widgets.ToggleButtons(options=['Random', 'Grid'], description='Positioning Strategy:', style=style)
red_slider = widgets.FloatSlider(value=1.0, min=0, max=1.0, step=0.01, description='Red:', style=style)
green_slider = widgets.FloatSlider(value=1.0, min=0, max=1.0, step=0.01, description='Green:', style=style)
blue_slider = widgets.FloatSlider(value=1.0, min=0, max=1.0, step=0.01, description='Blue:', style=style)
button = widgets.Button(description="Generate Art")

def on_button_clicked(b):
    with output:
        clear_output(wait=True)
        background_color = (red_slider.value, green_slider.value, blue_slider.value)
        create_art(
            num_polygons_slider.value, 
            num_sides_range_slider.value, 
            color_scheme_dropdown.value,
            transparency_slider.value, 
            np.deg2rad(rotation_slider.value),
            positioning_toggle.value,
            background_color
        )

button.on_click(on_button_clicked)
output = widgets.Output()

display(widgets.VBox([
    num_polygons_slider, 
    num_sides_range_slider, 
    color_scheme_dropdown, 
    transparency_slider,
    rotation_slider,
    positioning_toggle,
    widgets.HBox([red_slider, green_slider, blue_slider]),
    button, 
    output
]))
