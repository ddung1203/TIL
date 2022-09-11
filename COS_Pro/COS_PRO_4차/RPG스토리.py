# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean
class Unit:
	def __init__(self):
		self.HP = 1000
	def under_attack(self, damage):
		pass
class Monster(Unit):
	def __init__(self, attack_point):
		super().__init__()
		self.attack_point = attack_point
	def under_attack(self, damage):
		self.HP -= damage
	def attack(self):
		return self.attack_point

class Warrior(Unit):
	def __init__(self, attack_point):
		super().__init__()
		self.attack_point = attack_point
	def under_attack(self, damage):
		self.HP -= damage
	def attack(self):
		return self.attack_point

class Healer(Unit):
	def __init__(self, healing_point):
		super().__init__()
		self.healing_point = healing_point
	def under_attack(self, damage):
		self.HP -= damage
	def healing(self, unit):
		unit.HP += self.healing_point


def solution(monster_attack_point, warrior_attack_point, healing_point):
	monster = Monster(monster_attack_point)
	warrior = Warrior(warrior_attack_point)
	healer = Healer(healing_point)

	monster.under_attack(warrior.attack())
	warrior.under_attack(monster.attack())
	healer.under_attack(monster.attack())
	healer.healing(warrior)
	healer.healing(monster)

	answer = [monster.HP, warrior.HP, healer.HP]
	return answer


monster_attack_point = 100
warrior_attack_point = 90
healing_point = 30
ret = solution(monster_attack_point, warrior_attack_point, healing_point)

print("solution 함수의 반환 값은", ret, "입니다.")