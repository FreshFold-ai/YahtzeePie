package yahtzee

case class GameState(
  dice: List[Dice],
  scorecard: Scorecard,
  currentPlayer: Int,
  currentRound: Int,
  rollsLeft: Int,
  seed: Long
):
  
  def rollDice(indices: Set[Int]): GameState =
    val (newDice, newSeed) = 
      if indices.isEmpty then (dice, seed)
      else Game.rollSpecificDice(dice, indices, seed)
    copy(dice = newDice, rollsLeft = rollsLeft - 1, seed = newSeed)
  
  def recordScore(slotIdx: Int): Either[String, GameState] =
    val score = Game.calculateScore(dice, slotIdx)
    scorecard.setScore(currentPlayer, slotIdx, score).map { newScorecard =>
      val nextPlayer = (currentPlayer + 1) % scorecard.numPlayers
      val nextRound = if nextPlayer == 0 then currentRound + 1 else currentRound
      copy(scorecard = newScorecard, currentPlayer = nextPlayer, currentRound = nextRound, rollsLeft = 3)
    }
  
  def isGameOver: Boolean = currentRound >= 13

object GameState:
  def initial(numPlayers: Int, seed: Long): GameState =
    val (dice, newSeed) = (0 until 5).foldLeft((List.empty[Dice], seed)) { case ((acc, s), _) =>
      val (d, ns) = Dice.create(s)
      (acc :+ d, ns)
    }
    GameState(dice, Scorecard(numPlayers), 0, 0, 3, newSeed)
