package yahtzee

import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers
import Dice.*

class DiceSpec extends AnyFlatSpec with Matchers:
  
  "Dice" should "create with valid value between 1 and 6" in {
    val (dice, _) = Dice.create(42L)
    dice.value should (be >= 1 and be <= 6)
  }
  
  it should "throw exception for invalid values" in {
    assertThrows[IllegalArgumentException] {
      Dice(0)
    }
    assertThrows[IllegalArgumentException] {
      Dice(7)
    }
    assertThrows[IllegalArgumentException] {
      Dice(-1)
    }
  }
  
  it should "roll and return new dice with valid value" in {
    val dice = Dice(3)
    val (newDice, newSeed) = dice.roll(42L)
    
    newDice.value should (be >= 1 and be <= 6)
    newSeed should not be 42L
  }
  
  it should "not mutate original dice when rolling" in {
    val original = Dice(3)
    original.roll(42L)
    original.value shouldBe 3
  }
  
  it should "produce different values over multiple rolls" in {
    val dice = Dice(1)
    val values = (1 to 100).foldLeft((Set.empty[Int], 42L)) { case ((acc, seed), _) =>
      val (newDice, newSeed) = dice.roll(seed)
      (acc + newDice.value, newSeed)
    }._1
    values.size should be > 1
  }
  
  it should "be deterministic with same seed" in {
    val dice = Dice(1)
    val (dice1, _) = dice.roll(42L)
    val (dice2, _) = dice.roll(42L)
    dice1.value shouldBe dice2.value
  }
