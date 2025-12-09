package yahtzee

import Dice.*

object Game:
  
  def rollDice(dice: List[Dice], seed: Long): (List[Dice], Long) =
    dice.foldLeft((List.empty[Dice], seed)) { case ((acc, s), d) =>
      val (newDice, newSeed) = d.roll(s)
      (acc :+ newDice, newSeed)
    }
  
  def rollSpecificDice(dice: List[Dice], indices: Set[Int], seed: Long): (List[Dice], Long) =
    dice.zipWithIndex.foldLeft((List.empty[Dice], seed)) { case ((acc, s), (d, i)) =>
      if indices.contains(i) then
        val (newDice, newSeed) = d.roll(s)
        (acc :+ newDice, newSeed)
      else
        (acc :+ d, s)
    }
  
  def getDiceValues(dice: List[Dice]): List[Int] = 
    dice.map(_.value)
  
  def getSortedDice(dice: List[Dice]): List[Int] = 
    getDiceValues(dice).sorted
  
  def getFrequency(dice: List[Dice]): List[Int] =
    val values = getDiceValues(dice)
    (1 to 6).map(n => values.count(_ == n)).toList
  
  def calculateScore(dice: List[Dice], slotIdx: Int): Int =
    val values = getDiceValues(dice)
    val sortedValues = getSortedDice(dice)
    val freq = getFrequency(dice)
    
    slotIdx match
      case n if n < 6 => 
        values.filter(_ == n + 1).sum
      
      case 6 => 
        if freq.exists(_ >= 3) then values.sum else 0
      
      case 7 => 
        if freq.exists(_ >= 4) then values.sum else 0
      
      case 8 => 
        if freq.count(_ == 0) == 4 && freq.contains(3) && freq.contains(2) then 25 else 0
      
      case 9 => 
        if isSmallStraight(sortedValues) then 30 else 0
      
      case 10 => 
        if isLargeStraight(sortedValues) then 40 else 0
      
      case 11 => 
        if freq.max == 5 then 50 else 0
      
      case 12 => 
        values.sum
      
      case _ => 0
  
  def isSmallStraight(sortedValues: List[Int]): Boolean =
    val straights = List(List(1, 2, 3, 4), List(2, 3, 4, 5), List(3, 4, 5, 6))
    straights.exists(s => s.forall(sortedValues.contains))
  
  def isLargeStraight(sortedValues: List[Int]): Boolean = 
    sortedValues == List(1, 2, 3, 4, 5) || sortedValues == List(2, 3, 4, 5, 6)
