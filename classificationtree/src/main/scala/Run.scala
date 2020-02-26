import DataManipulation._

object CPDecisionTree extends App {

  if (args.size < 1) {
    println("usage: CPDT datafile" + " [-lb t minsup]"
      + " [-m max]" + " [-t testfile]")
    println("-lb t minsup: constraint on the minimum total number of examples in leafs (it t=% minsup is express in % of the total db, if t=# minsup is express in number)")
    println("-m max: specify maximum depth")
    println("-t testfile: run the learned tree on test data, output accuracy (can be used multiple times with various testfile")
    println("-complete: force tree to be complete")
    println("-save file: force tree to be complete")
    println("-format=binary or -format=sparse")
    println("-TO timeout: value in second of the timeout")
  } else {
    val file = args(0)
    var format: FileFormat = SparseFormat
    var TO = -1
    var isComplete = false
    var depth = 1
    var lbLeaf = 0
    var lbLeafPercent = true
    var heuristic = 0 // 0 = lexico, 1 = entropy, 2 = balance
    var saveFile: Option[String] = None
    var testFiles: List[String] = Nil
    var isCacheActive = true
    var isPrunningMinActive = true

    def process(args: List[String]): Boolean = {
      try {
        args match {
          case Nil =>
            true
          case "-lb" :: "%" :: x :: rest =>
            lbLeaf = x.toInt
            lbLeafPercent = true
            process(rest)
          case "-lb" :: "#" :: x :: rest =>
            lbLeaf = x.toInt
            lbLeafPercent = false
            process(rest)
          case "-m" :: x :: rest =>
            depth = x.toInt
            process(rest)
          case "-t" :: x :: rest =>
            testFiles = x :: testFiles
            process(rest)
          case "-complete" :: rest =>
            isComplete = true
            process(rest)
          case "-save" :: x :: rest =>
            saveFile = Some(x)
            process(rest)
          case "-format=binarypre" :: rest =>
            format = BinaryPreFormat
            process(rest)
          case "-format=binarypost" :: rest =>
            format = BinaryPostFormat
            process(rest)
          case "-format=sparse" :: rest =>
            format = SparseFormat
            process(rest)
          case "-TO" :: x :: rest =>
            TO = x.toInt
            process(rest)
          case "-heuristic" :: "entropy" :: rest =>
            heuristic = 1
            process(rest)
          case "-heuristic" :: "balance" :: rest =>
            heuristic = 2
            process(rest)
          case "-heuristic" :: "lex" :: rest =>
            heuristic = 0
            process(rest)
          case "-cache=no" :: rest =>
            isCacheActive = false
            process(rest)
          case "-cache=yes" :: rest =>
            isCacheActive = true
            process(rest)
          case "-minprunning=no" :: rest =>
            isPrunningMinActive = false
            process(rest)
          case "-minprunning=yes" :: rest =>
            isPrunningMinActive = true
            process(rest)
          case _ =>
            throw new WrongArgsException("wrong arguments " + args.mkString(" "))
        }
      }
      catch {
        case _: Throwable =>
          throw new WrongArgsException("wrong arguments " + args.mkString(" "))
      }
    }


    process(args.toList.drop(1))

    /// STEP 1 : build tree
    val tstart = System.currentTimeMillis()
    val tree = RunTreeANDOR.run(file, format, TO, isComplete, depth, lbLeaf, lbLeafPercent, heuristic,isPrunningMinActive,isCacheActive)
    val tend = System.currentTimeMillis()
    println("Time to compute "+ (tend - tstart))
    println("Tree: " + tree)

    /// STEP 2 : validation
    val validation = new Validation(tree)
    for (testFile <- testFiles)
      validation.validate(testFile, format)

  }


}

object DataSampler extends App {

  if (args.length < 1) {
    println("usage: DataSampler datafile" + " [-nb t X]"
      + " [-id I]")
    println("-nb t X: quantity of transaction to keep in the train file (it t=% X expressed in % of the total db, if t=# X expressed in number)")
    println("-id I: id number of the sampleling")
    println("-format=binarypre, -format=binarypost or -format=sparse")
  } else {
    val file = args(0)
    var format: FileFormat = SparseFormat
    var nb = 0
    var nbPercent = true
    var id = 0

    def process(args: List[String]): Boolean = {
      try {
        args match {
          case Nil =>
            true
          case "-nb" :: "%" :: x :: rest =>
            nb = x.toInt
            nbPercent = true
            process(rest)
          case "-nb" :: "#" :: x :: rest =>
            nb = x.toInt
            nbPercent = false
            process(rest)
          case "-id" :: x :: rest =>
            id = x.toInt
            process(rest)
          case "-format=binarypre" :: rest =>
            format = BinaryPreFormat
            process(rest)
          case "-format=binarypost" :: rest =>
            format = BinaryPostFormat
            process(rest)
          case "-format=sparse" :: rest =>
            format = SparseFormat
            process(rest)
          case _ =>
            throw new WrongArgsException("wrong arguments " + args.mkString(" "))
        }
      }
      catch {
        case _: Throwable =>
          throw new WrongArgsException("wrong arguments " + args.mkString(" "))
      }
    }


    process(args.toList.drop(1))

    val data = Data(file, format)

    if (nbPercent)
      data.sample(nb * data.nbTrans / 100, "" + id, format)
    else
      data.sample(nb, "" + id, format)

  }


}

object DataFormat extends App {

  if (args.length < 1) {
    println("usage: DataFormat datafile " + " [-nb t X]"
      + " [-id I]")
    println("-informat=binarypre, -informat=binarypost or -informat=sparse")
  } else {
    val file = args(0)
    var informat: FileFormat = SparseFormat
    var outformat: List[(FileFormat,String)] = List()
    var printinfo:Boolean = false

    def process(args: List[String]): Boolean = {
      try {
        args match {
          case Nil =>
            true
          case "-info" :: rest =>
            printinfo = true
            process(rest)
          case "-informat=binarypre" :: rest =>
            informat = BinaryPreFormat
            process(rest)
          case "-informat=binarypost" :: rest =>
            informat = BinaryPostFormat
            process(rest)
          case "-informat=sparse" :: rest =>
            informat = SparseFormat
            process(rest)
          case "-outformat=binarypre" :: x :: rest =>
            outformat = outformat :+ ((BinaryPreFormat,x))
            process(rest)
          case "-outformat=binarypost" :: x :: rest =>
            outformat = outformat :+ ((BinaryPostFormat,x))
            process(rest)
          case "-outformat=sparse" :: x :: rest =>
            outformat = outformat :+ ((SparseFormat,x))
            process(rest)
          case _ =>
            throw new WrongArgsException("wrong arguments " + args.mkString(" "))
        }
      }
      catch {
        case _: Throwable =>
          throw new WrongArgsException("wrong arguments " + args.mkString(" "))
      }
    }


    process(args.toList.drop(1))

    val data = Data(file, informat)

    if (printinfo){
      println(data.stringInfo())
    }

    for ((format,outputfile) <- outformat){
      data.printTo(outputfile,format)
    }


  }


}

class WrongArgsException(message: String) extends Exception(message)


object testing extends App {


//    val file = "./data/segment.txt"
//    val file = "./data/breast-wisconsin.txt"
//    val file = "./data/primary-tumor.txt"
  //  val file ="./toprocess/sparse/primary-tumor.txt"
  //  val file ="./toprocess/binary/primary-tumor.txt"
//    val file ="./toprocess/binary/kr-vs-kp.txt"
  //  val file ="./toprocess/binary/kr-vs-kp.txt"
  //  val file ="./data/australian-credit.txt"
//    val file ="./data/kr-vs-kp.txt"
//    val file ="./data/heart-cleveland.txt"
//    val file ="./data/audiology.txt"
//    val file ="./data/ionosphere.txt"
    val file ="./data/lymph.txt"
//    val file ="./data/anneal.txt"
//    val file ="./toprocess/sparse/mushroom.txt"
//    val file ="./monk1.txt"
//  val file = "./dataraw/Ionosphere.csv.train0.csv"
  val format: FileFormat = SparseFormat
  val TO: Int = 600
  val isComplete: Boolean = false
  val depth: Int = 4
  val lbLeaf: Int = 5
  val lbLeafPercent: Boolean = false
  val heuristic: Int = 1
  var isCacheActive = true
  var isPrunningMinActive = true
//  val tree = RunTree.run(file, format, TO, isComplete, depth, lbLeaf, lbLeafPercent, heuristic,isPrunningMinActive,isCacheActive)
//  println(tree)
  println("===============")
  val treeANDOR = RunTreeANDOR.run(file, format, TO, isComplete, depth, lbLeaf, lbLeafPercent, heuristic,isPrunningMinActive,isCacheActive)
  println(treeANDOR)
//  val validation = new Validation(tree)
//  validation.validate(file, format)


}

object createSamples extends App {
//  val bench = "kr-vs-kp"
//    val bench = "primary-tumor"
    val bench = "breast-wisconsin"
//    val bench = "mushroom"

  val file = "./data/" + bench + ".txt"

  val data = Data(file, SparseFormat).printTo("./toprocess/binary/" + bench , BinaryPreFormat)
  val file2 = "./toprocess/binary/" + bench + ".txt"

  val data2 = Data(file2, BinaryPreFormat).printTo("./toprocess/sparse/" + bench, SparseFormat)

  val data3 = Data(file,SparseFormat).printTo("./toprocess/binaryPost/" + bench, BinaryPostFormat)
}