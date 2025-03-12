from mmk import MmkAPIService

mmk = MmkAPIService()
res = mmk.country.list()
print(res)
