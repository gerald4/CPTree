package Constraints

import oscar.cp.core.{CPPropagStrength, Constraint}
import oscar.cp.core.variables.{CPIntVar, CPVar}

import scala.collection.Iterable

class CstSplitPossible(val decision: CPIntVar, val countP: CPIntVar, val countM: CPIntVar, val countSum: CPIntVar, threshold: Int) extends Constraint(decision.store, "SplitPossible") {

  override def associatedVars(): Iterable[CPVar] = Array(decision, countP, countM, countSum)

  val threshold2 = 2 * threshold

  /**
    *
    * @param l
    * @return CPOutcome state
    */
  override def setup(l: CPPropagStrength): Unit = {
    countSum.callPropagateWhenBoundsChange(this)
    decision.callPropagateWhenBoundsChange(this)
    propagate()
  }

  /**
    *
    * @return CPOutcome state
    */
  override def propagate(): Unit = {

    if (countP.max == 0 || countM.max == 0) { // If partition, no need to make decisions
      decision.assign(0)
      this.deactivate()
    } else if (countSum.max < threshold2) { // If not enough to partition into, takes no decisions
      decision.assign(0)
      this.deactivate()
    } else if (decision.min > 0) { // If decision 0 already removed, should have enough to partition
      countSum.updateMin(threshold2)
      this.deactivate()
    }

  }


}
