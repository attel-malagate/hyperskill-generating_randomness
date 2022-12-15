from string import digits
from random import randint
from numpy import array as np_array

triads = ['000', '001', '010', '011', '100', '101', '110', '111']
full_s = ""
triads_dict = dict.fromkeys(triads, [0,0])
#user_statistics_dict = dict()

def occurrences(string, sub):
    count = start = 0
    ind = []
    while True:
        start = string.find(sub, start) + 1
        if start > 0:
            count += 1
            ind.append(start + 2)
        else:
            return ind

def count_triad_pattern(_string, _t):
	try:
		indexes = occurrences(_string, _t)
		counter_n0, counter_n1 = 0, 0
		for i in indexes:
			#print('i:',i)
			if _string[i] == '0':
				counter_n0 += 1
			elif _string[i] == '1':
				counter_n1 += 1
		return np_array([counter_n0, counter_n1])
	except IndexError:
		return np_array([counter_n0, counter_n1])

def calculate_user_statistics(_string):
	global triads_dict
	for key in triads:
		triads_dict[key] += count_triad_pattern(_string, key)
	return triads_dict

def generate_triad_keys(_test_string): # use with input[3:] -> ommit 3 first characters
	test_keys = [_test_string[i:i+3] for i in range(len(_test_string))]
	return test_keys[:-3]

def make_prediction(_keys):
	prediction = generate_random_int(3)
	for key in _keys:
		if user_statistics_dict[key][0] == user_statistics_dict[key][1]:
			prediction += generate_random_int(1)
		elif user_statistics_dict[key][0] > user_statistics_dict[key][1]:
			prediction += '0'
		elif user_statistics_dict[key][0] < user_statistics_dict[key][1]:
			prediction += '1'
	return prediction
 
def estimate_accuracy(_s1, _s2):
	counter = 0
	for i in range(len(_s1)):
		if _s1[i] == _s2[i]:
			counter += 1
	return counter / len(_s1), counter


def generate_random_int(_i):
	s = ''
	for k in range(_i):
		s += str(randint(0,1))
	return str(s)

#user_statistics_dict = calculate_user_statistics()
#print(user_statistics_dict.keys(), user_statistics_dict.values())
def main():
	global full_s
	global user_statistics_dict
	balance = 1000
	try:
		
		#print(user_statistics_dict.keys(), user_statistics_dict.values())
		s = input("Please give AI some data to learn...\nThe current data length is 0, 100 symbols left\nPrint a random string containing 0 or 1:\n\n")
		while len(full_s) < 100:
			for char in s:
				if char in digits[:2]:
					full_s += char
			if len(full_s) <= 100:
				print(f"The current data length is {len(full_s)}, {100 - len(full_s)} symbols left")
				s = input("Print a random string containing 0 or 1:\n\n")
		print("Final data string:")
		print(full_s)
		print('\n')
		print('You have $1000. Every time the system successfully predicts your next press, you lose $1.\nOtherwise, you earn $1. Print "enough" to leave the game. Let\'s go!\n')
		user_statistics_dict = calculate_user_statistics(full_s)
		print('***', user_statistics_dict)
		while True:
			full_s_test = ''
			test_string = input("Print a random string containing 0 or 1:") # does not handle errors yet
			if test_string == 'enough':
				print('Game over!')
				break
			else:
				if all(item not in '01' for item in test_string):
					pass
					#test_string = input("Print a random string containing 0 or 1:")
				else:
					for char in test_string:
						if char in digits[:2]:
							full_s_test += char
				print('\n')
				if full_s_test != '':
					test_keys_for_dict = generate_triad_keys(full_s_test)
					prediction = make_prediction(test_keys_for_dict)
					print('prediction:')
					print(prediction)
					percent, counter = estimate_accuracy(full_s_test[3:], prediction[3:])
					print(f'Computer guessed right {counter} out of {len(full_s_test) - 3} symbols ({round(percent * 100, 2)} %)')
					balance += -1 * counter + ((len(full_s_test) - 3) - counter)
					print(f"Your balance is now ${balance}\nPrint a random string containing 0 or 1:")
					



					user_statistics_dict_1 = calculate_user_statistics(full_s_test)
					user_statistics_dict.update(user_statistics_dict_1)
					print(user_statistics_dict)

	except Exception:
		pass
		
main()
