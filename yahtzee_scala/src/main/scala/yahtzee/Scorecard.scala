package yahtzee

case class Scorecard(numPlayers: Int, cards: Map[(Int, Int), Int]):
  require(numPlayers > 0, "Must have at least one player")
  
  def getScore(playerIdx: Int, slotIdx: Int): Either[String, Int] =
    if playerIdx < 0 || playerIdx >= numPlayers then 
      Left("Invalid player index")
    else if slotIdx < 0 || slotIdx >= 13 then 
      Left("Invalid slot index")
    else 
      Right(cards.getOrElse((playerIdx, slotIdx), 0))
  
  def setScore(playerIdx: Int, slotIdx: Int, value: Int): Either[String, Scorecard] =
    if playerIdx < 0 || playerIdx >= numPlayers then 
      Left("Invalid player index")
    else if slotIdx < 0 || slotIdx >= 13 then 
      Left("Invalid slot index")
    else 
      Right(copy(cards = cards + ((playerIdx, slotIdx) -> value)))
  
  def getPlayerCard(playerIdx: Int): Either[String, List[Int]] =
    if playerIdx < 0 || playerIdx >= numPlayers then 
      Left("Invalid player index")
    else 
      Right((0 until 13).map(slot => cards.getOrElse((playerIdx, slot), 0)).toList)

object Scorecard:
  def apply(numPlayers: Int): Scorecard = 
    Scorecard(numPlayers, Map.empty)
