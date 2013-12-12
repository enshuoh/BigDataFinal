generate RDD

def makeRDD[T](seq: Seq[(T, Seq[String])])(implicit arg0: ClassManifest[T]): RDD[T]
Distribute a local Scala collection to form an RDD, with one or more location preferences (hostnames of Spark nodes) for each object.

def makeRDD[T](seq: Seq[T], numSlices: Int)(implicit arg0: ClassManifest[T]): RDD[T]
Distribute a local Scala collection to form an RDD.

def hadoopFile[K, V, F <: InputFormat[K, V]](path: String)(implicit km: ClassManifest[K], vm: ClassManifest[V], fm: ClassManifest[F]): RDD[(K, V)]
Smarter version of hadoopFile() that uses class manifests to figure out the classes of keys, values and the InputFormat so that users don't need to pass them directly. Instead, callers can just write, for example,
val file = sparkContext.hadoopFile[LongWritable, Text, TextInputFormat](path)

def hadoopFile[K, V, F <: InputFormat[K, V]](path: String, minSplits: Int)(implicit km: ClassManifest[K], vm: ClassManifest[V], fm: ClassManifest[F]): RDD[(K, V)]
Smarter version of hadoopFile() that uses class manifests to figure out the classes of keys, values and the InputFormat so that users don't need to pass them directly. Instead, callers can just write, for example,
val file = sparkContext.hadoopFile[LongWritable, Text, TextInputFormat](path, minSplits)

def hadoopFile[K, V](path: String, inputFormatClass: Class[_ <: org.apache.hadoop.mapred.InputFormat[K,V]], keyClass: Class[K], valueClass: Class[V], minSplits: Int): RDD[(K, V)]
Get an RDD for a Hadoop file with an arbitrary InputFormat

def hadoopRDD[K, V](conf: JobConf, inputFormatClass: Class[_ <: org.apache.hadoop.mapred.InputFormat[K,V]], keyClass: Class[K], valueClass: Class[V], minSplits: Int): RDD[(K, V)]
Get an RDD for a Hadoop-readable dataset from a Hadoop JobConf giving its InputFormat and any other necessary info (e.g. file name for a filesystem-based dataset, table name for HyperTable, etc).

def newAPIHadoopFile[K, V, F <: InputFormat[K, V]](path: String, fClass: Class[F], kClass: Class[K], vClass: Class[V], conf: Configuration): RDD[(K, V)]
Get an RDD for a given Hadoop file with an arbitrary new API InputFormat and extra configuration options to pass to the input format.

def newAPIHadoopFile[K, V, F <: InputFormat[K, V]](path: String)(implicit km: ClassManifest[K], vm: ClassManifest[V], fm: ClassManifest[F]): RDD[(K, V)]
Get an RDD for a Hadoop file with an arbitrary new API InputFormat.

def newAPIHadoopRDD[K, V, F <: InputFormat[K, V]](conf: Configuration, fClass: Class[F], kClass: Class[K], vClass: Class[V]): RDD[(K, V)]
Get an RDD for a given Hadoop file with an arbitrary new API InputFormat and extra configuration options to pass to the input format.
	
def sequenceFile[K, V](path: String, minSplits: Int = defaultMinSplits)(implicit km: ClassManifest[K], vm: ClassManifest[V], kcf: () ⇒ WritableConverter[K], vcf: () ⇒ WritableConverter[V]): RDD[(K, V)]
Version of sequenceFile() for types implicitly convertible to Writables through a WritableConverter. For example, to access a SequenceFile where the keys are Text and the values are IntWritable, you could simply write
sparkContext.sequenceFile[String, Int](path, ...)
WritableConverters are provided in a somewhat strange way (by an implicit function) to support both subclasses of Writable and types for which we define a converter (e.g. Int to IntWritable). The most natural thing would've been to have implicit objects for the converters, but then we couldn't have an object for every subclass of Writable (you can't have a parameterized singleton object). We use functions instead to create a new converter for the appropriate type. In addition, we pass the converter a ClassManifest of its type to allow it to figure out the Writable class to use in the subclass case.

def sequenceFile[K, V](path: String, keyClass: Class[K], valueClass: Class[V]): RDD[(K, V)]
Get an RDD for a Hadoop SequenceFile with given key and value types.

def sequenceFile[K, V](path: String, keyClass: Class[K], valueClass: Class[V], minSplits: Int): RDD[(K, V)]
Get an RDD for a Hadoop SequenceFile with given key and value types.

def textFile(path: String, minSplits: Int = defaultMinSplits): RDD[String]
Read a text file from HDFS, a local file system (available on all nodes), or any Hadoop-supported file system URI, and return it as an RDD of Strings.


RDD

def ++(other: RDD[T]): RDD[T]
Return the union of this RDD and another one.

def union(other: RDD[T]): RDD[T]
Return the union of this RDD and another one.
/*
def subtract(other: RDD[T], p: Partitioner): RDD[T]
Return an RDD with the elements from this that are not in other.

def subtract(other: RDD[T], numPartitions: Int): RDD[T]
Return an RDD with the elements from this that are not in other.
*/
def subtract(other: RDD[T]): RDD[T]
Return an RDD with the elements from this that are not in other.

def aggregate[U](zeroValue: U)(seqOp: (U, T) ⇒ U, combOp: (U, U) ⇒ U)(implicit arg0: ClassManifest[U]): U
Aggregate the elements of each partition, and then the results for all the partitions, using given combine functions and a neutral "zero value".

def first(): T
Return the first element in this RDD.


def collect[U](f: PartialFunction[T, U])(implicit arg0: ClassManifest[U]): RDD[U]
Return an RDD that contains all matching values by applying f.

def collect(): Array[T]
Return an array that contains all of the elements in this RDD.

def distinct(): RDD[T]
/*
def distinct(numPartitions: Int): RDD[T]
Return a new RDD containing the distinct elements in this RDD.
*/
def filter(f: (T) ⇒ Boolean): RDD[T]
Return a new RDD containing only the elements that satisfy a predicate.
/*
def filterWith[A](constructA: (Int) ⇒ A)(p: (T, A) ⇒ Boolean)(implicit arg0: ClassManifest[A]): RDD[T]
Filters this RDD with p, where p takes an additional parameter of type A.
*/
def flatMap[U](f: (T) ⇒ TraversableOnce[U])(implicit arg0: ClassManifest[U]): RDD[U]
Return a new RDD by first applying a function to all elements of this RDD, and then flattening the results.
/*
def flatMapWith[A, U](constructA: (Int) ⇒ A, preservesPartitioning: Boolean)(f: (T, A) ⇒ Seq[U])(implicit arg0: ClassManifest[A], arg1: ClassManifest[U]): RDD[U]
FlatMaps f over this RDD, where f takes an additional parameter of type A.
*/
def fold(zeroValue: T)(op: (T, T) ⇒ T): T
Aggregate the elements of each partition, and then the results for all the partitions, using a given associative function and a neutral "zero value". The function op(t1, t2) is allowed to modify t1 and return it as its result value to avoid object allocation; however, it should not modify t2. 
/*
def groupBy[K](f: (T) ⇒ K, p: Partitioner)(implicit arg0: ClassManifest[K]): RDD[(K, Seq[T])]
Return an RDD of grouped items.

def groupBy[K](f: (T) ⇒ K, numPartitions: Int)(implicit arg0: ClassManifest[K]): RDD[(K, Seq[T])]
Return an RDD of grouped elements.
*/
def groupBy[K](f: (T) ⇒ K)(implicit arg0: ClassManifest[K]): RDD[(K, Seq[T])]
Return an RDD of grouped items.

def keyBy[K](f: (T) ⇒ K): RDD[(K, T)]
Creates tuples of the elements in this RDD by applying f.

def map[U](f: (T) ⇒ U)(implicit arg0: ClassManifest[U]): RDD[U]
Return a new RDD by applying a function to all elements of this RDD.

def reduce(f: (T, T) ⇒ T): T
Reduces the elements of this RDD using the specified commutative and associative binary operator.

def sample(withReplacement: Boolean, fraction: Double, seed: Int): RDD[T]
Return a sampled subset of this RDD.

def saveAsObjectFile(path: String): Unit
Save this RDD as a SequenceFile of serialized objects.

def saveAsTextFile(path: String, codec: Class[_ <: org.apache.hadoop.io.compress.CompressionCodec]): Unit
Save this RDD as a compressed text file, using string representations of elements.

def saveAsTextFile(path: String): Unit
Save this RDD as a text file, using string representations of elements.

