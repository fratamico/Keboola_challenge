import csv
import numpy as np
import matplotlib.pyplot as plt


beer_to_rating_dict = {}
brewery_to_rating_dict = {}
beer_style_to_rating_dict = {}

brewery_to_beer_to_rating_dict = {}
beer_to_brewery_to_rating_dict = {}
beer_style_to_beer_to_rating_dict = {}


abv_max = 0
abv_max_beer = []

def load_beer_info(filename):
    data_initial = open(filename, "rb")
    beer_reader = csv.reader((line.replace('\0','') for line in data_initial), delimiter=',', quotechar='"')

    next(beer_reader) #skip header row
    for row in beer_reader:
        try:
            beer_name = row[10]
            brewery_name = row[1]
            beer_style = row[7]
            abv = float(row[11])
            overall_rating = float(row[3])
        except:
        	continue

        if beer_name not in beer_to_rating_dict:
            beer_to_rating_dict[beer_name] = []
        beer_to_rating_dict[beer_name].append(overall_rating)

        if brewery_name not in brewery_to_rating_dict:
            brewery_to_rating_dict[brewery_name] = []
        brewery_to_rating_dict[brewery_name].append(overall_rating)

        if beer_style not in beer_style_to_rating_dict:
            beer_style_to_rating_dict[beer_style] = []
        beer_style_to_rating_dict[beer_style].append(overall_rating)

        global abv_max
        global abv_max_beer
        if abv == abv_max:
            abv_max_beer.append(beer_name)
        if abv > abv_max:
            abv_max = abv
            abv_max_beer = [beer_name]

        
        if brewery_name not in brewery_to_beer_to_rating_dict:
            brewery_to_beer_to_rating_dict[brewery_name] = {}
        if not beer_name in brewery_to_beer_to_rating_dict[brewery_name]:
            brewery_to_beer_to_rating_dict[brewery_name][beer_name] = []
        brewery_to_beer_to_rating_dict[brewery_name][beer_name].append(overall_rating)

        if beer_name not in beer_to_brewery_to_rating_dict:
            beer_to_brewery_to_rating_dict[beer_name] = {}
        if not brewery_name in beer_to_brewery_to_rating_dict[beer_name]:
            beer_to_brewery_to_rating_dict[beer_name][brewery_name] = []
        beer_to_brewery_to_rating_dict[beer_name][brewery_name].append(overall_rating)

        if beer_style not in beer_style_to_beer_to_rating_dict:
            beer_style_to_beer_to_rating_dict[beer_style] = {}
        if not beer_name in beer_style_to_beer_to_rating_dict[beer_style]:
            beer_style_to_beer_to_rating_dict[beer_style][beer_name] = []
        beer_style_to_beer_to_rating_dict[beer_style][beer_name].append(overall_rating)
     

def plot_histogram(array, title):
    plt.hist(array)
    plt.title(title)
    plt.xlabel("Number of times reviewed")
    plt.ylabel("Frequency")
    plt.show()


def get_frequency(array, number):
    return sum([array[x] <= number for x in array])/float(len(array))


def prune_dictionary(d):
    # decided to eliminate all that had 10 or fewer reviews -> Yelp principle. If something is barely reviewed, this means it's not popular enough to be good 
    return { k:v for k, v in d.items() if len(v) > 10 }


for filename in ['beer csv.csv', 'beer spreadsheet.csv']:
    load_beer_info(filename)



print "For determining unique numbers of beer, breweries, and beer types:"
print "beer:", len(beer_to_rating_dict)
print "breweries:", len(brewery_to_rating_dict)
print "beer types:", len(beer_style_to_rating_dict)


print "For determining where the cutoff for number of Beer reviews should be:"
number_of_beer_ratings = [len(beer_to_rating_dict[x]) for x in beer_to_rating_dict]
print 1, get_frequency(number_of_beer_ratings, 1) #0.173751692843
print 10, get_frequency(number_of_beer_ratings, 10) #0.76625569411
print 100, get_frequency(number_of_beer_ratings, 100) #0.991786411524

print "How do I get drunk:"
print abv_max_beer, abv_max

print "Worst beers"
beer_to_rating_dict_pruned = prune_dictionary(beer_to_rating_dict)
sorted_beer_list = sorted(beer_to_rating_dict_pruned.keys(), key=lambda x: np.mean(beer_to_rating_dict_pruned[x]))
for record in sorted_beer_list[:5]:
    print record+"  : "+str(np.mean(beer_to_rating_dict_pruned[record]))+"  : "+str(len(beer_to_rating_dict_pruned[record]))

print "Best beers"
for record in sorted_beer_list[-5:]:
    print record+"  : "+str(np.mean(beer_to_rating_dict_pruned[record]))+"  : "+str(len(beer_to_rating_dict_pruned[record]))
    pruned_brewery_list = prune_dictionary(beer_to_brewery_to_rating_dict[record]) #more than 10 reviews
    print "location:", sorted(pruned_brewery_list.keys(), key=lambda x: np.mean(pruned_brewery_list[x]))[-1]

print "Best breweries:"
brewery_to_rating_dict_pruned = prune_dictionary(brewery_to_rating_dict)
sorted_brewery_list = sorted(brewery_to_rating_dict_pruned.keys(), key=lambda x: np.mean(brewery_to_rating_dict_pruned[x]))
for record in sorted_brewery_list[-5:]:
    print record
    pruned_beer_list = prune_dictionary(brewery_to_beer_to_rating_dict[record]) #more than 10 reviews
    best_beer = sorted(pruned_beer_list.keys(), key=lambda x: np.mean(pruned_beer_list[x]))[-1]
    print "beer:", best_beer,  " : ", np.mean(beer_to_rating_dict[best_beer])

print "Best IPA:"
pruned_IPA_list = prune_dictionary(beer_style_to_beer_to_rating_dict["English India Pale Ale (IPA)"]) #more than 10 reviews
sorted_IPA_list = sorted(pruned_IPA_list.keys(), key=lambda x: np.mean(pruned_IPA_list[x]))
for record in sorted_IPA_list[-5:]:
    print record+"  : "+str(np.mean(pruned_IPA_list[record]))+"  : "+str(len(pruned_IPA_list[record]))









