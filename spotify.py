#!/usr/bin/env python
# coding: utf-8

# # <center>Top Spotify Song</center>

# ## Adding Interaction

# In[1]:


import pandas as pd
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import CategoricalColorMapper
from bokeh.palettes import Category20
from bokeh.layouts import widgetbox, row, gridplot
from bokeh.models import Slider, Select


# In[2]:


data = pd.read_csv(r"C:\Users\Tami\Downloads\Tubes visdat\top10s.csv")
data.set_index('year', inplace=True)
data.head()


# In[3]:


# Make a list of the unique values from the region column: regions_list
genre = data.top_genre.unique().tolist()

# Make a color mapper: color_mapper
color_mapper = CategoricalColorMapper(factors=genre, palette=Category20[20])


# In[4]:
# Make the ColumnDataSource: source
source = ColumnDataSource(data={
    'x'       : data.loc[2010].bpm,
    'y'       : data.loc[2010].nrgy,
    'Title'   : data.loc[2010].title,
    'id'      : (data.loc[2010].ID / 20000000) + 2,
    'genre'   : data.loc[2010].top_genre,
})



# In[ ]:


# Create the figure: plot
plot = figure(title='2010', x_axis_label='bpm', y_axis_label='nrgy',
           plot_height=1000, plot_width=1000, tools=[HoverTool(tooltips='@Title')])

# Add a circle glyph to the figure p
plot.circle(x='x', y='y', source=source, fill_alpha=0.8,
           color=dict(field='genre', transform=color_mapper), legend='genre')

# Set the legend and axis attributes
plot.legend.location = 'bottom_left'


# Define the callback function: update_plot
def update_plot(attr, old, new):
    # set the `yr` name to `slider.value` and `source.data = new_data`
    yr = slider.value
    x = x_select.value
    y = y_select.value
    # Label axes of plot
    plot.xaxis.axis_label = x
    plot.yaxis.axis_label = y
    # new data
    new_data = {
    'x'       : data.loc[yr][x],
    'y'       : data.loc[yr][y],
    'genre'   : data.loc[yr].top_genre,
    'id'      : (data.loc[yr].ID / 20000000) + 2,
    'Title'   : data.loc[yr].title,
    }
    source.data = new_data
    
    # Add title to figure: plot.title.text
    plot.title.text = 'Gapminder data for %d' % yr

# Make a slider object: slider
slider = Slider(start=2010, end=2019, step=1, value=2010, title='year')
slider.on_change('value',update_plot)

# Make dropdown menu for x and y axis
# Create a dropdown Select widget for the x data: x_select
x_select = Select(
    options=['bpm', 'nrgy', 'val', 'pop'],
    value='bpm',
    title='x-axis data'
)
# Attach the update_plot callback to the 'value' property of x_select
x_select.on_change('value', update_plot)

# Create a dropdown Select widget for the y data: y_select
y_select = Select(
    options=['bpm', 'nrgy', 'val', 'pop'],
    value='nrgy',
    title='y-axis data'
)
# Attach the update_plot callback to the 'value' property of y_select
y_select.on_change('value', update_plot)
    
# Create layout and add to current document
layout = row(widgetbox(slider, x_select, y_select), plot)
curdoc().add_root(layout)


# In[5]:


# bokeh serve --show myapp.py


# For more on all things interaction in Bokeh, [**Adding Interactions**](https://docs.bokeh.org/en/latest/docs/user_guide/interaction.html) in the Bokeh User Guide is a great place to start.

# In[ ]:




