package yahtzee

opaque type Dice = Int

object Dice:
  def apply(value: Int): Dice = 
    require(value >= 1 && value <= 6, "Face value must be between 1 and 6")
    value
  
  extension (d: Dice)
    def value: Int = d
    
    def roll(seed: Long): (Dice, Long) =
      val newSeed = (seed * 0x5DEECE66DL + 0xBL) & 0xFFFFFFFFFFFFL
      val newValue = ((newSeed >>> 16).toInt.abs % 6) + 1
      (Dice(newValue), newSeed)
  
  def create(seed: Long): (Dice, Long) =
    val newSeed = (seed * 0x5DEECE66DL + 0xBL) & 0xFFFFFFFFFFFFL
    val value = ((newSeed >>> 16).toInt.abs % 6) + 1
    (Dice(value), newSeed)
