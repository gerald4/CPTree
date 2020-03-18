package DataManipulation

import java.io.{File, PrintWriter}

abstract class FileFormat {
  val extension :String
  def readLines(lines:Array[String]) : Array[(Array[Int],Int)] = {
    lines.foreach(checkFormatLine(_))
    lines.map(readLine(_))
  }

  def checkFormatLine(line:String): Unit

  def readLine(line:String):(Array[Int],Int)

  def writeFile(outputName: String,data:Data):Unit = {
    val pw = new PrintWriter(new File(outputName+extension))
    writeTransactions(pw,data)
    pw.close()
  }
  def writeTransactions(printer:PrintWriter,data:Data):Unit = {
    var id = 0
    while (id < data.nbTrans) {
      printer.println(writeTransaction(data.rawDatas(id),data.nbItem))
      id += 1
    }
  }

  def writeTransaction(transaction: (Array[Int], Int),nbItem:Int):String
}


/**
  * Format sparse
  * F_i F_k F_l T
  * F_a F_i T
  */
object SparseFormat extends FileFormat {
  val extension :String=".txt"
  def checkFormatLine(line:String): Unit = {
    val data = line.split(" ")
    val pattern = "[0-9]*"
    assert(data.forall(str => str.matches(pattern)))
  }
  def readLine(line:String):(Array[Int],Int) = {
    val data = line.split(" ").map(_.toInt + 1)
    (data.dropRight(1).sorted, data.last - 1)
  }
  def writeTransaction(transaction: (Array[Int], Int),nbItem:Int):String = {
    var str = ""
    for (item <- transaction._1)
      str += (item - 1) + " "
    str + transaction._2
  }
}

/**
  * Format Binaire Pre Target
  * T 0 1 0 1 0 1
  * T 1 0 1 0 0 0
  * used by DL8
  */

object BinaryPreFormat extends FileFormat {
  val extension :String = ".txt"
  def checkFormatLine(line:String): Unit = {
    val data = line.split(" ")
    val pattern = "[0-1]*"
    assert(data.forall(str => str.matches(pattern)))
  }
  def readLine(line:String):(Array[Int],Int) = {
    val data = line.split(" ").map(_.toInt)
    val buffer = new scala.collection.mutable.ArrayBuffer[Int]()
    var i = 1
    while (i < data.length) {
      if (data(i) == 1)
        buffer += i
      i += 1
    }
    (buffer.toArray, data.head)
  }
  def writeTransaction(transaction: (Array[Int], Int),nbItem:Int):String = {
    val arr = Array.fill(nbItem - 1)(0)
    for (id <- transaction._1)
      arr(id - 1) = 1
    transaction._2 + " " + arr.mkString(" ")
  }
}

/**
  * Format Binaire Pre Target
  * 0;1;0;1;0;1;T
  * 1;0;1;0;0;0;T
  * used by BinOCT
  */
object BinaryPostFormat extends FileFormat {
  val extension :String = ".csv"
  def checkFormatLine(line:String): Unit = {
    val data = line.split(";")
    val pattern = "[0-1]*"
    assert(data.forall(str => str.matches(pattern)))
  }
  override def readLines(lines:Array[String]) : Array[(Array[Int],Int)] =
    lines.drop(1).map(readLine(_))

  def readLine(line:String):(Array[Int],Int) = {
    val data = line.split(";").map(_.toInt)
    val buffer = new scala.collection.mutable.ArrayBuffer[Int]()
    var i = 0
    while (i < data.length-1) {
      if (data(i) == 1)
        buffer += (i+1)
      i += 1
    }
    (buffer.toArray, data.last)
  }
  override def writeTransactions(printer:PrintWriter,data:Data):Unit = {
    printer.println((0 until data.nbItem-1).map("Feat_"+_).mkString(";")+";target")
    super.writeTransactions(printer,data)
  }
  def writeTransaction(transaction: (Array[Int], Int),nbItem:Int):String = {
    val arr = Array.fill(nbItem - 1)(0)
    for (id <- transaction._1)
      arr(id - 1) = 1
    arr.mkString(";") + ";"+transaction._2
  }
}
