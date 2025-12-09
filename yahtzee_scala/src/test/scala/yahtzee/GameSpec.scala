package yahtzee

import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers
import Dice.*

class GameSpec extends AnyFlatSpec with Matchers:
  
  "Game.rollDice" should "roll all dice" in {
    val dice = List.fill(5)(Dice(1))
    val (rolled, _) = Game.rollDice(dice, 42L)
    rolled should have length 5
    rolled.forall(d => d.value >= 1 && d.value <= 6) shouldBe true
  }
  
  "Game.rollSpecificDice" should "only roll specified indices" in {
    val dice = List(Dice(1), Dice(2), Dice(3), Dice(4), Dice(5))
    val (rolled, _) = Game.rollSpecificDice(dice, Set(0, 2), 42L)
    
    rolled(1).value shouldBe 2
    rolled(3).value shouldBe 4
  }
  
  "Game.getDiceValues" should "return list of values" in {
    val dice = List(Dice(1), Dice(3), Dice(5))
    Game.getDiceValues(dice) shouldBe List(1, 3, 5)
  }
  
  "Game.getSortedDice" should "return sorted values" in {
    val dice = List(Dice(5), Dice(2), Dice(6), Dice(1), Dice(3))
    Game.getSortedDice(dice) shouldBe List(1, 2, 3, 5, 6)
  }
  
  "Game.getFrequency" should "count dice frequencies" in {
    val dice = List(Dice(1), Dice(1), Dice(3), Dice(3), Dice(3))
    Game.getFrequency(dice) shouldBe List(2, 0, 3, 0, 0, 0)
  }
  
  "Game.calculateScore" should "score ones correctly" in {
    val dice = List(Dice(1), Dice(1), Dice(3), Dice(4), Dice(1))
    Game.calculateScore(dice, 0) shouldBe 3
  }
  
  it should "score twos correctly" in {
    val dice = List(Dice(2), Dice(2), Dice(2), Dice(4), Dice(5))
    Game.calculateScore(dice, 1) shouldBe 6
  }
  
  it should "score three of a kind" in {
    val dice = List(Dice(3), Dice(3), Dice(3), Dice(4), Dice(5))
    Game.calculateScore(dice, 6) shouldBe 18
    
    val noDice = List(Dice(1), Dice(2), Dice(3), Dice(4), Dice(5))
    Game.calculateScore(noDice, 6) shouldBe 0
  }
  
  it should "score four of a kind" in {
    val dice = List(Dice(5), Dice(5), Dice(5), Dice(5), Dice(2))
    Game.calculateScore(dice, 7) shouldBe 22
    
    val noDice = List(Dice(5), Dice(5), Dice(5), Dice(2), Dice(3))
    Game.calculateScore(noDice, 7) shouldBe 0
  }
  
  it should "score full house" in {
    val dice = List(Dice(2), Dice(2), Dice(2), Dice(5), Dice(5))
    Game.calculateScore(dice, 8) shouldBe 25
    
    val noDice = List(Dice(2), Dice(2), Dice(3), Dice(4), Dice(5))
    Game.calculateScore(noDice, 8) shouldBe 0
  }
  
  it should "score small straight" in {
    val dice1 = List(Dice(1), Dice(2), Dice(3), Dice(4), Dice(6))
    Game.calculateScore(dice1, 9) shouldBe 30
    
    val dice2 = List(Dice(2), Dice(3), Dice(4), Dice(5), Dice(6))
    Game.calculateScore(dice2, 9) shouldBe 30
    
    val dice3 = List(Dice(3), Dice(4), Dice(5), Dice(6), Dice(1))
    Game.calculateScore(dice3, 9) shouldBe 30
    
    val noDice = List(Dice(1), Dice(2), Dice(4), Dice(5), Dice(6))
    Game.calculateScore(noDice, 9) shouldBe 0
  }
  
  it should "score large straight" in {
    val dice1 = List(Dice(1), Dice(2), Dice(3), Dice(4), Dice(5))
    Game.calculateScore(dice1, 10) shouldBe 40
    
    val dice2 = List(Dice(2), Dice(3), Dice(4), Dice(5), Dice(6))
    Game.calculateScore(dice2, 10) shouldBe 40
    
    val noDice = List(Dice(1), Dice(2), Dice(3), Dice(4), Dice(6))
    Game.calculateScore(noDice, 10) shouldBe 0
  }
  
  it should "score yahtzee" in {
    val dice = List(Dice(4), Dice(4), Dice(4), Dice(4), Dice(4))
    Game.calculateScore(dice, 11) shouldBe 50
    
    val noDice = List(Dice(4), Dice(4), Dice(4), Dice(4), Dice(5))
    Game.calculateScore(noDice, 11) shouldBe 0
  }
  
  it should "score chance" in {
    val dice = List(Dice(1), Dice(2), Dice(3), Dice(4), Dice(5))
    Game.calculateScore(dice, 12) shouldBe 15
  }
  
  "Game.isSmallStraight" should "detect small straights" in {
    Game.isSmallStraight(List(1, 2, 3, 4, 6)) shouldBe true
    Game.isSmallStraight(List(2, 3, 4, 5, 6)) shouldBe true
    Game.isSmallStraight(List(1, 3, 4, 5, 6)) shouldBe true
    Game.isSmallStraight(List(1, 2, 2, 3, 4)) shouldBe true
    Game.isSmallStraight(List(1, 2, 4, 5, 6)) shouldBe false
  }
  
  "Game.isLargeStraight" should "detect large straights" in {
    Game.isLargeStraight(List(1, 2, 3, 4, 5)) shouldBe true
    Game.isLargeStraight(List(2, 3, 4, 5, 6)) shouldBe true
    Game.isLargeStraight(List(1, 2, 3, 4, 6)) shouldBe false
    Game.isLargeStraight(List(1, 2, 2, 3, 4)) shouldBe false
  }
