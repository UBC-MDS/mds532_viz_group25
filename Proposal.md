# Motivation and purpose

Our role: Data scientist consultancy firm

Target audience: People considering moving into a new city.

Safety is one of the most significant factors that affect people's decisions on where to live. Everyone wants to live in a peaceful city, but usually it is not easy to make the right choice. Searching over Internet for crime-related news happened within a specific location is often very time-consuming, and find the . Our app will show the distribution of serious violent crime cases happened in 68 police jurisdictions and also the changes in number of crimes over recent 40 years in each of these 68 polic jurisdictions.

# Description of the data

We will be visualizing the dataset of serious violent crime cases happened in 68 police jurisdictions over 40 years. This [city crime dataset](https://github.com/themarshallproject/city-crime) is contributed by Gabriel Dance, Tom Meagher, and Emily Hopkins from the Marshall Project. It contains 2829 entries. Each of the entries denotes a report of crimes happened in a specific location in a specific year. 

The column `ORI` is an identifier for each police jurisdiction and the column `department_name` is the name of the department. The column `total_pop` represents the number of residents living under the specific police jurisdiction. 

The dataset includes information about four types of major violent crimes: homicide, rape, robbery and aggravated assault. Column `violent_crime` is the total number of violent crimes happened and  `homs_sum`, `rape_sum`, `rob_sum` and `agg_ass_sum` are the number of crime cases of each of the categories respectively. Column `violent_per_100k` is the average number of violent crimes within every 100 thousands residents in that city.


# Research questions and usage scenario

## Research questions

Safety is one of the biggest concerns for people who are considering to relocate.  It then boils down to the question "Where is safe now and would the city remain safe in the future?"  The research question can be further split into following questions:

1. Which is the safest state ?

2. Which city is the safest in the state?

3. The total number of violent crimes in this city is increasing or decreasing over the recent decade?

## Usage scenario

John Doe has spent his entire life in his hometown. He never sets his foot into another city. One day, the idea of moving into a new city to explore and meet new people kicks in. He then decides to spend his life after retirement in another US city, and/or in a different state. In order to achieve his goal, John Doe has been working very hard, now the day has finally come.  Among all the factors of moving into a city, John Doe want to first find out the saftest cities. For sure, He would love to avoid any hiccups from criminal conducts at his age.

The whole process of moving into a new city can be very stressful and time consuming. He has limit time/budgets to conduct a comprehensive analysis. He is seeking a quick answer to address his concerns regarding safety. The visualization tool, city crime visualizer, can serve this purpose. The app can display the crime data from 68 US cities over 4 decades in a fast and effective way. He can first quickly understand how the violent crimes evolve in different states. By comparison, he can filter out saftest states by look at the total number of crimes in the recent 5 years. Furthermore, he can find out cities with lowest number of crimes in the selected states. The app also displays the violent crime in four categories. Just in case, he is more concerned about any specific type of crime. 

After a quick exploration, he can make a list of safest cities. With this info in mind, he can explore other factors such as weather, pleasurable activities and the cost of living of these candidate cities. 



