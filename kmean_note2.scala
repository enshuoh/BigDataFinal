  val R = 1000     // Scaling factor
  val rand = new Random(42)

  def parseVector(line: String,Separator:String): Vector = {
  	return new Vector(line.split(Separator).map(_.toDouble))
  }


  def main(args: Array[String]) {

    val sc = new SparkContext(args(0), "SparkLocalKMeans",
      System.getenv("SPARK_HOME"), Seq(System.getenv("SPARK_EXAMPLES_JAR")))

    val lines = sc.textFile filePath
    //function fid 2_args_func args args
    val data = lines.map function parseVector 2_args_func line ' '
    //val data = lines.map(line -> parseVector(line,' ')) .cache()


    val K = args(2).toInt
    val convergeDist = args(3).toDouble
    
    //var kPoints = data.takeSample(false, K, 42).toArray
    var kPoints = data function takeSample 3_args_func "false" "K" "42"

    var tempDist = 1.0

    while tempDist > convergeDist {
    	//closestPoint -> to-do maybe use java to solve
    	//var closest = data.map (p => (closestPoint(p, kPoints), p))
    	var closest = data function map 1_args_func "(closestPoint(p, kPoints), p)"
    	//var closest = data function map 1_args_func tuple function closestPoint 2_args_func data_unit kPoints tuple data_unit 1

    	//args : tuple_init
    	//tuple_init : tuple expresion expression
    	//
    	var pointStats = closest.reduceByKey{ (p1,p2) =>p1+p2}

    }


    while(tempDist > convergeDist) {
      var closest = data.map (p => (closestPoint(p, kPoints), (p, 1)))
      
      var pointStats = closest.reduceByKey{case ((x1, y1), (x2, y2)) => (x1 + x2, y1 + y2)}
      
      var newPoints = pointStats.map {pair => (pair._1, pair._2._1 / pair._2._2)}.collectAsMap()
      
      tempDist = 0.0
      for (i <- 0 until K) {
        tempDist += kPoints(i).squaredDist(newPoints(i))
      }
      
      for (newP <- newPoints) {
        kPoints(newP._1) = newP._2
      }
      println("Finished iteration (delta = " + tempDist + ")")
    }

    println("Final centers:")
    kPoints.foreach(println)
    System.exit(0)
  }