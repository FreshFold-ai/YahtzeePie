package analysis

import yahtzee.*
import yahtzee.Dice.*
import scala.util.Using
import java.io.PrintWriter
import scala.collection.mutable.ArrayBuffer

case class PerformanceMetrics(
  executionTimeMs: Double,
  executionTimeStd: Double,
  memoryUsedKb: Double,
  memoryStdKb: Double,
  numTrials: Int,
  samplesPerTrial: Int
)

object PerformanceProfiler:
  
  // Configuration optimized for memory measurement
  val NUM_TRIALS = 3
  val SAMPLES_PER_TRIAL = 15
  val WARMUP_ITERATIONS = 10
  val BATCH_SIZE = 1000  // Create multiple objects per measurement
  
  def calculateMean(values: Seq[Double]): Double =
    values.sum / values.length
  
  def calculateStdDev(values: Seq[Double], mean: Double): Double =
    if values.length <= 1 then 0.0
    else
      val variance = values.map(v => Math.pow(v - mean, 2)).sum / values.length
      Math.sqrt(variance)
  
  def profileMethod[T](name: String)(f: => T): PerformanceMetrics =
    // Warmup phase (reduced to keep measurements faster)
    (0 until WARMUP_ITERATIONS).foreach(_ => f)
    
    val allTrialTimes = ArrayBuffer[Double]()
    val allTrialMemory = ArrayBuffer[Double]()
    
    for trial <- 0 until NUM_TRIALS do
      val sampleTimes = ArrayBuffer[Double]()
      val sampleMemory = ArrayBuffer[Double]()
      
      // Aggressive GC and stabilization
      System.gc()
      System.runFinalization()
      System.gc()
      Thread.sleep(200)
      
      val runtime = Runtime.getRuntime
      
      for sample <- 0 until SAMPLES_PER_TRIAL do
        // Baseline memory after GC
        System.gc()
        Thread.sleep(50)
        val memBefore = runtime.totalMemory() - runtime.freeMemory()
        
        // Create multiple objects in a batch to amplify memory footprint
        val startTime = System.nanoTime()
        val results = ArrayBuffer[T]()
        var i = 0
        while i < BATCH_SIZE do
          results += f
          i += 1
        val endTime = System.nanoTime()
        
        // Force retention by accessing results
        val _ = results.length
        
        // Measure memory immediately after
        val memAfter = runtime.totalMemory() - runtime.freeMemory()
        
        // Time per single operation
        sampleTimes += (endTime - startTime) / 1e6 / BATCH_SIZE
        // Memory per single operation
        val memDiff = (memAfter - memBefore) / 1024.0 / BATCH_SIZE
        sampleMemory += math.max(0.0, memDiff)
      
      // Calculate mean for this trial
      allTrialTimes += calculateMean(sampleTimes.toSeq)
      allTrialMemory += calculateMean(sampleMemory.toSeq)
    
    // Calculate statistics across all trials
    val timeMean = calculateMean(allTrialTimes.toSeq)
    val timeStd = calculateStdDev(allTrialTimes.toSeq, timeMean)
    val memMean = calculateMean(allTrialMemory.toSeq)
    val memStd = calculateStdDev(allTrialMemory.toSeq, memMean)
    
    PerformanceMetrics(timeMean, timeStd, memMean, memStd, NUM_TRIALS, SAMPLES_PER_TRIAL)
  
  def profileDice(): Map[String, PerformanceMetrics] =
    val results = scala.collection.mutable.Map[String, PerformanceMetrics]()
    var seed = 12345L
    
    // Dice creation
    results("dice_create") = profileMethod("dice_create") {
      val (d, s) = Dice.create(seed)
      seed = s
      d
    }
    
    // Dice apply
    results("dice_apply") = profileMethod("dice_apply") {
      Dice(3)
    }
    
    // Dice value access
    val dice = Dice(3)
    results("dice_value") = profileMethod("dice_value") {
      dice.value
    }
    
    // Dice roll
    results("dice_roll") = profileMethod("dice_roll") {
      val (d, s) = dice.roll(seed)
      seed = s
      d
    }
    
    results.toMap
  
  def profileScorecard(): Map[String, PerformanceMetrics] =
    val results = scala.collection.mutable.Map[String, PerformanceMetrics]()
    
    // Scorecard creation
    results("scorecard_apply") = profileMethod("scorecard_apply") {
      Scorecard(2)
    }
    
    val scorecard = Scorecard(2)
    
    // Get score
    results("scorecard_getScore") = profileMethod("scorecard_getScore") {
      scorecard.getScore(0, 0)
    }
    
    // Set score
    results("scorecard_setScore") = profileMethod("scorecard_setScore") {
      scorecard.setScore(0, 0, 10)
    }
    
    // Get player card
    results("scorecard_getPlayerCard") = profileMethod("scorecard_getPlayerCard") {
      scorecard.getPlayerCard(0)
    }
    
    results.toMap
  
  def profileGame(): Map[String, PerformanceMetrics] =
    val results = scala.collection.mutable.Map[String, PerformanceMetrics]()
    var seed = 12345L
    
    // Create test dice
    val (dice, newSeed) = (0 until 5).foldLeft((List.empty[Dice], seed)) { case ((acc, s), _) =>
      val (d, ns) = Dice.create(s)
      (acc :+ d, ns)
    }
    seed = newSeed
    
    // Roll dice
    results("game_rollDice") = profileMethod("game_rollDice") {
      val (d, s) = Game.rollDice(dice, seed)
      seed = s
      d
    }
    
    // Roll specific dice
    results("game_rollSpecificDice") = profileMethod("game_rollSpecificDice") {
      val (d, s) = Game.rollSpecificDice(dice, Set(0, 2, 4), seed)
      seed = s
      d
    }
    
    // Get dice values
    results("game_getDiceValues") = profileMethod("game_getDiceValues") {
      Game.getDiceValues(dice)
    }
    
    // Get sorted dice
    results("game_getSortedDice") = profileMethod("game_getSortedDice") {
      Game.getSortedDice(dice)
    }
    
    // Get frequency
    results("game_getFrequency") = profileMethod("game_getFrequency") {
      Game.getFrequency(dice)
    }
    
    // Calculate scores for all categories
    (0 until 13).foreach { slot =>
      val categoryName = slot match
        case 0 => "ones"
        case 1 => "twos"
        case 2 => "threes"
        case 3 => "fours"
        case 4 => "fives"
        case 5 => "sixes"
        case 6 => "three_of_kind"
        case 7 => "four_of_kind"
        case 8 => "full_house"
        case 9 => "small_straight"
        case 10 => "large_straight"
        case 11 => "yahtzee"
        case 12 => "chance"
      
      results(s"game_calculateScore_$categoryName") = profileMethod(s"game_calculateScore_$categoryName") {
        Game.calculateScore(dice, slot)
      }
    }
    
    // Straight detection
    val sortedDice = List(1, 2, 3, 4, 5)
    results("game_isSmallStraight") = profileMethod("game_isSmallStraight") {
      Game.isSmallStraight(sortedDice)
    }
    
    results("game_isLargeStraight") = profileMethod("game_isLargeStraight") {
      Game.isLargeStraight(sortedDice)
    }
    
    results.toMap
  
  def profileGameState(): Map[String, PerformanceMetrics] =
    val results = scala.collection.mutable.Map[String, PerformanceMetrics]()
    var seed = 12345L
    
    // GameState initial
    results("gamestate_initial") = profileMethod("gamestate_initial") {
      GameState.initial(2, seed)
    }
    
    val state = GameState.initial(2, seed)
    
    // Roll dice
    results("gamestate_rollDice") = profileMethod("gamestate_rollDice") {
      state.rollDice(Set(0, 2, 4))
    }
    
    // Record score
    results("gamestate_recordScore") = profileMethod("gamestate_recordScore") {
      state.recordScore(0)
    }
    
    // Is game over
    results("gamestate_isGameOver") = profileMethod("gamestate_isGameOver") {
      state.isGameOver
    }
    
    results.toMap
  
  def toJson(allResults: Map[String, Map[String, PerformanceMetrics]]): String =
    val sb = new StringBuilder
    sb.append("{\n")
    
    val modules = allResults.toList
    modules.zipWithIndex.foreach { case ((moduleName, methods), moduleIdx) =>
      sb.append(s"""  "$moduleName": {\n""")
      val methodList = methods.toList
      methodList.zipWithIndex.foreach { case ((methodName, metrics), methodIdx) =>
        sb.append(s"""    "$methodName": {\n""")
        sb.append(s"""      "execution_time_ms": ${metrics.executionTimeMs},\n""")
        sb.append(s"""      "execution_time_std": ${metrics.executionTimeStd},\n""")
        sb.append(s"""      "memory_used_kb": ${metrics.memoryUsedKb},\n""")
        sb.append(s"""      "memory_std_kb": ${metrics.memoryStdKb},\n""")
        sb.append(s"""      "num_trials": ${metrics.numTrials},\n""")
        sb.append(s"""      "samples_per_trial": ${metrics.samplesPerTrial}\n""")
        sb.append(s"""    }${if methodIdx < methodList.size - 1 then "," else ""}\n""")
      }
      sb.append(s"""  }${if moduleIdx < modules.size - 1 then "," else ""}\n""")
    }
    
    sb.append("}\n")
    sb.toString
  
  def main(args: Array[String]): Unit =
    println("Running Scala performance analysis...")
    println(f"Configuration: $NUM_TRIALS trials × $SAMPLES_PER_TRIAL samples per trial")
    println("=" * 80)
    
    val allResults = Map(
      "dice" -> profileDice(),
      "scorecard" -> profileScorecard(),
      "game" -> profileGame(),
      "gamestate" -> profileGameState()
    )
    
    // Save to JSON
    val jsonOutput = toJson(allResults)
    val outputPath = "../yahtzee_scala_analysis/data/performance_metrics.json"
    Using(new PrintWriter(outputPath)) { writer =>
      writer.write(jsonOutput)
    }
    
    // Print results
    println("\nPerformance Analysis Results:")
    println("=" * 80)
    
    allResults.foreach { case (module, methods) =>
      println(s"\n${module.toUpperCase}")
      println("-" * 80)
      methods.toList.sortBy(_._1).foreach { case (method, metrics) =>
        val timeStr = f"${metrics.executionTimeMs}%7.4f±${metrics.executionTimeStd}%6.4f"
        val memStr = f"${metrics.memoryUsedKb}%7.2f±${metrics.memoryStdKb}%5.2f"
        println(f"  $method%-35s | Time: ${timeStr}ms | Memory: ${memStr}KB")
      }
    }
    
    println(s"\nResults saved to: $outputPath")
    println(f"Statistics: Mean ± Std Dev from $NUM_TRIALS trials")
