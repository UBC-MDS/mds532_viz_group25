## Reflection on the interactive app

Based on the lab 2 instructions and TA’s feedbacks, the target is to show around 3 plots. Therefore, 
our group has decided to display only two plots rather than five plots on the dashboard. Please see the [link](https://crimeviz.herokuapp.com/) for the prototype of deployed app.

The interactive app is a visualization tool to display violent crimes of 68 U.S. cities over 45 years from 1975 to 2015. It now consists of two side by side plots. The one on the left by default is set to display the evolution of total violent crimes of the city Los Angeles over 45 years. The one on the right is a bar chart that by default is set to display violent crime in four categories of the city Los Angeles in 2015. And each bar has been annotated with label for a quick review. 

We also have implemented a control panel on the left that can facilitate a user to update the bar chart geological and chronically. The bar chart will eventually display the counts of different type of crimes per 100k in the city and the year of interest. 

The control panel consists of three dropdown menus. From top to bottom, they respectively allow a user to choose a state from the “State” menus, a city from the “City” menus, a year from the “Year” menu. 

In order to see a different bar chart, the recommended step would be as follows:
1.	Pick a state. 
2.	Pick a city and note that options in the “City” dropdown menu will be automatically updated based on the value in the “State” dropdown menu. 
3.	Pick a year to display the bar chart.

Moreover, we also implemented a range slider below the line chart for a user to adjust the period. The data spans over 45 years. If a user is interested in seeing the total crime per 100k within a specific period, the user could specify the year range from the slider and the line chart will be updated accordingly.

## Future improvements and additions

We could also include the trend of crimes of each type in the line chart and highlight the result by clicking the legend.









  

 
