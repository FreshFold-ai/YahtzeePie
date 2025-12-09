package yahtzee

import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers

class ScorecardSpec extends AnyFlatSpec with Matchers:
  
  "Scorecard" should "initialize with correct number of players" in {
    val scorecard = Scorecard(3)
    scorecard.numPlayers shouldBe 3
  }
  
  it should "return 0 for all initial scores" in {
    val scorecard = Scorecard(2)
    (0 until 2).foreach { player =>
      (0 until 13).foreach { slot =>
        scorecard.getScore(player, slot) shouldBe Right(0)
      }
    }
  }
  
  it should "set and get scores correctly" in {
    val scorecard = Scorecard(2)
    val updated = scorecard.setScore(0, 5, 30).getOrElse(fail())
    updated.getScore(0, 5) shouldBe Right(30)
  }
  
  it should "return error for invalid player index" in {
    val scorecard = Scorecard(2)
    scorecard.getScore(-1, 0).isLeft shouldBe true
    scorecard.getScore(2, 0).isLeft shouldBe true
    scorecard.setScore(-1, 0, 10).isLeft shouldBe true
    scorecard.setScore(2, 0, 10).isLeft shouldBe true
  }
  
  it should "return error for invalid slot index" in {
    val scorecard = Scorecard(2)
    scorecard.getScore(0, -1).isLeft shouldBe true
    scorecard.getScore(0, 13).isLeft shouldBe true
    scorecard.setScore(0, -1, 10).isLeft shouldBe true
    scorecard.setScore(0, 13, 10).isLeft shouldBe true
  }
  
  it should "not mutate original when setting score" in {
    val original = Scorecard(1)
    original.setScore(0, 0, 10)
    original.getScore(0, 0) shouldBe Right(0)
  }
  
  it should "return correct player card" in {
    val scorecard = Scorecard(2)
      .setScore(0, 0, 3).getOrElse(fail())
      .setScore(0, 5, 15).getOrElse(fail())
    
    val card = scorecard.getPlayerCard(0).getOrElse(fail())
    card should have length 13
    card(0) shouldBe 3
    card(5) shouldBe 15
  }
  
  it should "keep players independent" in {
    val scorecard = Scorecard(3)
      .setScore(0, 0, 10).getOrElse(fail())
      .setScore(1, 0, 20).getOrElse(fail())
      .setScore(2, 0, 30).getOrElse(fail())
    
    scorecard.getScore(0, 0) shouldBe Right(10)
    scorecard.getScore(1, 0) shouldBe Right(20)
    scorecard.getScore(2, 0) shouldBe Right(30)
  }
