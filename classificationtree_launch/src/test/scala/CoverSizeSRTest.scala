import Constraints.CoverSizeSR
import DataManipulation.Data
import org.scalatest.FunSuite
import oscar.cp._
import oscar.cp.core.CPSolver
import oscar.cp.core.variables.CPIntVar

import scala.util.Random

class CoverSizeSRTest extends FunSuite {


  test("Coversize instanciation ") {

    val data = new Data("test", Array(
      (Array(0, 1, 2), 0),
      (Array(0, 1, 3, 4), 0)
    ))

    val nbTransaction = data.nbTransM
    val nbFeature = data.nbItem

    val solver = CPSolver()

    val takeVars = Array.fill(3)(CPIntVar(0 until nbFeature)(solver))
    val dropVars = Array.fill(3)(CPIntVar(0 until nbFeature)(solver))
    val sup = CPIntVar(0 to nbTransaction)(solver)

    val cst = new CoverSizeSR(takeVars, dropVars, sup, nbFeature, nbTransaction, data.dataM,data.dataMI)

    assert(sup.min == 0)
    assert(sup.max == 2)
    assert(takeVars.forall(_.min == 0))
    assert(takeVars.forall(_.max == nbFeature - 1))
    assert(takeVars.forall(_.size == nbFeature))
    assert(dropVars.forall(_.min == 0))
    assert(dropVars.forall(_.max == nbFeature - 1))
    assert(dropVars.forall(_.size == nbFeature))

    solver.add(cst)


  }

  test("Coversize Random test ") {

    for (i <- 0 until 100) {
      val randomData = Array.fill(100)((generateData(10), 0))

      val data = new Data("test", randomData)
      val nbTransaction = data.nbTransM
      val nbFeature = 10

      val assign = Array.tabulate(10)(i => (i, Random.nextInt(100))).sortBy(_._2)

      val solver = CPSolver()

      val takeVars = Array.fill(3)(CPIntVar(0 until nbFeature)(solver))
      val dropVars = Array.fill(3)(CPIntVar(0 until nbFeature)(solver))
      val sup = CPIntVar(0 to nbTransaction)(solver)

      val cst = new CoverSizeSR(takeVars, dropVars, sup, nbFeature, nbTransaction, data.dataM,data.dataMI)

      solver.add(cst)

      for (i <- 0 until 3) {
        solver.assign(takeVars(i), assign(i)._1)
        solver.assign(dropVars(i), assign(i + 3)._1)
      }

      assert(sup.isBound)
      assert(sup.min == randomData.count(a => takeVars.forall(x => a._1.contains(x.min) && dropVars.forall(x => !a._1.contains(x.min)))))
    }
  }

  test("Coversize Random test 2 ") {

    for (i <- 0 until 100) {
      val randomData = Array.fill(100)((generateDataDummy(10), 0))

      val data = new Data("test", randomData)
      val nbTransaction = data.nbTransM
      val nbFeature = 10

      val assign = Array.tabulate(9)(i => (i+1, Random.nextInt(100))).sortBy(_._2)

      val solver = CPSolver()

      val takeVars = Array.fill(3)(CPIntVar(0 until nbFeature)(solver))
      val dropVars = Array.fill(3)(CPIntVar(0 until nbFeature)(solver))
      val sup = CPIntVar(0 to nbTransaction)(solver)

      val cst = new CoverSizeSR(takeVars, dropVars, sup, nbFeature, nbTransaction, data.dataM,data.dataMI)

      solver.add(cst)

      for (i <- 0 until 2) {
        solver.assign(takeVars(i), assign(i)._1)
        solver.assign(dropVars(i), assign(i + 3)._1)
      }

    solver.add(sup < 10)

      solver.assign(takeVars.last,0)

    assert(1==1)
      solver.onSolution {
        assert(sup.isBound)
        assert(sup.min == randomData.count(a => takeVars.forall(x => a._1.contains(x.min) && dropVars.forall(x => !a._1.contains(x.min)))))
      }

      solver.search(
        binaryStatic(Array(takeVars.last,dropVars.last))
      )
      solver.start()
    }
  }


  def generateData(nbFeature: Int) = {
    var data: Array[Int] = Array()
    for (i <- 0 until nbFeature; if (Random.nextInt(2) == 1)) {
      data = data :+ i
    }
    data
  }

  def generateDataDummy(nbFeature: Int) = {
    var data: Array[Int] = Array()
    for (i <- 1 until nbFeature; if (Random.nextInt(2) == 1)) {
      data = data :+ i
    }
    data
  }
}


object tt extends App {

  def generateData(nbFeature: Int) = {
    var data: Array[Int] = Array()
    for (i <- 0 until nbFeature; if (Random.nextInt(2) == 1)) {
      data = data :+ i
    }
    data
  }

  val randomData = Array.fill(100)((generateData(10), 0))

  println(randomData.map(_._1.mkString(",")).mkString("\n"))
}

