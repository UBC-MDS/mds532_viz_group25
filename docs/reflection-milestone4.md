## Reflection on the interactive app

We have successfully implemented a production-ready dashboard in Python and added some major improvements in response to suggestions from feedbacks. The production-ready dashboard was improved based on the previous Python-version skeleton app. 

#### Update 1 : 

To add more layers of complexity, our team decides to include a  map of the U.S. together with dropdown menus to facilitate users to visualize how each type of violent crime is distributed in the states on each year. After picking the crime type on a specific year from the dropdown menus on the left, the map will be decorated with colors. States with darker color represent a higher number of the violent crime. 

#### Update 2 :  

The line chart has included the evolutions of each type of violent crime in addition to the total crime. If the city is not specified, the line chart is set to show the summative results of the selected state. The line chart will be updated to show the results of a city if a user selects one. Furthermore, if a user hovers over points on the line chart, the corresponding value can be viewed. 

#### Update 3 :  

Similarly, if the city is not specified, the bar chart is set to show the summative results of the selected state. The bar chart will be updated to show the results of a city if a user selects one.


#### Update 4:  

We successfully achieve to set up Heroku's GitHub integration to automate the deploys.

#### Update 5:  

Aesthetical improvement is done on the slider bar to include notches

#### Future improvements and final remarks

We appreciate all the feedbacks that give an insight into a different perspective for the same problem that we were trying to solve. We hope the app turns out to be user friendly and easy to use as we expect. 

The styling of the dashboard can be further improved. We can add 'Cards' to make tidy the dashboard. We also tried to implement more interactivities among plots. However, we create the plots separately in different callback functions, hence, we could not figure out an efficient way to make connections between plots. The app is far near perfect, however, we are happy for what we can achieve in a short time. 

Go team 25!