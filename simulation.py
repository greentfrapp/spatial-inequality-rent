import numpy as np

class District():

	def __init__(self, name, transport_costs):
		self.name = name
		self.transport_costs = transport_costs
		self.profit = 4
		self.sectors = [[], [], [], []]
		self.maintenance = np.random.choice(np.arange(1,11),4)
		self.fixed = [False, False, False, False]
		self.update_rent()

	def update_rent(self):
		# self.rent = [(((1 + self.profit) * maintenance + self.transport_costs) / max(1, len(self.sectors[i]))) for i, maintenance in enumerate(self.maintenance)]
		self.rent = [(((1 + self.profit) * maintenance) / max(1, len(self.sectors[i]))) for i, maintenance in enumerate(self.maintenance)]

	def calculate_rent(self, sector_id):
		# return ((1 + self.profit) * self.maintenance[sector_id] + self.transport_costs) / (len(self.sectors[sector_id]) + 1)
		return ((1 + self.profit) * self.maintenance[sector_id]) / (len(self.sectors[sector_id]) + 1)

	def update_maintenance(self):
		for i, sector in enumerate(self.sectors):
			if self.fixed[i] == False:
				total_income = 0
				for tenant in sector:
					total_income += tenant.income
				self.maintenance[i] = max(1, min(10, int(total_income - self.transport_costs) / (1 + self.profit)))
		self.update_rent()

	def update_tenants(self):
		updated_tenants = []
		for i, sector in enumerate(self.sectors):
			for tenant_no, tenant in enumerate(sector):
				if tenant.name not in updated_tenants:
					self.sectors[i].pop(tenant_no)
					self.update_rent()
					displaced = True
					rent_list = []
					for j, sector in enumerate(self.sectors):
						rent_list.append([1 / (len(self.sectors[j]) + 1), self.calculate_rent(j), j])
					rent_list.sort(reverse=True)
					for [size, rent, sector_id] in rent_list:
						if tenant.income >= rent:
							self.sectors[sector_id].append(tenant)
							displaced = False
							break
					if displaced:
						rent_list = []
						for j, sector in enumerate(self.sectors):
							rent_list.append([self.calculate_rent(j), 1 / (len(self.sectors[j]) + 1), j])
						rent_list.sort(reverse=True)
						self.sectors[rent_list[-1][2]].append(tenant)
					updated_tenants.append(tenant.name)
		self.update_rent()

class Tenant():

	def __init__(self, name, income):
		self.name = name
		self.income = income

def main():
	district_1 = District(name='1', transport_costs=5)
	district_2 = District(name='2', transport_costs=10)
	for i in np.arange(1):
		district_2.sectors[0].append(Tenant('1_{}'.format(i), 1))
		district_2.sectors[0].append(Tenant('2_{}'.format(i), 1))
		district_2.sectors[0].append(Tenant('3_{}'.format(i), 1))
		district_2.sectors[0].append(Tenant('4_{}'.format(i), 20))
		district_2.sectors[0].append(Tenant('5_{}'.format(i), 20))
		district_2.sectors[0].append(Tenant('6_{}'.format(i), 20))
		district_2.sectors[0].append(Tenant('7_{}'.format(i), 100))
		district_2.sectors[0].append(Tenant('7_{}'.format(i), 100))
		# district_2.sectors[0].append(Tenant('1_{}'.format(i), 5))
		# district_2.sectors[0].append(Tenant('2_{}'.format(i), 100))

	round_no = 0
	district_2.update_rent()
	print(district_2.maintenance)
	while True:
		print('ROUND {}'.format(round_no))
		print(district_2.rent)
		for i, sector in enumerate(district_2.sectors):
			print([tenant.income for tenant in sector])
			# print(i, len(sector))
			# for tenant in sector:
			# 	print(tenant.income)
		round_no += 1
		response = input('Enter: ')
		if response == 'q':
			quit()
		else:
			if response in ['0', '1', '2', '3']:
				district_2.fixed[int(response)] = True
				district_2.maintenance[int(response)] = 10

		district_2.update_maintenance()
		print(district_2.maintenance)
		print(district_2.rent)
		response = input('Enter: ')
		if response == 'q':
			quit()
		district_2.update_tenants()


if __name__ == '__main__':
	main()