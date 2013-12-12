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
  	args(0), 
   	"SparkLocalKMeans",
   	System.getenv("SPARK_HOME"), 
   	Seq(System.getenv("SPARK_EXAMPLES_JAR"))
)
val lines = sc.textFile(args(1))


var name
var name = number
var name = variable
var name = user_define_string

SparkKMeans

jobName
