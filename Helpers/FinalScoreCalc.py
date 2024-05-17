
# TODO: modularize this code by creating a class.
class ScoreCalculator:
   def __init__(self, k=100, n=2):
       self.k = k
       self.n = n

   def CalculateScore(self, age):
       return (100 / (1 + (age / self.k) ** self.n))