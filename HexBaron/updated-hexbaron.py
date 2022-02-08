# I have numbered the cells and added coulours to this version to make it more playable.
# The unedited version provided by AQA is called raw-hexbaron.py

from colorama import init, Fore, Style
init() # For colorama

def map_icon(icon): # Added this func to colour icons
  ICON_MAP = {
    '#': Fore.GREEN + '#',
    '~': Fore.RED + '~'
  }
  if icon == ' ':
    return icon
  if icon in ICON_MAP:
    return ICON_MAP[icon] + Style.RESET_ALL
  out = f'{icon}{Style.RESET_ALL}'
  return Fore.BLUE + out if icon.isupper() else Fore.YELLOW + out

##########################################################################
#Skeleton Program code for the AQA A Level Paper 1 Summer 2021 examination
#this code should be used in conjunction with the Preliminary Material
#written by the AQA Programmer Team
#developed in the Python 3.5 programming environment

import random
import os

class Piece:
  def __init__(self, Player1):
    self._FuelCostOfMove = 1
    self._BelongsToPlayer1 = Player1
    self._Destroyed = False
    self._PieceType = "S"
    self._VPValue = 1
    self._ConnectionsToDestroy = 2

  def GetVPs(self):
    return self._VPValue

  def GetBelongsToPlayer1(self):
    return self._BelongsToPlayer1

  def CheckMoveIsValid(self, DistanceBetweenTiles, StartTerrain, EndTerrain):
    if DistanceBetweenTiles == 1:
      if StartTerrain == "~" or EndTerrain == "~":
        return self._FuelCostOfMove * 2
      else:
        return self._FuelCostOfMove
    return -1

  def HasMethod(self, MethodName):
    return callable(getattr(self, MethodName, None))

  def GetConnectionsNeededToDestroy(self):
    return self._ConnectionsToDestroy

  def GetPieceType(self):
    if self._BelongsToPlayer1:
      return self._PieceType
    else:
      return self._PieceType.lower()

  def DestroyPiece(self):
    self._Destroyed = True

class BaronPiece(Piece):
  def __init__(self, Player1):
    super(BaronPiece, self).__init__(Player1)
    self._PieceType = "B"
    self._VPValue = 10

  def CheckMoveIsValid(self, DistanceBetweenTiles, StartTerrain, EndTerrain):
    if DistanceBetweenTiles == 1:
      return self._FuelCostOfMove
    return -1

class LESSPiece(Piece):
  def __init__(self, Player1):
    super(LESSPiece, self).__init__(Player1)
    self._PieceType = "L"
    self._VPValue = 3

  def CheckMoveIsValid(self, DistanceBetweenTiles, StartTerrain, EndTerrain):
    if DistanceBetweenTiles == 1 and StartTerrain != "#":
      if StartTerrain == "~" or EndTerrain == "~":
        return self._FuelCostOfMove * 2
      else:
        return self._FuelCostOfMove
    return -1

  def Saw(self, Terrain):
    if Terrain != "#":
      return 0
    return 1

class PBDSPiece(Piece):
  def __init__(self, Player1):
    super(PBDSPiece, self).__init__(Player1)
    self._PieceType = "P"
    self._VPValue = 2
    self._FuelCostOfMove = 2

  def CheckMoveIsValid(self, DistanceBetweenTiles, StartTerrain, EndTerrain):
    if DistanceBetweenTiles != 1 or StartTerrain == "~":
      return -1
    return self._FuelCostOfMove

  def Dig(self, Terrain):
    if Terrain != "~":
      return 0
    if random.random() < 0.9:
      return 1
    else:
      return 5

class Tile:
  def __init__(self, xcoord, ycoord, zcoord):
    self._x = xcoord
    self._y = ycoord
    self._z = zcoord
    self._Terrain = " "
    self._PieceInTile = None
    self._Neighbours = []

  def GetDistanceToTileT(self, T):
    return max(max(abs(self.Getx() - T.Getx()), abs(self.Gety() - T.Gety())), abs(self.Getz() - T.Getz()))

  def AddToNeighbours(self, N):
    self._Neighbours.append(N)

  def GetNeighbours(self):
    return self._Neighbours

  def SetPiece(self, ThePiece):
    self._PieceInTile = ThePiece

  def SetTerrain(self, T):
    self._Terrain = T

  def Getx(self):
    return self._x

  def Gety(self):
    return self._y

  def Getz(self):
    return self._z

  def GetTerrain(self, display=False): # Added display
    return self._Terrain if not display else map_icon(self._Terrain) # Added map_icon()

  def GetPieceInTile(self):
    return self._PieceInTile

class HexGrid:
  def __init__(self, n):
    self._Size = n
    self._Player1Turn = True
    self._Tiles = []
    self._Pieces = []
    self.__ListPositionOfTile = 0
    self.__SetUpTiles()
    self.__SetUpNeighbours()
    self.grid_index = -1 # Added this attribute (see get_grid_index())

  def SetUpGridTerrain(self, ListOfTerrain):
    for Count in range (0, len(ListOfTerrain)):
      self._Tiles[Count].SetTerrain(ListOfTerrain[Count])

  def AddPiece(self, BelongsToPlayer1, TypeOfPiece, Location):
    if TypeOfPiece == "Baron":
      NewPiece = BaronPiece(BelongsToPlayer1)
    elif TypeOfPiece == "LESS":
      NewPiece = LESSPiece(BelongsToPlayer1)
    elif TypeOfPiece == "PBDS":
      NewPiece = PBDSPiece(BelongsToPlayer1)
    else:
      NewPiece = Piece(BelongsToPlayer1)
    self._Pieces.append(NewPiece)
    self._Tiles[Location].SetPiece(NewPiece)

  def ExecuteCommand(self, Items, FuelAvailable, LumberAvailable, PiecesInSupply):
    FuelChange = 0
    LumberChange = 0
    SupplyChange = 0
    if Items[0] == "move":
      FuelCost = self.__ExecuteMoveCommand(Items, FuelAvailable)
      if FuelCost < 0:
        return "That move can't be done", FuelChange, LumberChange, SupplyChange
      FuelChange = -FuelCost
    elif Items[0] in ["saw", "dig"]:
      Success, FuelChange, LumberChange = self.__ExecuteCommandInTile(Items)
      if not Success:
        return "Couldn't do that", FuelChange, LumberChange, SupplyChange
    elif Items[0] == "spawn":
      LumberCost = self.__ExecuteSpawnCommand(Items, LumberAvailable, PiecesInSupply)
      if LumberCost < 0:
        return "Spawning did not occur", FuelChange, LumberChange, SupplyChange
      LumberChange = -LumberCost
      SupplyChange = 1
    elif Items[0] == "upgrade":
      LumberCost = self.__ExecuteUpgradeCommand(Items, LumberAvailable)
      if LumberCost < 0:
        return "Upgrade not possible", FuelChange, LumberChange, SupplyChange
      LumberChange = -LumberCost
    return "Command executed", FuelChange, LumberChange, SupplyChange

  def __CheckTileIndexIsValid(self, TileToCheck):
    return TileToCheck >= 0 and TileToCheck < len(self._Tiles)

  def __CheckPieceAndTileAreValid(self, TileToUse):
    if self.__CheckTileIndexIsValid(TileToUse):
      ThePiece = self._Tiles[TileToUse].GetPieceInTile()
      if ThePiece is not None:
        if ThePiece.GetBelongsToPlayer1() == self._Player1Turn:
          return True
    return False

  def __ExecuteCommandInTile(self, Items):
    TileToUse = int(Items[1])
    Fuel = 0
    Lumber = 0
    if self.__CheckPieceAndTileAreValid(TileToUse) == False:
      return False, Fuel, Lumber
    ThePiece = self._Tiles[TileToUse].GetPieceInTile()
    Items[0] = Items[0][0].upper() + Items[0][1:]
    if ThePiece.HasMethod(Items[0]):
      Method = getattr(ThePiece, Items[0], None)
      if Items[0] == "Saw":
        Lumber += Method(self._Tiles[TileToUse].GetTerrain())
      elif Items[0] == "Dig":
        Fuel += Method(self._Tiles[TileToUse].GetTerrain())
        if abs(Fuel) > 2:
          self._Tiles[TileToUse].SetTerrain(" ")
      return True, Fuel, Lumber
    return False, Fuel, Lumber

  def __ExecuteMoveCommand(self, Items, FuelAvailable):
    StartID = int(Items[1])
    EndID = int(Items[2])
    if not self.__CheckPieceAndTileAreValid(StartID) or not self.__CheckTileIndexIsValid(EndID):
      return -1
    ThePiece = self._Tiles[StartID].GetPieceInTile()
    if self._Tiles[EndID].GetPieceInTile() is not None:
      return -1
    Distance = self._Tiles[StartID].GetDistanceToTileT(self._Tiles[EndID])
    FuelCost = ThePiece.CheckMoveIsValid(Distance, self._Tiles[StartID].GetTerrain(), self._Tiles[EndID].GetTerrain())
    if FuelCost == -1 or FuelAvailable < FuelCost:
      return -1
    self.__MovePiece(EndID, StartID)
    return FuelCost

  def __ExecuteSpawnCommand(self, Items, LumberAvailable, PiecesInSupply):
    TileToUse = int(Items[1])
    if PiecesInSupply < 1 or LumberAvailable < 3 or not self.__CheckTileIndexIsValid(TileToUse):
      return -1
    ThePiece = self._Tiles[TileToUse].GetPieceInTile()
    if ThePiece is not None:
      return -1
    OwnBaronIsNeighbour = False
    ListOfNeighbours = self._Tiles[TileToUse].GetNeighbours()
    for N in ListOfNeighbours:
      ThePiece = N.GetPieceInTile()
      if ThePiece is not None:
        if self._Player1Turn and ThePiece.GetPieceType() == "B" or not self._Player1Turn and ThePiece.GetPieceType() == "b":
          OwnBaronIsNeighbour = True
          break
    if not OwnBaronIsNeighbour:
      return -1
    NewPiece = Piece(self._Player1Turn)
    self._Pieces.append(NewPiece)
    self._Tiles[TileToUse].SetPiece(NewPiece)
    return 3

  def __ExecuteUpgradeCommand(self, Items, LumberAvailable):
    TileToUse = int(Items[2])
    if not self.__CheckPieceAndTileAreValid(TileToUse) or LumberAvailable < 5 or not (Items[1] == "pbds" or Items[1] == "less"):
      return -1
    else:
      ThePiece = self._Tiles[TileToUse].GetPieceInTile()
      if ThePiece.GetPieceType().upper() != "S":
        return -1
      ThePiece.DestroyPiece()
      if Items[1] == "pbds":
        ThePiece = PBDSPiece(self._Player1Turn)
      else:
        ThePiece = LESSPiece(self._Player1Turn)
      self._Pieces.append(ThePiece)
      self._Tiles[TileToUse].SetPiece(ThePiece)
      return 5

  def __SetUpTiles(self):
    EvenStartY = 0
    EvenStartZ = 0
    OddStartZ = 0
    OddStartY = -1
    for count in range (1, self._Size // 2 + 1):
      y = EvenStartY
      z = EvenStartZ
      for x in range (0, self._Size - 1, 2):
        TempTile = Tile(x, y, z)
        self._Tiles.append(TempTile)
        y -= 1
        z -= 1
      EvenStartZ += 1
      EvenStartY -= 1
      y = OddStartY
      z = OddStartZ
      for x in range (1, self._Size, 2):
        TempTile = Tile(x, y, z)
        self._Tiles.append(TempTile)
        y -= 1
        z -= 1
      OddStartZ += 1
      OddStartY -= 1

  def __SetUpNeighbours(self):
    for FromTile in self._Tiles:
      for ToTile in self._Tiles:
        if FromTile.GetDistanceToTileT(ToTile) == 1:
          FromTile.AddToNeighbours(ToTile)

  def DestroyPiecesAndCountVPs(self):
    BaronDestroyed = False
    Player1VPs = 0
    Player2VPs = 0
    ListOfTilesContainingDestroyedPieces = []
    for T in self._Tiles:
      if T.GetPieceInTile() is not None:
        ListOfNeighbours = T.GetNeighbours()
        NoOfConnections = 0
        for N in ListOfNeighbours:
          if N.GetPieceInTile() is not None:
            NoOfConnections += 1
        ThePiece = T.GetPieceInTile()
        if NoOfConnections >= ThePiece.GetConnectionsNeededToDestroy():
          ThePiece.DestroyPiece()
          if ThePiece.GetPieceType().upper() == "B":
            BaronDestroyed = True
          ListOfTilesContainingDestroyedPieces.append(T)
          if ThePiece.GetBelongsToPlayer1():
            Player2VPs += ThePiece.GetVPs()
          else:
            Player1VPs += ThePiece.GetVPs()
    for T in ListOfTilesContainingDestroyedPieces:
      T.SetPiece(None)
    return BaronDestroyed, Player1VPs, Player2VPs

  def get_grid_index(self): # Added this function to number cells
    self.grid_index += 1
    return f"{self.grid_index}{'_' if len(str(self.grid_index)) == 1 else ''}"

  def GetGridAsString(self, P1Turn):
    self.__ListPositionOfTile = 0
    self._Player1Turn = P1Turn
    GridAsString = self.__CreateTopLine() + self.__CreateEvenLine(True)
    self.__ListPositionOfTile += 1
    GridAsString += self.__CreateOddLine()
    for count in range (1, self._Size - 1, 2):
      self.__ListPositionOfTile += 1
      GridAsString += self.__CreateEvenLine(False)
      self.__ListPositionOfTile += 1
      GridAsString += self.__CreateOddLine()
    return GridAsString + self.__CreateBottomLine()

  def __MovePiece(self, NewIndex, OldIndex):
    self._Tiles[NewIndex].SetPiece(self._Tiles[OldIndex].GetPieceInTile())
    self._Tiles[OldIndex].SetPiece(None)

  def GetPieceTypeInTile(self, ID, display=False): # Added display
    ThePiece = self._Tiles[ID].GetPieceInTile()
    if ThePiece is None:
      return " "
    else:
      return ThePiece.GetPieceType() if not display else map_icon(ThePiece.GetPieceType()) # Added map_icon

  def __CreateBottomLine(self):
    Line = "   "
    for count in range (1, self._Size // 2 + 1):
      Line += f" \\{self.get_grid_index()}/ " # Edited this line
    self.grid_index = -1 # Added to reset get_grid_index()
    return Line + os.linesep

  def __CreateTopLine(self):
    Line = os.linesep + "  "
    for count in range (1, self._Size // 2 + 1):
      Line += "__    "
    return Line + os.linesep

  def __CreateOddLine(self):
    Line = ""
    for count in range (1, self._Size // 2 + 1):
      if count > 1 and count < self._Size // 2:
        Line += self.GetPieceTypeInTile(self.__ListPositionOfTile, display=True) + f"\\{self.get_grid_index()}/" # Edited this line
        self.__ListPositionOfTile += 1
        Line += self._Tiles[self.__ListPositionOfTile].GetTerrain(display=True) # Edited this line
      elif count == 1:
        Line += f" \\{self.get_grid_index()}/" + self._Tiles[self.__ListPositionOfTile].GetTerrain(display=True) # Edited this line
    Line += self.GetPieceTypeInTile(self.__ListPositionOfTile, display=True) + f"\\{self.get_grid_index()}/" # Edited this line
    self.__ListPositionOfTile += 1
    if self.__ListPositionOfTile < len(self._Tiles):
      Line += self._Tiles[self.__ListPositionOfTile].GetTerrain(display=True) + self.GetPieceTypeInTile(self.__ListPositionOfTile, display=True) + "\\" + os.linesep # Edited this line
    else:
      Line += "\\" + os.linesep
    return Line

  def __CreateEvenLine(self, FirstEvenLine):
    Line = " /" + self._Tiles[self.__ListPositionOfTile].GetTerrain(display=True) # Edited this line
    for count in range (1, self._Size // 2):
      Line += self.GetPieceTypeInTile(self.__ListPositionOfTile, display=True) # Edited this line
      self.__ListPositionOfTile += 1
      Line += f"\\{'__' if FirstEvenLine else self.get_grid_index()}/" + self._Tiles[self.__ListPositionOfTile].GetTerrain(display=True) # Edited this line
    if FirstEvenLine:
      Line += self.GetPieceTypeInTile(self.__ListPositionOfTile, display=True) + "\\__" + os.linesep # Edited this line
    else:
      Line += self.GetPieceTypeInTile(self.__ListPositionOfTile, display=True) + f"\\{self.get_grid_index()}/" + os.linesep # Edited this line
    return Line

class Player:
  def __init__(self, N, V, F, L, T):
    self._Name = N
    self._VPs = V
    self._Fuel = F
    self._Lumber = L
    self._PiecesInSupply = T

  def GetStateString(self):
    return "VPs: " + str(self._VPs) + "   Pieces in supply: " + str(self._PiecesInSupply) + "   Lumber: " + str(self._Lumber) + "   Fuel: " + str(self._Fuel)

  def GetVPs(self):
    return self._VPs

  def GetFuel(self):
    return self._Fuel

  def GetLumber(self):
    return self._Lumber

  def GetName(self):
    return self._Name

  def AddToVPs(self, n):
    self._VPs += n

  def UpdateFuel(self, n):
    self._Fuel += n

  def UpdateLumber(self, n):
    self._Lumber += n

  def GetPiecesInSupply(self):
    return self._PiecesInSupply

  def RemoveTileFromSupply(self):
    self._PiecesInSupply -= 1

def Main():
  FileLoaded = True
  Player1 = None
  Player2 = None
  Grid = None
  Choice = ""
  while Choice != "Q":
    DisplayMainMenu()
    Choice = input()
    if Choice == "1":
      Player1, Player2, Grid = SetUpDefaultGame()
      PlayGame(Player1, Player2, Grid)
    elif Choice == "2":
      FileLoaded, Player1, Player2, Grid = LoadGame()
      if FileLoaded:
        PlayGame(Player1, Player2, Grid)

def LoadGame():
  FileName = input("Enter the name of the file to load: ")
  Items = []
  LineFromFile = ""
  Player1 = None
  Player2 = None
  Grid = None
  try:
    with open(FileName) as f:
      LineFromFile = f.readline().rstrip()
      Items = LineFromFile.split(",")
      Player1 = Player(Items[0], int(Items[1]), int(Items[2]), int(Items[3]), int(Items[4]))
      LineFromFile = f.readline().rstrip()
      Items = LineFromFile.split(",")
      Player2 = Player(Items[0], int(Items[1]), int(Items[2]), int(Items[3]), int(Items[4]))
      GridSize = int(f.readline().rstrip())
      Grid = HexGrid(GridSize)
      T = f.readline().rstrip().split(",")
      Grid.SetUpGridTerrain(T)
      LineFromFile = f.readline().rstrip()
      while LineFromFile != "":
        Items = LineFromFile.split(",")
        if Items[0] == "1":
          Grid.AddPiece(True, Items[1], int(Items[2]))
        else:
          Grid.AddPiece(False, Items[1], int(Items[2]))
        LineFromFile = f.readline().rstrip()
  except:
    print("File not loaded")
    return False, Player1, Player2, Grid
  return True, Player1, Player2, Grid

def SetUpDefaultGame():
  T = [" ", "#", "#", " ", "~", "~", " ", " ", " ", "~", " ", "#", "#", " ", " ", " ", " ", " ", "#", "#", "#", "#", "~", "~", "~", "~", "~", " ", "#", " ", "#", " "]
  GridSize = 8
  Grid = HexGrid(GridSize)
  Player1 = Player("Player One", 0, 10, 10, 5)
  Player2 = Player("Player Two", 1, 10, 10, 5)
  Grid.SetUpGridTerrain(T)
  Grid.AddPiece(True, "Baron", 0)
  Grid.AddPiece(True, "Serf", 8)
  Grid.AddPiece(False, "Baron", 31)
  Grid.AddPiece(False, "Serf", 23)
  return Player1, Player2, Grid

def CheckMoveCommandFormat(Items):
  if len(Items) == 3:
    for Count in range (1, 3):
      try:
        Result = int(Items[Count])
      except:
        return False
    return True
  return False

def CheckStandardCommandFormat(Items):
  if len(Items) == 2:
    try:
      Result = int(Items[1])
    except:
      return False
    return True
  return False

def CheckUpgradeCommandFormat(Items):
  if len(Items) == 3:
    if Items[1].upper() != "LESS" and Items[1].upper() != "PBDS":
      return False
    try:
      Result = int(Items[2])
    except:
      return False
    return True
  return False

def CheckCommandIsValid(Items):
  if len(Items) > 0:
    if Items[0] == "move":
      return CheckMoveCommandFormat(Items)
    elif Items[0] in ["dig", "saw", "spawn"]:
      return CheckStandardCommandFormat(Items)
    elif Items[0] == "upgrade":
      return CheckUpgradeCommandFormat(Items)
  return False

def PlayGame(Player1, Player2, Grid):
  GameOver = False
  Player1Turn = True
  Commands = []
  print("Player One current state - " + Player1.GetStateString())
  print("Player Two current state - " + Player2.GetStateString())
  while not (GameOver and Player1Turn):
    print(Grid.GetGridAsString(Player1Turn))
    if Player1Turn:
      print(Player1.GetName() + " state your three commands, pressing enter after each one.")
    else:
      print(Player2.GetName() + " state your three commands, pressing enter after each one.")
    for Count in range (1, 4):
      Commands.append(input("Enter command: ").lower().strip()) # Added .strip() for convenience
    for C in Commands:
      Items = C.split(" ")
      ValidCommand = CheckCommandIsValid(Items)
      if not ValidCommand:
        print("Invalid command")
      else:
        FuelChange = 0
        LumberChange = 0
        SupplyChange = 0
        if Player1Turn:
          SummaryOfResult, FuelChange, LumberChange, SupplyChange = Grid.ExecuteCommand(Items, Player1.GetFuel(), Player1.GetLumber(), Player1.GetPiecesInSupply())
          Player1.UpdateLumber(LumberChange)
          Player1.UpdateFuel(FuelChange)
          if SupplyChange == 1:
            Player1.RemoveTileFromSupply()
        else:
          SummaryOfResult, FuelChange, LumberChange, SupplyChange = Grid.ExecuteCommand(Items, Player2.GetFuel(), Player2.GetLumber(), Player2.GetPiecesInSupply())
          Player2.UpdateLumber(LumberChange)
          Player2.UpdateFuel(FuelChange)
          if SupplyChange == 1:
            Player2.RemoveTileFromSupply()
        print(SummaryOfResult)
    Commands.clear()
    Player1Turn = not Player1Turn
    Player1VPsGained = 0
    Player2VPsGained = 0
    if GameOver:
      GameOver, Player1VPsGained, Player2VPsGained = Grid.DestroyPiecesAndCountVPs()
      GameOver = True
    else:
      GameOver, Player1VPsGained, Player2VPsGained = Grid.DestroyPiecesAndCountVPs()
    Player1.AddToVPs(Player1VPsGained)
    Player2.AddToVPs(Player2VPsGained)
    print("Player One current state - " + Player1.GetStateString())
    print("Player Two current state - " + Player2.GetStateString())
    input("Press Enter to continue...")
  print(Grid.GetGridAsString(Player1Turn))
  DisplayEndMessages(Player1, Player2)

def DisplayEndMessages(Player1, Player2):
  print()
  print(Player1.GetName() + " final state: " + Player1.GetStateString())
  print()
  print(Player2.GetName() + " final state: " + Player2.GetStateString())
  print()
  if Player1.GetVPs() > Player2.GetVPs():
    print(Player1.GetName() + " is the winner!")
  else:
    print(Player2.GetName() + " is the winner!")

def DisplayMainMenu():
  print("1. Default game")
  print("2. Load game")
  print("Q. Quit")
  print()
  print("Enter your choice: ", end="")

if __name__ == "__main__":
  Main()