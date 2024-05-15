
# TODO: modularize this code by creating a class.
def calculate_score(age, k=100, n=2):
    return (100 / (1 + (age / k) ** n))