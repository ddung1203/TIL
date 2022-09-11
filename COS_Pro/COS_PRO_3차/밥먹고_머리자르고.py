# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean
class Customer:
	def __init__(self, id, time, num_of_people):
		self.id = id
		self.time = time
		self.num_of_people = num_of_people

class Shop:
	def __init__(self):
		self.reserve_list = []

	def reserve(self, customer):
		self.reserve_list.append(customer)
		return True

class HairShop(Shop):
	def __init__(self):
		super().__init__()

	def reserve(self, customer):
		if customer.num_of_people != 1:
			return False
		for r in self.reserve_list:
			if r.time == customer.time:
				return False
		self.reserve_list.append(customer)
		return True

class Restaurant(Shop):
	def __init__(self):
		super().__init__()
		
	def reserve(self, customer):
		if 2 > customer.num_of_people or 8 < customer.num_of_people:
			return False
		count = 0
		for r in self.reserve_list:
			if r.time == customer.time:
				count += 1
		if count >= 2:
			return False
		self.reserve_list.append(customer)
		return True

def solution(customers, shops):
	hairshop = HairShop()
	restaurant = Restaurant()

	count = 0
	for customer, shop in zip(customers, shops):
		if shop == "hairshop":
			if hairshop.reserve(Customer(customer[0], customer[1], customer[2])):
				count += 1
		elif shop == "restaurant":
			if restaurant.reserve(Customer(customer[0], customer[1], customer[2])):
				count += 1

	return count


customers = [[1000, 2, 1],[2000, 2, 4],[1234, 5, 1],[4321, 2, 1],[1111, 3, 10]]
shops = ["hairshop", "restaurant", "hairshop", "hairshop", "restaurant"]
ret = solution(customers, shops)

print("solution 함수의 반환 값은", ret, "입니다.")