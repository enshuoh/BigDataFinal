Object kmeans
val R = 1000
val rand = USERDEFINE "new Random(42)"

	/*
	SparkContext(master: String, jobName: String, sparkHome: String, jars: Seq[String]):
	master      Cluster URL to connect to (e.g. mesos://host:port, spark://host:port, local[4]).
	jobName     A name for your job, to display on the cluster web UI
	sparkHome   Location where Spark is installed on cluster nodes.
	jars        Collection of JARs to send to the cluster. These can be paths on the local file system or HDFS, HTTP, HTTPS, or FTP URLs. 
	*/
val sc = new SparkContext(
  	"jobName", 
   	"SparkLocalKMeans",
   	System.getenv("SPARK_HOME"), 
   	Seq(System.getenv("SPARK_EXAMPLES_JAR"))
)

val K = 10
val lines = sc.textFile("input.data")
val convergeDist = 0.1
val data = lines.map(line => new Vector(line.split(' ').map(_.toDouble)))
//def takeSample(withReplacement: Boolean, num: Int, seed: Int): Array[T] 

var kPoints = data.takeSample(false, K, 42).toArray

var tempDist = 1.0
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
SparkKMeans

jobName
val R = 1000
val rand = userdefine "new Random(42)"
val K = 10
val lines = textFile("input.data")
val convergeDist = 0.1