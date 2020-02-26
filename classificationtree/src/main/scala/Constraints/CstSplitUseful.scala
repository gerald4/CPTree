package Constraints

import oscar.cp.constraints.Gr
import oscar.cp.core.variables.{CPIntVar, CPVar}
import oscar.cp.core.{CPPropagStrength, Constraint}
import oscar.cp.minimum

import scala.collection.Iterable

class CstSplitUseful(val decision: CPIntVar, val miniSum: CPIntVar, val countP: CPIntVar, val countM: CPIntVar, val errorUB:Int) extends Constraint(decision.store, "SplitUseful") {

  //  println( "sup " + Sup)
  override def associatedVars(): Iterable[CPVar] = Array(decision, miniSum, miniSumUB)

  //idempotent = true

  val miniSumUB: CPIntVar = CPIntVar(0 to errorUB, "minUB[" + miniSum.name + "]")(s)

    s.add(minimum(Array(countP, countM), miniSumUB))


  // ub > minisum
  class GrBis(x: CPIntVar, y: CPIntVar) extends Gr(x, y) {

    override def setup(l: CPPropagStrength): Unit = {
      if (!y.isBound && !x.isBound) {
        y.callPropagateWhenBoundsChange(this)
        x.callPropagateWhenBoundsChange(this)
        propagate()
      } else {
        x.updateMin(y.getMin + 1)
        y.updateMax(x.getMax - 1)
      }
    }

    override def propagate(): Unit = {
      x.updateMin(y.getMin + 1)
      y.updateMax(x.getMax - 1)
      if (x.getMin > y.getMax)
        this.deactivate()
    }
  }

  val cst = new GrBis(miniSumUB, miniSum)

  /**
    *
    * @param l
    * @return CPOutcome state
    */
  override def setup(l: CPPropagStrength): Unit = {
      decision.callPropagateWhenBoundsChange(this)
      propagate()

  }

  /**
    *
    * @return CPOutcome state
    */
  override def propagate(): Unit = {

    if (decision.min > 0) {
      s.add(cst)
      this.deactivate()
    } else if (decision.max == 0) {
      this.deactivate()
    }

  }


}