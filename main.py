#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Haomiao Han
@version: 09-22-2018

Data source: Bureau of Transportation Statistics, U.S. Department of Transportation
(https://www.transtats.bts.gov/ONTIME/Arrivals.aspx)
"""

import csv
import pylab

#function for drawing the plot graph
def draw_plot_graph(airline1, airline2, airline3, airline4, data1, data2, data3, data4):
    
    #setting up data to be plotted
    pylab.clf()
    
    months_str = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'
    months = months_str.split()
    x = list(range(0,12))
    pylab.xticks(x, months)
    
    pylab.xlabel('Month')
    pylab.ylabel('Average Arrival Delay Per Flight (Minutes)')
    pylab.title('Average Delay Time Per Arriving Flight at New York-LaGuardia in 2017')
    
    #plotting graph according to user input
    if not(airline1 == None) and not(data1 == None):
        pylab.plot(x, data1, color='blue', label=airline1)
    if not(airline2 == None) and not(data2 == None):
        pylab.plot(x, data2, color='red', label=airline2)
    if not(airline3 == None) and not(data3 == None):
        pylab.plot(x, data3, color='green', label=airline3)
    if not(airline4 == None) and not(data4 == None):
        pylab.plot(x, data4, color='orange', label=airline4)
    
    pylab.legend(loc='upper right')
    pylab.show()
    
#function for drawing the first bar chart
def draw_bar_graph(data, xlabel, title):
    
    #since the original data is in an array of key-value pairs,
    #we need to break them down into two arrays first
    x_list = []
    delay_time_data = []
    for city in data:
        x_list.append(city[0])
        delay_time_data.append(city[1])
    
    #then we can draw the graph
    x = list(range(0,10))
    pylab.xticks(x, x_list)
    
    pylab.xlabel(xlabel)
    pylab.ylabel('Average Arrival Delay Per Flight (Minutes)')
    pylab.title(title)
    
    pylab.bar(x, delay_time_data, color='purple', label=xlabel)
    pylab.show()

#function for drawing the second bar chart  
def draw_bar_graph2(data, xlabel, title):
    
    #preparing data to be plotted
    x_list = list(data.keys())
    delay_time_data = list(data.values())
    
    #plotting the graph
    x = list(range(0,4))
    pylab.xticks(x, x_list)
    pylab.xlabel(xlabel)
    pylab.ylabel('Average Arrival Delay Per Flight (Minutes)')
    pylab.title(title)
    pylab.bar(x, delay_time_data, color='purple', label=xlabel)
    
    pylab.show()
    
#function for drawing the 2 pie graphs
def draw_pie_graph(data, title):
    pylab.figure(1,figsize=(6,6))
    pylab.axis('equal')
    
    airlines = list(data.keys())
    total_delay_time = list(data.values())
    
    pylab.pie(total_delay_time, explode=None, labels=airlines, autopct='%1.1f%%')
    pylab.title(title)
    pylab.show()

#accessing the processed csv file

try:
    file = open('combined-delays-lga.csv', 'r')
except Exception as e:
    print("Cannot open the file; error found: ", e)
else:
    #setting up variables
    original_data = csv.reader(file, delimiter=',', quotechar='"')
    data_list = []
    
    #preprocessing the file by removing unnecessary rows
    for line in original_data:
        if (len(line) > 5) and (line[0] != "Carrier Code"):
            data_list.append(line)
    
    #part 1: an interactive graph
    #prompt user to enter the airline         
    airline_choice_str = input("Please enter the airline code: you can enter AA, DL, WN, UA (lower case is fine), or any combination of these, separated by a comma (e.g. aa,dl or WN,UA; no spaces): ")
    airline_choice = airline_choice_str.upper().split(",")
    if (len(airline_choice)) == 0:
        print("please enter valid airline code(s)!")
    else:
        #creating 2 dictionaries, one with airlines & their total delay time per month,
        #and one with airlines & their total number of flights per month
        airline_data_dict = {'AA': [0] * 12, 'WN': [0] * 12, 'DL': [0] * 12, 'UA': [0] * 12}
        airline_flights_dict = {'AA': [0] * 12, 'WN': [0] * 12, 'DL': [0] * 12, 'UA': [0] * 12}
        
        #processing the data
        for flight in data_list:
            #print(flight)
            delay_time = flight[9]
            month_key = int(flight[1][0:2])
            month_index = month_key - 1
            airline_key = flight[0]
            
            airline_data_dict[airline_key][month_index] += int(delay_time)
            airline_flights_dict[airline_key][month_index] += 1
        
        #getting the average delay time per flight by month
        for airline in airline_data_dict:
            for i in range(0,12): 
                airline_data_dict[airline][i] = airline_data_dict[airline][i] / airline_flights_dict[airline][i]
        
        #preparing to draw the graph
        if "AA" in airline_choice:
            a1 = "American (AA)"
            d1 = airline_data_dict["AA"]
        else:
            a1 = None
            d1 = None
            
        if "DL" in airline_choice:
            a2 = "Delta (DL)"
            d2 = airline_data_dict["DL"]
        else:
            a2 = None
            d2 = None
            
        if "UA" in airline_choice:
            a3 = "United (UA)"
            d3 = airline_data_dict["UA"]
        else:
            a3 = None
            d3 = None
            
        if "WN" in airline_choice:
            a4 = "Southwest (WN)"
            d4 = airline_data_dict["WN"]
        else:
            a4 = None
            d4 = None
    
        #drawing the graph
        draw_plot_graph(a1,a2,a3,a4,d1,d2,d3,d4)
    
    #part2: other data (non-interactive)
    cities_dict = {}
    cities_flights_dict = {}
    total_delay_time_dict = {}
    total_flights_dict = {}
    
    #processing the data and getting total flight delay times by city and airline,
    #as well as total amount of arrived flights by city and airline
    for flight in data_list:
        airline_key = flight[0]
        cities_key = flight[4]
        delay_time = flight[9]
        
        if cities_key in cities_dict:
            cities_dict[cities_key] += int(delay_time)
            cities_flights_dict[cities_key] += 1
        else:
            cities_dict[cities_key] = int(delay_time)
            cities_flights_dict[cities_key] = 1
        
        if airline_key in total_delay_time_dict:
            total_delay_time_dict[airline_key] += int(delay_time)
            total_flights_dict[airline_key] += 1
        else:
            total_delay_time_dict[airline_key] = int(delay_time)
            total_flights_dict[airline_key] = 1

    #getting the average delay time per flight by city
    for city in cities_dict:
        if cities_flights_dict[city] > 1000: #filtering some data-see webpage for more info
            cities_dict[city] = cities_dict[city] / cities_flights_dict[city]
        else:
            cities_dict[city] = -float("inf")
    
    #sorting the cities by average delay time and getting the top 10, then draw bar graph of that
    top_ten_cities = sorted(cities_dict.items(), key=lambda x: -x[1])[0:10]
    draw_bar_graph(top_ten_cities, "Cities", "Top 10 Most Delayed Airports of Origin at New York-LaGuardia in 2017")

    #drawing two pie graphs of total delay time and total number of flights by airline
    draw_pie_graph(total_delay_time_dict, "Total Delay Time by Airline at New York-LaGuardia in 2017")
    draw_pie_graph(total_flights_dict, "Total Number of Arrived Flights by Airline at New York-LaGuardia in 2017")
    
    #drawing another bar graph of average arrival delay per flight by airline
    for airline in total_delay_time_dict:
        total_delay_time_dict[airline] = total_delay_time_dict[airline] / total_flights_dict[airline]

    draw_bar_graph2(total_delay_time_dict, "Airline", "Average Arrival Flight Delay Per Airline New York-LaGuardia in 2017")

    