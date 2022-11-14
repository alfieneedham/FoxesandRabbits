#Skeleton Program code for the AQA A Level Paper 1 2017 examination
#this code should be used in conjunction with the Preliminary Material
#written by the AQA Programmer Team
#developed in the Python 3.4.1 programming environment

import enum
import random
import math

class Location:
  def __init__(self):
    self.Fox = None
    self.Warren = None
    self.Den = None

class Simulation:
  def __init__(self, LandscapeSize, InitialWarrenCount, InitialFoxCount, Variability, FixedInitialLocations):
    self.__ViewRabbits = ""
    self.__TimePeriod = 0
    self.__WarrenCount = 0
    self.__FoxCount = 0
    self.__ShowDetail = False
    self.__LandscapeSize = LandscapeSize
    self.__Variability = Variability
    self.__FixedInitialLocations = FixedInitialLocations
    self.__Landscape = []
    for Count1 in range (self.__LandscapeSize):
      LandscapeRow = []
      for Count2 in range (self.__LandscapeSize):
        LandscapeLocation = None
        LandscapeRow.append(LandscapeLocation)
      self.__Landscape.append(LandscapeRow)
    self.__CreateLandscapeAndAnimals(InitialWarrenCount, InitialFoxCount, self.__FixedInitialLocations)
    self.__DrawLandscape()
    MenuOption = 0
    while (self.__WarrenCount > 0 or self.__FoxCount > 0) and MenuOption != 5:
      print()
      print("0. Advance 10 time periods hiding detail")
      print("1. Advance to next time period showing detail")
      print("2. Advance to next time period hiding detail")
      print("3. Inspect fox")
      print("4. Inspect warren")
      print("5. Exit")
      print()
      MenuOption = int(input("Select option: "))
      if MenuOption == 0:
        self.__TimePeriod += 10
        self.__ShowDetail = False
        for index in range(10):
          self.__AdvanceTimePeriod()
      if MenuOption == 1:
        self.__TimePeriod += 1
        self.__ShowDetail = True
        self.__AdvanceTimePeriod()
      if MenuOption == 2:
        self.__TimePeriod += 1
        self.__ShowDetail = False
        self.__AdvanceTimePeriod()
      if MenuOption == 3:
        x = self.__InputCoordinate("x")
        y = self.__InputCoordinate("y")
        if not self.__Landscape[x][y].Fox is None:
          self.__Landscape[x][y].Fox.Inspect()
      if MenuOption == 4:
        x = self.__InputCoordinate("x")
        y = self.__InputCoordinate("y")
        if not self.__Landscape[x][y].Warren is None:
          self.__Landscape[x][y].Warren.Inspect()
          self.__ViewRabbits = input("View individual rabbits (y/n)? ")
          if self.__ViewRabbits == "y":
            self.__Landscape[x][y].Warren.ListRabbits()
    input()
    
  def __InputCoordinate(self, CoordinateName):
    Coordinate = int(input("  Input " + CoordinateName + " coordinate:"))
    return Coordinate
  
  def __AdvanceTimePeriod(self):
    NewFoxCount = 0
    if self.__ShowDetail:
      print()
    for x in range (0, self.__LandscapeSize):
      for y in range (0, self.__LandscapeSize):
        if not self.__Landscape[x][y].Warren is None:
          if self.__ShowDetail:
            print("Warren at (", x, ",", y, "):", sep = "")
            print("  Period Start: ", end = "")
            self.__Landscape[x][y].Warren.Inspect()
          if self.__FoxCount > 0:
            self.__FoxesEatRabbitsInWarren(x, y)
          if self.__Landscape[x][y].Warren.NeedToCreateNewWarren():
            self.__CreateNewWarren()
          self.__Landscape[x][y].Warren.AdvanceGeneration(self.__ShowDetail)
          if self.__ShowDetail:
            print("  Period End: ", end = "")
            self.__Landscape[x][y].Warren.Inspect()
            input()
          if self.__Landscape[x][y].Warren.WarrenHasDiedOut():
            self.__Landscape[x][y].Warren = None
            self.__WarrenCount -= 1
    for x in range (0, self.__LandscapeSize):
      for y in range (0, self.__LandscapeSize):
        if not self.__Landscape[x][y].Fox is None:
          if self.__ShowDetail:
            print("Fox at (", x, ",", y, "): ", sep = "")
          self.__Landscape[x][y].Fox.AdvanceGeneration(self.__ShowDetail)
          if self.__Landscape[x][y].Fox.CheckIfDead():
            self.__Landscape[x][y].Fox = None
            self.__FoxCount -= 1
          else:
            if self.__Landscape[x][y].Fox.ReproduceThisPeriod():
              if self.__ShowDetail:
                print("  Fox has reproduced. ")
              NewFoxCount += 1
            if self.__ShowDetail:
              self.__Landscape[x][y].Fox.Inspect()
            self.__Landscape[x][y].Fox.ResetFoodConsumed()
        if not self.__Landscape[x][y].Den is None:
          self.__Landscape[x][y].Den.advance_generation()
          if self.__Landscape[x][y].Den.get_need_to_spawn_new_fox() == True:
            self.__CreateNewFox()
    if NewFoxCount > 0:
      if self.__ShowDetail:
        print("New foxes born: ")
      for f in range (0, NewFoxCount):
        self.__CreateNewFox()
    if self.__ShowDetail:
      input()
    self.__DrawLandscape()
    print()

  def __CreateLandscapeAndAnimals(self, InitialWarrenCount, InitialFoxCount, FixedInitialLocations):
    for x in range (0, self.__LandscapeSize):
      for y in range (0, self.__LandscapeSize):
        self.__Landscape[x][y] = Location()
    if FixedInitialLocations:
      self.__Landscape[1][1].Warren = Warren(self.__Variability, 38)
      self.__Landscape[2][8].Warren = Warren(self.__Variability, 80) 
      self.__Landscape[9][7].Warren = Warren(self.__Variability, 20)
      self.__Landscape[10][3].Warren = Warren(self.__Variability, 52)
      self.__Landscape[13][4].Warren = Warren(self.__Variability, 67)
      self.__Landscape[11][4].Warren = GiantWarren(self.__Variability, 115)
      self.__WarrenCount = 6
      self.__Landscape[2][10].Fox = Fox(self.__Variability)
      self.__Landscape[6][1].Fox = Fox(self.__Variability)
      self.__Landscape[8][6].Fox = Fox(self.__Variability)
      self.__Landscape[11][13].Fox = Fox(self.__Variability)
      self.__Landscape[12][4].Fox = Fox(self.__Variability)
      self.__FoxCount = 5
      self.__Landscape[2][3].Den = Den(self.__Variability)
      self.__DenCount = 1
    else:
      for w in range (0, InitialWarrenCount):
        self.__CreateNewWarren()
      for f in range (0, InitialFoxCount):
        self.__CreateNewFox()

  def __CreateNewWarren(self):
    x = random.randint(0, self.__LandscapeSize - 1)
    y = random.randint(0, self.__LandscapeSize - 1)
    while not self.__Landscape[x][y].Warren is None:
      x = random.randint(0, self.__LandscapeSize - 1)
      y = random.randint(0, self.__LandscapeSize - 1)
    if self.__ShowDetail:
      print("New Warren at (", x, ",", y, ")", sep = "")
    self.__Landscape[x][y].Warren = Warren(self.__Variability)
    self.__WarrenCount += 1
  
  def __CreateNewFox(self):
    x = random.randint(0, self.__LandscapeSize - 1)
    y = random.randint(0, self.__LandscapeSize - 1)
    while not self.__Landscape[x][y].Fox is None:
      x = random.randint(0, self.__LandscapeSize - 1)
      y = random.randint(0, self.__LandscapeSize - 1)
 #   if self.__ShowDetail:
    print("  New Fox at (", x, ",", y, ")", sep = "")
    self.__Landscape[x][y].Fox = Fox(self.__Variability)
    self.__FoxCount += 1

  def __FoxesEatRabbitsInWarren(self, WarrenX, WarrenY):
    RabbitCountAtStartOfPeriod  = self.__Landscape[WarrenX][WarrenY].Warren.GetRabbitCount()
    for FoxX in range(0, self.__LandscapeSize):
      for FoxY in range (0, self.__LandscapeSize):
        if not self.__Landscape[FoxX][FoxY].Fox is None:
          Dist = self.__DistanceBetween(FoxX, FoxY, WarrenX, WarrenY)
          if Dist <= 3.5:
            PercentToEat = 20
          elif Dist <= 7:
            PercentToEat = 10
          else:
            PercentToEat = 0
          RabbitsToEat = int(round(float(PercentToEat * RabbitCountAtStartOfPeriod / 100)))
          FoodConsumed = self.__Landscape[WarrenX][WarrenY].Warren.EatRabbits(RabbitsToEat)
          self.__Landscape[FoxX][FoxY].Fox.GiveFood(FoodConsumed)
          if self.__ShowDetail:
            print("  ", FoodConsumed, " rabbits eaten by fox at (", FoxX, ",", FoxY, ").", sep = "")

  def __DistanceBetween(self, x1, y1, x2, y2):
    return math.sqrt((pow(x1 - x2, 2) + pow(y1 - y2, 2)))

  def __DrawLandscape(self):
    print()
    print("TIME PERIOD:", self.__TimePeriod)
    print()
    print("   ", end = "")
    for x in range (0, self.__LandscapeSize):
      if x < 10:
        print(" ", end = "")
      print(x, "|", end = "")
    print()
    for x in range (0, self.__LandscapeSize * 4 + 3):
      print("-", end = "")
    print()
    for y in range (0, self.__LandscapeSize):
      if y < 10:
        print(" ", end = "")
      print("", y, "|", sep = "", end = "")
      for x in range (0, self.__LandscapeSize):
        if not self.__Landscape[x][y].Warren is None:
          if self.__Landscape[x][y].Warren.GetRabbitCount() < 10:
            print(" ", end = "")
          print(self.__Landscape[x][y].Warren.GetRabbitCount(), end = "")
        else:
          print("  ", end = "")
        if not self.__Landscape[x][y].Fox is None:
          print("F", end = "")
        else:
          print(" ", end = "")
        if not self.__Landscape[x][y].Den is None:
          print("D" + str(self.__Landscape[x][y].Den.get_num_foxes_spawned()), end = "")
        else:
          print(" ", end = "")
        print("|", end = "")

      print()

class Den:
  def __init__(self, Variability):
    self.__variability = Variability
    self.__numFoxesSpawned = 0
    self.__periodsRun = 0
    self.__timeUntilNextFoxSpawn = 3
    self.__needToCreateNewFox = False

  def advance_generation(self):
    self.__needToCreateNewFox = False
    self.__periodsRun += 1
    self.__timeUntilNextFoxSpawn -= 1
    if self.__timeUntilNextFoxSpawn == 0:
      self.__needToCreateNewFox = True
      self.__numFoxesSpawned += 1
      self.__timeUntilNextFoxSpawn = 3

  def get_num_foxes_spawned(self):
    return (self.__numFoxesSpawned)

  def get_need_to_spawn_new_fox(self):
    return (self.__needToCreateNewFox)


class Warren:
  def __init__(self, Variability, RabbitCount = 0, MaxRabbits = 99):
    self._MAX_RABBITS_IN_WARREN = MaxRabbits
    self._RabbitCount = RabbitCount
    self._PeriodsRun = 0
    self._AlreadySpread = False
    self._Variability = Variability
    self._Rabbits = []
    for Count in range(0, self._MAX_RABBITS_IN_WARREN):
      self._Rabbits.append(None)
    if self._RabbitCount == 0:
      self._RabbitCount = int(self._CalculateRandomValue(int(self._MAX_RABBITS_IN_WARREN / 4), self._Variability))
    for r in range (0, self._RabbitCount):
      self._Rabbits[r] = Rabbit(self._Variability)

  def _CalculateRandomValue(self, BaseValue, Variability):
    return BaseValue - (BaseValue * Variability / 100) + (BaseValue * random.randint(0, Variability * 2) / 100)

  def GetRabbitCount(self): 
    return self._RabbitCount
  
  def NeedToCreateNewWarren(self): 
    if self._RabbitCount == self._MAX_RABBITS_IN_WARREN and not self._AlreadySpread:
      self._AlreadySpread = True
      return True
    else:
      return False
    
  def WarrenHasDiedOut(self):
    if self._RabbitCount == 0:
      return True
    else:
      return False

  def AdvanceGeneration(self, ShowDetail):
    self._PeriodsRun += 1
    if self._RabbitCount > 0:
      self._KillByOtherFactors(ShowDetail)
    if self._RabbitCount > 0:
      self._AgeRabbits(ShowDetail)
    if self._RabbitCount > 0 and self._RabbitCount <= self._MAX_RABBITS_IN_WARREN:
      if self._ContainsMales():
        self._MateRabbits(ShowDetail)
    if self._RabbitCount == 0 and ShowDetail:
      print("  All rabbits in warren are dead")
    
  def EatRabbits(self, RabbitsToEat):
    DeathCount = 0
    if RabbitsToEat > self._RabbitCount:
      RabbitsToEat = self._RabbitCount
    while DeathCount < RabbitsToEat:
      RabbitNumber = random.randint(0, self._RabbitCount - 1)
      if not self._Rabbits[RabbitNumber] is None:
        self._Rabbits[RabbitNumber] = None
        DeathCount += 1
    self._CompressRabbitList(DeathCount)
    return RabbitsToEat

  def _KillByOtherFactors(self, ShowDetail):
    DeathCount = 0
    for r in range (0, self._RabbitCount):
      if self._Rabbits[r].CheckIfKilledByOtherFactor():
        self._Rabbits[r] = None
        DeathCount += 1
    self._CompressRabbitList(DeathCount)
    if ShowDetail:
      print(" ", DeathCount, "rabbits killed by other factors.")

  def _AgeRabbits(self, ShowDetail):
    DeathCount = 0
    for r in range (0, self._RabbitCount):
      self._Rabbits[r].CalculateNewAge()
      if self._Rabbits[r].CheckIfDead():
        self._Rabbits[r] = None
        DeathCount += 1
    self._CompressRabbitList(DeathCount)
    if ShowDetail:
      print(" ", DeathCount, "rabbits die of old age.")

  def _MateRabbits(self, ShowDetail):
    Mate = 0
    Babies = 0 
    for r in range (0, self._RabbitCount):
      if self._Rabbits[r].IsFemale() and self._RabbitCount + Babies < self._MAX_RABBITS_IN_WARREN:
        Mate = random.randint(0, self._RabbitCount - 1)
        while Mate == r or self._Rabbits[Mate].IsFemale():
          Mate = random.randint(0, self._RabbitCount - 1)
        CombinedReproductionRate = (self._Rabbits[r].GetReproductionRate() + self._Rabbits[Mate].GetReproductionRate()) / 2
        if CombinedReproductionRate >= 1:
          self._Rabbits[self._RabbitCount + Babies] = Rabbit(self._Variability, CombinedReproductionRate)
          Babies += 1
    self._RabbitCount = self._RabbitCount + Babies
    if ShowDetail:
      print(" ", Babies, "baby rabbits born.")

  def _CompressRabbitList(self, DeathCount):
    if DeathCount > 0:
      ShiftTo = 0
      ShiftFrom  = 0
      while ShiftTo < self._RabbitCount - DeathCount:
        while self._Rabbits[ShiftFrom] is None:
          ShiftFrom += 1
        if ShiftTo != ShiftFrom:
          self._Rabbits[ShiftTo] = self._Rabbits[ShiftFrom]
        ShiftTo += 1
        ShiftFrom += 1
      self._RabbitCount = self._RabbitCount - DeathCount

  def _ContainsMales(self):
    Males = False
    for r in range (0, self._RabbitCount):
      if not self._Rabbits[r].IsFemale():
        Males = True
    return Males

  def Inspect(self):
    print("Periods Run", self._PeriodsRun, "Size", self._RabbitCount)

  def ListRabbits(self):
    if self._RabbitCount > 0:
      for r in range (0, self._RabbitCount):
        self._Rabbits[r].Inspect()

class GiantWarren(Warren):
  def __init__(self, Variability, RabbitCount = 0, MaxRabbits = 200):
    super().__init__(Variability, RabbitCount, MaxRabbits)

  def NeedToCreateNewWarren(self): 
    if self._RabbitCount >= self._MAX_RABBITS_IN_WARREN:
      return True
    else:
      return False

class Animal:
  _ID = 1

  def __init__(self, AvgLifespan, AvgProbabilityOfDeathOtherCauses, Variability):
    self._NaturalLifespan = int(AvgLifespan * self._CalculateRandomValue(100, Variability) / 100)
    self._ProbabilityOfDeathOtherCauses = AvgProbabilityOfDeathOtherCauses * self._CalculateRandomValue(100, Variability) / 100
    self._IsAlive = True
    self._ID = Animal._ID
    self._Age = 0
    Animal._ID += 1

  def CalculateNewAge(self):
    self._Age += 1
    if self._Age >= self._NaturalLifespan:
      self._IsAlive = False

  def CheckIfDead(self): 
    return not self._IsAlive

  def Inspect(self):
    print("  ID", self._ID, "", end = "")
    print("Age", self._Age, "", end = "")
    print("LS", self._NaturalLifespan, "", end = "")
    print("Pr dth", round(self._ProbabilityOfDeathOtherCauses, 2), "", end = "")

  def CheckIfKilledByOtherFactor(self):
    if random.randint(0, 100) < self._ProbabilityOfDeathOtherCauses * 100:
      self._IsAlive = False
      return True
    else:
      return False

  def _CalculateRandomValue(self, BaseValue, Variability):
    return BaseValue - (BaseValue * Variability / 100) + (BaseValue * random.randint(0, Variability * 2) / 100)

class Fox(Animal):
  def __init__(self, Variability):
    self.__DEFAULT_LIFE_SPAN = 7
    self.__DEFAULT_PROBABILITY_DEATH_OTHER_CAUSES = 0.1
    super(Fox, self).__init__(self.__DEFAULT_LIFE_SPAN, self.__DEFAULT_PROBABILITY_DEATH_OTHER_CAUSES, Variability)
    self.__FoodUnitsNeeded = int(10 * self._CalculateRandomValue(100, Variability) / 100)
    self.__FoodUnitsConsumedThisPeriod  = 0
    if random.randrange(0, 3) == 0:
      self.__gender = "Male"
    else:
      self.__gender = "Female"

  def AdvanceGeneration(self, ShowDetail):
    if self.__FoodUnitsConsumedThisPeriod == 0:
      self._IsAlive = False
      if ShowDetail:
        print("  Fox dies as has eaten no food this period.")
    else:
      if self.CheckIfKilledByOtherFactor():
        self._IsAlive = False
        if ShowDetail:
          print("  Fox killed by other factor.")
      else:
        if self.__FoodUnitsConsumedThisPeriod < self.__FoodUnitsNeeded:
          self.CalculateNewAge()
          if ShowDetail:
            print("  Fox ages further due to lack of food.")
        self.CalculateNewAge()
        if not self._IsAlive:
          if ShowDetail:
            print("  Fox has died of old age.")

  def ResetFoodConsumed(self):
    self.__FoodUnitsConsumedThisPeriod = 0

  def ReproduceThisPeriod(self): 
    REPRODUCTION_PROBABILITY  = 0.25
    if random.randint(0, 100) < REPRODUCTION_PROBABILITY * 100 and self.__gender == "Female":
      return True
    else:
      return False

  def GiveFood(self, FoodUnits):
    self.__FoodUnitsConsumedThisPeriod = self.__FoodUnitsConsumedThisPeriod + FoodUnits
  
  def Inspect(self):
    super(Fox, self).Inspect()
    print("Food needed", self.__FoodUnitsNeeded, "", end = "")
    print("Food eaten", self.__FoodUnitsConsumedThisPeriod, "", end = "")
    print("Gender", self.__gender, "", end = "")
    print()

class Genders(enum.Enum):
  Male = 1
  Female = 2
    
class Rabbit(Animal):
  def __init__(self, Variability, ParentsReproductionRate = 1.2, percentageMales = 50):
    self.__DEFAULT_LIFE_SPAN = 4
    self.__DEFAULT_PROBABILITY_DEATH_OTHER_CAUSES  = 0.05
    super(Rabbit, self).__init__(self.__DEFAULT_LIFE_SPAN, self.__DEFAULT_PROBABILITY_DEATH_OTHER_CAUSES, Variability)
    self.__ReproductionRate = ParentsReproductionRate * self._CalculateRandomValue(100, Variability) / 100
    self.__genderRatio = percentageMales
    if random.randint(0, 100) < self.__genderRatio:
      self.__Gender = Genders.Male
    else:
      self.__Gender = Genders.Female

  def Inspect(self):
    super(Rabbit, self).Inspect()
    print("Rep rate", round(self.__ReproductionRate, 1), "", end = "")
    if self.__Gender == Genders.Female:
      print("Gender Female")
    else:
      print("Gender Male")
    
  def IsFemale(self):
    if self.__Gender == Genders.Female:
      return True
    else:
      return False
    
  def GetReproductionRate(self): 
    return self.__ReproductionRate

def Main():
  MenuOption = 0
  while MenuOption != 4:
    print("Predator Prey Simulation Main Menu")
    print()
    print("1. Run simulation with default settings")
    print("2. Run simulation with custom settings")
    print("3. Rabbit Paradise")
    print("4. Exit")
    print("")
    MenuOption = int(input("Select option: "))
    if MenuOption == 1 or MenuOption == 2 or MenuOption == 3:
      if MenuOption == 1:
        LandscapeSize = 15
        InitialWarrenCount = 5
        InitialFoxCount = 5
        Variability = 0
        FixedInitialLocations = True
      elif MenuOption == 3:
        LandscapeSize = 20
        InitialWarrenCount = 20
        InitialFoxCount = 0
        Variability = 1
        FixedInitialLocations = False
      else:
        LandscapeSize = int(input("Landscape Size: "))
        InitialWarrenCount = int(input("Initial number of warrens: "))
        InitialFoxCount = int(input("Initial number of foxes: "))
        Variability = int(input("Randomness variability (percent): "))
        FixedInitialLocations = False
      Sim = Simulation(LandscapeSize, InitialWarrenCount, InitialFoxCount, Variability, FixedInitialLocations)
  input()

if __name__ == "__main__":
  Main()