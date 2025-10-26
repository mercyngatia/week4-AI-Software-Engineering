# Creating and sorting lists
empty_list = list()
print(empty_list)  # Output: []
fruits = ['banana', 'orange', 'mango', 'lemon']
vegetables = ['Tomato', 'Potato', 'Cabbage', 'Onion', 'Carrot']
fruits.sort()
print("Ascending:", fruits)
fruits.sort(reverse=True)
print("Descending:", fruits)

vegetables.sort()
print("Ascending:", vegetables)
vegetables.sort(reverse=True)
print("Descending:", vegetables)

# Dictionary sorting function
def dict_sort_list(dict_list, sort_key):
    return sorted(dict_list, key=lambda x: x[sort_key])
data = [
    {'type': 'banana', 'price': 'ksh 25'},
    {'type': 'mango', 'price': 'ksh 22'},
    {'type': 'lemon', 'price': 'ksh 30'}
    ]
sorted_by_type = dict_sort_list(data, 'type')
print("Sorted by type:", sorted_by_type)