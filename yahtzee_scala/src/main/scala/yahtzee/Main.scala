package yahtzee

import scala.io.StdIn
import scala.util.Try
import Dice.*

@main def run(): Unit =
  val seed = System.currentTimeMillis()
  val numPlayers = getNumPlayers()
  println(s"Starting Yahtzee with $numPlayers players!")
  
  val initialState = GameState.initial(numPlayers, seed)
  gameLoop(initialState)

def getNumPlayers(): Int =
  println("How many players? ")
  Try(StdIn.readLine().trim.toInt).filter(_ > 0).getOrElse {
    println("Invalid input. Please enter a positive integer.")
    getNumPlayers()
  }

def displayDice(dice: List[Dice], kept: Set[Int]): Unit =
  val values = dice.zipWithIndex.map { (d, i) =>
    if kept.contains(i) then s"[${d.value}]" else s" ${d.value} "
  }.mkString(" ")
  val indices = dice.indices.map { i => 
    if kept.contains(i) then s"[${i+1}]" else s" ${i+1} "
  }.mkString(" ")
  
  println(s"Values: $values")
  println(s"Dice#:  $indices")
  if kept.nonEmpty then println(s"(Kept: ${kept.map(_ + 1).toList.sorted.mkString(", ")})")

def getRerollIndices(): Set[Int] =
  println("Enter dice numbers to reroll (1-5, space-separated), or press Enter to keep all: ")
  val input = StdIn.readLine().trim
  if input.isEmpty then Set.empty
  else
    Try {
      input.split("\\s+").map(_.toInt - 1).filter(i => i >= 0 && i < 5).toSet
    }.getOrElse {
      println("Invalid input. Please enter numbers 1-5.")
      getRerollIndices()
    }

def displayScorecard(state: GameState): Unit =
  val categories = List(
    "Ones", "Twos", "Threes", "Fours", "Fives", "Sixes",
    "3 of a Kind", "4 of a Kind", "Full House", "Small Straight",
    "Large Straight", "Yahtzee", "Chance"
  )
  
  println("=" * 60)
  println(s"Player ${state.currentPlayer + 1} Scorecard")
  println("=" * 60)
  
  state.scorecard.getPlayerCard(state.currentPlayer).foreach { card =>
    card.zipWithIndex.foreach { (score, idx) =>
      val status = if score == 0 then "✓ OPEN" else "✗ USED"
      val display = if score == 0 then "-" else score.toString
      println(f"$idx%-2d ${categories(idx)}%-20s $display%-8s $status")
    }
  }
  println("=" * 60)

def getSlotChoice(state: GameState): Int =
  displayScorecard(state)
  println(s"\nChoose an open scoring slot (0-12) for Player ${state.currentPlayer + 1}: ")
  
  val slotOpt = for {
    slot <- Try(StdIn.readLine().trim.toInt).toOption
    if slot >= 0 && slot < 13
    score <- state.scorecard.getScore(state.currentPlayer, slot).toOption
    if score == 0
  } yield slot
  
  slotOpt.getOrElse {
    println("Invalid or used slot. Choose an open slot (0-12).")
    getSlotChoice(state)
  }

def playTurn(state: GameState, kept: Set[Int] = Set.empty): GameState =
  if state.rollsLeft == 0 then
    val slot = getSlotChoice(state)
    state.recordScore(slot).getOrElse(state)
  else
    println(s"\nRoll ${4 - state.rollsLeft}/3:")
    val rolled = state.rollDice(if state.rollsLeft == 3 then Set(0, 1, 2, 3, 4) else kept)
    displayDice(rolled.dice, Set.empty)
    
    if rolled.rollsLeft > 0 then
      val reroll = getRerollIndices()
      playTurn(rolled, reroll)
    else
      println(s"\nFinal dice: ${Game.getDiceValues(rolled.dice).mkString(", ")}")
      val slot = getSlotChoice(rolled)
      rolled.recordScore(slot).getOrElse(rolled)

def gameLoop(state: GameState): Unit =
  if state.isGameOver then
    println("\nGame Over!")
  else
    println(s"\n${"=" * 60}")
    println(s"ROUND ${state.currentRound + 1}")
    println(s"${"=" * 60}")
    println(s"--- Player ${state.currentPlayer + 1}'s Turn ---")
    
    val newState = playTurn(state)
    gameLoop(newState)
