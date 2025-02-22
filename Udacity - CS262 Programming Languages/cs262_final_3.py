# Market Exchange
#
# Focus: Units 5 and 6, Interpreting and Environments
#
#
# In this problem you will use your knowledge of interpretation and
# environments to simulate a simple market. Here the "program" is not a
# list of JavaScript commands that describe webpage computation, but
# instead a list of economic commands that describe business transactions.  
#
# Our parse tree (or abstract syntax tree) is a list of elements. Elements
# have three forms: has, buy and sell. "has" elements indicate that the
# given person begins with the given amount of money:
#
#       [ "klaus teuber", "has", 100 ] 
#
# "buy" elements indicate that the given person wants to purchase some
# item for the listed amount of money. For example:
#
#       [ "klaus teuber", "buy", "sheep", 50 ] 
#
# ... means that "klaus teuber" is interesting in buying the item
# "sheep" for 50 monetary units. For this assignment, that transaction will
# only happen if there is a seller also selling "sheep" for 50 (and if
# klaus actually has 50 or more monetary units). That is, both the item and
# the price must match exactly. The final type of element is "sell": 
#
#       [ "andreas seyfarth", "sell", "sheep" , 50 ] 
#
# This indicates that "andreas seyfarth" is willing to sell the item
# "sheep" for 50 monetary units. (Again, that transaction will only take
# place if there is a buyer wishing to purchase that item for exactly the
# same amount of money -- and if the buyer actually has at least that much
# money!) 
#
# All of the "has" commands will come first in the program.
#
# "buy" and "sell" elements only operate once per time they are listed. In
# this example: 
# 
#       [ "klaus teuber", "has", 100 ] 
#       [ "andreas seyfarth", "has", 50 ] 
#       [ "klaus teuber", "buy", "sheep", 50 ] 
#       [ "andreas seyfarth", "sell", "sheep" , 50 ] 
#
# klaus will buy "sheep" from andreas once, at which poin klaus will have
# 50 money and andreas will have 100. However, in this example:
#
#       [ "klaus teuber", "has", 100 ] 
#       [ "andreas seyfarth", "has", 50 ] 
#       [ "klaus teuber", "buy", "sheep", 50 ] 
#       [ "klaus teuber", "buy", "sheep", 50 ]          # listed twice
#       [ "andreas seyfarth", "sell", "sheep" , 50 ] 
#       [ "andreas seyfarth", "sell", "sheep" , 50 ]    # listed twice
# 
# klaus will buy "sheep" from andreas and then buy "sheep" from andreas
# again, at which point klaus will have 0 money and andreas will have 150. 
#
# Write a procedure evaluate() that takes a list of elements as an input.
# It should perform all possible transactions, in any order, until no more
# transactions are possible (e.g., because all "buy" and "sell" elements
# have been used and/or potential buyers do not have enough money left for
# their desired "buy"s). Your procedure should return an environment
# (a Python dictionary) mapping names to final money amounts (after all
# transactions have happened).  
#
# Hint: To avoid processing a "buy" or "sell" twice, you might either call
# yourself recursively with a smaller AST (i.e., with those two elements
# removed) or you can use Python's list.remove() to remove elements "in
# place". Example: 
#
# lst = [("a",1) , ("b",2) ]
# print lst
# [('a', 1), ('b', 2)]
# 
# lst.remove( ("a",1) )
# print lst
# [('b', 2)]

def evaluate(ast):
	# fill in your code here ...
	# contruct the env
	processed = []
	env = {}
	for item in ast:
		if item[1] == 'has':
			actor = item[0]
			if env.get(actor) ==  None:
				env[actor] = item[2]
			else:
				env[actor] += item[2]
			processed.append(item)
	# process the transaction
	#print 'processed: ', processed
	while True:
		count = len(processed)
		# run through
		for item in ast:
			if item in processed:
				continue
			# should only have buy or sell left
			actor, action, stuff, amount = item
			# process buy
			if action == 'buy':
				# make sure the buyer has enough money
				if env[actor] < amount:
					continue
				current_item = item
				for item1 in ast:
					#print '-----beginning of loop:', item1
					if item1 == current_item:
						continue
					if item1 in processed:
						continue
					# skip cmd from self
					if item1[0] == current_item[0]:
						continue
					if item1[1] == 'sell' and item1[2] == stuff and item1[3] == amount:
						#print 'curent:', current_item
						#print 'item1', item1
						# remove money from buyer
						env[actor] -= amount
						# add money to seller
						env[item1[0]] += amount
						# mark these two cmd processed
						processed.append(current_item)
						processed.append(item1)
						#print 'processed: ', processed
						break
				break
				#print '-------------------------------'
		new_count = len(processed)
		# this means that we did not make successful process, so nothing left to do
		if count == new_count:
			break
	return env
					


# In test1, exactly one sell happens. Even though klaus still has 25 money
# left over, a "buy"/"sell" only happens once per time it is listed.

test1 = [ ["klaus","has",50] ,
          ["wrede","has",80] ,
          ["klaus","buy","sheep", 25] ,
          ["wrede","sell","sheep", 25] , ] 

print evaluate(test1) == {'klaus': 25, 'wrede': 105}

# In test2, klaus does not have enough money, so no transactions take place.
test2 = [ ["klaus","has",5] ,
          ["wrede","has",80] ,
          ["klaus","buy","sheep", 25] ,
          ["wrede","sell","sheep", 25] , ] 

print evaluate(test2) == {'klaus': 5, 'wrede': 80}

# Wishful thinking, klaus! Although you want to buy sheep for 5 money and
# you even have 5 money, no one is selling sheep for 5 money. So no
# transactions happen.
test2b = [ ["klaus","has",5] ,
           ["wrede","has",80] ,
           ["klaus","buy","sheep", 5] ,
           ["wrede","sell","sheep", 25] , ] 

print evaluate(test2b) == {'klaus': 5, 'wrede': 80}

# In test3, wrede does not have the 75 required to buy the wheat from
# andreas until after wrede sells the sheep to klaus. 
test3 = [ ["klaus","has",50] ,
          ["wrede","has",50] ,
          ["andreas","has",50] ,
          ["wrede","buy","wheat", 75] ,
          ["andreas","sell","wheat", 75] , 
          ["klaus","buy","sheep", 25] ,
          ["wrede","sell","sheep", 25] , 
          ] 
print evaluate(test3 ) == {'andreas': 125, 'klaus': 25, 'wrede': 0}
test4 = [   ["klaus", "has", 50],
			["wrede", "has", 0],
			["andreas", "has", 50],
			["arthur", "has", 50],
			["arthur", "sell", "sheep", 50],
			["klaus", "sell", "cow", 50],
			["wrede", "sell", "sheep", 50],
			["wrede", "buy", "cow", 50],
			["andreas", "buy", "sheep", 50]
		]
print evaluate(test4)