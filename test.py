mydicks = [{"key1": 0} for _ in range(3)]
print(f"before: {mydicks}")

for dick in mydicks:
    dick["key2"] = 0
print(f"after: {mydicks}")