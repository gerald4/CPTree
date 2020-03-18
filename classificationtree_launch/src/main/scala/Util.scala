import oscar.cp.CPIntVar

object Util {
//  def readDatasFrom(file: String) = {
//    val result1 = fromFile(file).getLines().toArray.map(_.split(" ").map(_.toInt))
//
//    val nbItem = result1.map(_.max).max + 1
//    val dataPt = Array.fill(nbItem)(new scala.collection.mutable.ArrayBuffer[Int]())
//    val dataMt = Array.fill(nbItem)(new scala.collection.mutable.ArrayBuffer[Int]())
//    val res = result1.groupBy(_.last)
//    var nbTransP = 0
//    for (id <- res(0).indices) {
//      nbTransP += 1
//      for (item <- res(0)(id).dropRight(1))
//        dataPt(item) += id
//    }
//    var nbTransM = 0
//    for (id <- res(1).indices) {
//      nbTransM += 1
//      for (item <- res(1)(id).dropRight(1))
//        dataMt(item) += id
//    }
//    val dataP = dataPt.map(_.toSet)
//    val dataM = dataMt.map(_.toSet)
//    (nbItem, nbTransP, dataP, nbTransM, dataM)
//  }
//
//  def readDatasFromWithDummy(file: String) = {
//    val result1 = fromFile(file).getLines().toArray.map(_.split(" ").map(_.toInt))
//
//    val nbItem = result1.map(_.max).max + 1
//    val dataPt = Array.fill(nbItem + 1)(new scala.collection.mutable.ArrayBuffer[Int]())
//    val dataMt = Array.fill(nbItem + 1)(new scala.collection.mutable.ArrayBuffer[Int]())
//    val res = result1.groupBy(_.last)
//    var nbTransP = 0
//    for (id <- res(0).indices) {
//      nbTransP += 1
//      for (item <- res(0)(id).dropRight(1))
//        dataPt(item + 1) += id
//    }
//    var nbTransM = 0
//    for (id <- res(1).indices) {
//      nbTransM += 1
//      for (item <- res(1)(id).dropRight(1))
//        dataMt(item + 1) += id
//    }
//    val dataP = dataPt.map(_.toSet)
//    val dataM = dataMt.map(_.toSet)
//    (nbItem + 1, nbTransP, dataP, nbTransM, dataM)
//  }
//
//  def readDatasFromExample() = {
//    val nbItem = 4
//
//    //  val dataP = Array(Set(0,2),Set(0,1),Set(0,1,3))
//    val dataP = Array(Set(0, 1, 2), Set(1, 2), Set(0), Set(2))
//    val nbTransP = 3
//    //  val dataM = Array(Set(2),Set(1,2,3),Set(2,3))
//    val dataM = Array(Set(0), Set(1), Set(1, 2), Set(1, 2))
//    val nbTransM = 3
//
//    (nbItem, nbTransP, dataP, nbTransM, dataM)
//  }
//
//  def readDatasFromExampleWithDummy = {
//    val nbItem = 10
//
//    //  val dataP = Array(Set(0,2),Set(0,1),Set(0,1,3))
//    val dataP = Array(Set(), Set(0 until 20), Set(0 until 60), Set(),Set(),Set(),Set(),Set(),Set(60 until 80),Set(80 until 100))
//    val nbTransP = 100
//    //  val dataM = Array(Set(2),Set(1,2,3),Set(2,3))
//    val dataM = Array(Set(), Set(), Set(0 until 60), Set(0 until 20),Set(),Set(),Set(),Set(),Set(80 until 100),Set(60 until 80))
//    val nbTransM = 100
//  }
//
//  val benchmarks = Array(
//    "anneal", "australian-credit", "breast-wisconsin", "diabetes", "german-credit", "heart-cleveland", "hypothyroid",
//    "ionosphere", "kr-vs-kp", "letter", "mushroom", "pendigits", "primary-tumor", "segment", "soybean", "splice-1", "vehicle", "yeast"
//  )
//  val benchmarksMIP = Array(
//    "breast-wisconsin", "heart-cleveland", "ionosphere"
//  )

  def treeString(depth: Int, decisions: Array[CPIntVar], countP:Array[CPIntVar], countM:Array[CPIntVar]): String = {
    val lines = Array.fill(Math.pow(2, depth).toInt * 2 - 1, depth + 1)("")

    for (i <- 0 to depth) {
      val offset = Math.pow(2, depth - i).toInt
      for (j <- 0 until Math.pow(2, i).toInt) {
        val idx = offset - 1 + j * 2 * offset
        if (i != depth)
          for (k <- -offset / 2 to offset / 2; if k != 0)
            lines(idx + k)(i + 1) += "|"
        lines(idx)(i) += "-  "
        if (i != depth)
          lines(idx)(i) += decisions(Math.pow(2, i).toInt + j-1)
        else
          lines(idx)(i) += (if (countP(j).min > countM(j).min) "+" else "-")+ "\t"+ Math.min(countP(j).min,countM(j).min) + "\t"+ countP(j).min + "/" + countM(j).min
      }
    }
    lines.map(_.mkString("\t\t")).mkString("\n")
  }
  def treeString2(depth: Int, decisions: Array[CPIntVar], countP:Array[CPIntVar], countM:Array[CPIntVar]): String = {
    val k =  Math.pow(2, depth).toInt
    val lines = Array.fill(k * 2 - 1, depth + 1)("")

    for (i <- 0 to depth) {
      val offset = Math.pow(2, depth - i).toInt
      for (j <- 0 until Math.pow(2, i).toInt) {
        val idx = offset - 1 + j * 2 * offset
        if (i != depth)
          for (k <- -offset / 2 to offset / 2; if k != 0)
            lines(idx + k)(i + 1) += "|"
        lines(idx)(i) += "-  "
        if (i != depth)
          lines(idx)(i) += decisions(Math.pow(2, i).toInt + j-1) + " " + countP(Math.pow(2, i).toInt-1+j).min + "/"+ countM(Math.pow(2, i).toInt-1+j).min
        else
          lines(idx)(i) += (if (countP(k-1+j).min > countM(k-1+j).min) "+" else "-")+ "\t"+ Math.min(countP(k-1+j).min,countM(k-1+j).min) + "\t"+ countP(k-1+j).min + "/" + countM(k-1+j).min
      }
    }
    lines.map(_.mkString("\t\t")).mkString("\n")
  }

  def treeString3(depth: Int, decisions: Array[Int], countP:Array[Int], countM:Array[Int]): String = {
    val k =  Math.pow(2, depth).toInt
    val lines = Array.fill(k * 2 - 1, depth + 1)("")

    for (i <- 0 to depth) {
      val offset = Math.pow(2, depth - i).toInt
      for (j <- 0 until Math.pow(2, i).toInt) {
        val idx = offset - 1 + j * 2 * offset
        if (i != depth)
          for (k <- -offset / 2 to offset / 2; if k != 0)
            lines(idx + k)(i + 1) += "|"
        lines(idx)(i) += "-  "
        if (i != depth)
          lines(idx)(i) += decisions(Math.pow(2, i).toInt + j-1) + " " + countP(Math.pow(2, i).toInt-1+j) + "/"+ countM(Math.pow(2, i).toInt-1+j)
        else
          lines(idx)(i) += (if (countP(k-1+j) > countM(k-1+j)) "+" else "-")+ "\t"+ Math.min(countP(k-1+j),countM(k-1+j)) + "\t"+ countP(k-1+j) + "/" + countM(k-1+j)
      }
    }
    lines.map(_.mkString("\t\t")).mkString("\n")
  }



}
